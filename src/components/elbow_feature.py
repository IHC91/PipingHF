# SPDX-License-Identifier: LGPL-3.0-or-later
# PipingHF - Codo 90° Long Radius paramétrico (ASME B16.9)

import math
import FreeCAD
import FreeCADGui
import Part
from FreeCAD import Vector


class Elbow90:
    """Codo 90° Long Radius paramétrico según ASME B16.9.
    
    Crea un codo 3D como barrido de un círculo a lo largo de un arco.
    
    Propiedades:
        Diameter: NPS (pulgadas)
        Schedule: Cédula
        Radius: Radio de curvatura (LR = 1.5 × OD)
        Angle: Ángulo del codo (45-90°)
    """

    def __init__(self, obj):
        obj.addProperty(
            "App::PropertyFloat", "Diameter",
            "Elbow", "Diámetro nominal NPS (pulgadas)"
        ).Diameter = 6.0

        obj.addProperty(
            "App::PropertyEnumeration", "Schedule",
            "Elbow", "Cédula"
        )
        obj.Schedule = ["SCH 40", "SCH 80", "SCH 160", "SCH STD", "SCH XS", "SCH XXS"]
        obj.Schedule = "SCH 80"

        obj.addProperty(
            "App::PropertyFloat", "Radius",
            "Elbow", "Radio de curvatura center-to-end (mm)"
        ).Radius = 228.6  # 1.5 * 168.28 * 0.5 para NPS 6

        obj.addProperty(
            "App::PropertyAngle", "Angle",
            "Elbow", "Ángulo del codo"
        ).Angle = 90.0

        obj.addProperty(
            "App::PropertyFloat", "OD",
            "Elbow", "OD (mm) - solo lectura"
        ).OD = 0.0

        obj.addProperty(
            "App::PropertyFloat", "Wall",
            "Elbow", "Wall (mm) - solo lectura"
        ).Wall = 0.0

        obj.Proxy = self

    def execute(self, fp):
        """Genera la geometría del codo."""
        from src.catalog.pipe_schedule import PipeCatalog, ElbowCatalog

        od, wall = PipeCatalog.get_pipe_dimensions(fp.Diameter, fp.Schedule)
        fp.OD = od
        fp.Wall = wall

        # Radio center-to-end según ASME B16.9
        cte = ElbowCatalog.get_center_to_end(fp.Diameter, 90, "LR")
        fp.Radius = cte

        angle_rad = math.radians(fp.Angle)

        # Construir codo como toroide hueco
        # Es más confiable en modo consola que el sweep
        try:
            angle_val = float(fp.Angle)
            # Toroide exterior: codo de radio cte, tubo de radio OD/2
            outer_torus = Part.makeTorus(cte, od / 2.0, 
                                          Vector(0, 0, 0), Vector(0, 0, 1),
                                          angle_val)
            # Toroide interior: remove el material interior
            inner_torus = Part.makeTorus(cte, (od / 2.0) - wall,
                                          Vector(0, 0, 0), Vector(0, 0, 1),
                                          angle_val)
            fp.Shape = outer_torus.cut(inner_torus)
        except Exception as e:
            FreeCAD.Console.PrintError(f"Elbow failed: {e}\n")

    def _fallback_geometry(self, fp, od, wall, cte, angle_rad):
        """Geometría alternativa para el codo como revolución de un perfil."""
        # Crear perfil L-shaped del codo en sección
        inner_r = cte - od / 2.0
        outer_r = cte + od / 2.0
        
        # Anillo como toroide
        torus = Part.makeTorus(cte, od / 2.0, angle_rad)
        torus_inner = Part.makeTorus(cte, od / 2.0 - wall, angle_rad)
        
        # Codo = toroide exterior - toroide interior
        fp.Shape = torus.cut(torus_inner)

    def _get_elbow_dimensions(self, nps):
        """Retorna center-to-end (mm) para codo 90° LR."""
        dims = {
            0.5: 38, 0.75: 38, 1: 38, 1.25: 38, 1.5: 38,
            2: 51, 2.5: 64, 3: 76, 4: 102, 5: 127,
            6: 152, 8: 203, 10: 254, 12: 305,
            14: 356, 16: 406, 18: 457, 20: 508, 24: 610,
        }
        return dims.get(nps, 152)


class ViewProviderElbow:
    """View provider para el codo."""

    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        return "elbow_90"

    def attach(self, vobj):
        self.ViewObject = vobj

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


def make_elbow(diameter=6.0, schedule="SCH 80", angle=90.0):
    """Crea un codo en el documento activo."""
    doc = FreeCAD.ActiveDocument
    if doc is None:
        doc = FreeCAD.newDocument("Piping")

    obj = doc.addObject("Part::FeaturePython", "Elbow90")
    Elbow90(obj)
    
    try:
        import FreeCADGui
        if FreeCADGui.GuiUp:
            ViewProviderElbow(obj.ViewObject)
    except Exception:
        pass

    obj.Diameter = diameter
    obj.Schedule = schedule
    obj.Angle = angle

    doc.recompute()
    return obj
