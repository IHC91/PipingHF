# SPDX-License-Identifier: LGPL-3.0-or-later
# PipingHF - Brida Weld Neck paramétrica (ASME B16.5)

import FreeCAD
import FreeCADGui
import Part
from FreeCAD import Vector


class FlangeWN:
    """Brida de cuello soldable (Weld Neck) paramétrica según ASME B16.5.
    
    Propiedades:
        Diameter: NPS (pulgadas)
        Class: Clase de presión (150, 300, 600)
        Bore: Diámetro interior = OD del tubo correspondiente
    """

    def __init__(self, obj):
        obj.addProperty(
            "App::PropertyFloat", "Diameter",
            "Flange", "Diámetro nominal NPS (pulgadas)"
        ).Diameter = 6.0

        obj.addProperty(
            "App::PropertyEnumeration", "Class",
            "Flange", "Clase de presión ASME"
        )
        obj.Class = ["150", "300", "600"]
        obj.Class = "150"

        obj.addProperty(
            "App::PropertyFloat", "OD",
            "Flange", "Diámetro exterior (mm) - solo lectura"
        ).OD = 0.0

        obj.addProperty(
            "App::PropertyFloat", "Thickness",
            "Flange", "Espesor (mm) - solo lectura"
        ).Thickness = 0.0

        obj.addProperty(
            "App::PropertyFloat", "HubOD",
            "Flange", "OD del hub en la base (mm) - solo lectura"
        ).HubOD = 0.0

        obj.addProperty(
            "App::PropertyFloat", "HubLength",
            "Flange", "Longitud del hub (mm) - solo lectura"
        ).HubLength = 0.0

        obj.addProperty(
            "App::PropertyFloat", "Bore",
            "Flange", "Diámetro interior = bore del tubo (mm)"
        ).Bore = 0.0

        obj.addProperty(
            "App::PropertyInteger", "BoltHoles",
            "Flange", "Número de huecos para pernos - solo lectura"
        ).BoltHoles = 8

        obj.Proxy = self

    def execute(self, fp):
        """Genera la geometría de la brida."""
        from src.catalog.pipe_schedule import FlangeCatalog, PipeCatalog

        dims = FlangeCatalog.get_flange_dimensions(fp.Diameter, fp.Class)
        if dims is None:
            FreeCAD.Console.PrintError(
                f"Brida WN Class {fp.Class}, NPS {fp.Diameter}: no disponible en catálogo\n"
            )
            return

        od, wall = PipeCatalog.get_pipe_dimensions(fp.Diameter, "SCH 80")

        fp.OD = dims["OD"]
        fp.Thickness = dims["t"]
        fp.HubOD = dims["X"]
        fp.HubLength = dims["H"]
        fp.Bore = od
        fp.BoltHoles = dims["Holes"]

        # Alturas de cada sección de la brida:
        #   flange_thick = espesor del disco de brida
        #   hub_length = altura del cuello cónico
        flange_thick = dims["t"]
        hub_length = dims["H"]
        total_height = flange_thick + hub_length

        # Diámetros
        flange_od = dims["OD"]
        hub_base_od = dims["X"]
        bore = od
        hub_top_od = hub_base_od * 0.75  # Hub se reduce en la parte superior

        # --- Construir brida como revolución de perfil ---
        # Perfil en el plano XZ (luego revolucionar alrededor del eje Z)
        
        # Puntos del perfil (r, z) — mitad derecha de la brida
        profile_points = [
            Vector(bore / 2.0, 0),                    # P0: interior abajo
            Vector(bore / 2.0, total_height),          # P1: interior arriba (bore)
            Vector(hub_top_od / 2.0, total_height),    # P2: top del hub
            Vector(hub_base_od / 2.0, flange_thick),   # P3: base del hub
            Vector(flange_od / 2.0, flange_thick),     # P4: OD de la brida
            Vector(flange_od / 2.0, 0),                # P5: OD abajo
            Vector(bore / 2.0, 0),                     # P0: cerrar
        ]

        # Crear el perfil como wire
        edges = []
        for i in range(len(profile_points) - 1):
            p1 = profile_points[i]
            p2 = profile_points[i + 1]
            edges.append(Part.Edge(Part.LineSegment(p1, p2)))
        
        profile_wire = Part.Wire(edges)
        profile_face = Part.Face(profile_wire)

        # Revolucionar 360° alrededor del eje Z
        revolution = profile_face.revolve(Vector(0, 0, 0), Vector(0, 0, 1), 360)

        fp.Shape = revolution

    def _get_flange_dims(self, nps, flange_class):
        """Obtiene dimensiones de brida del catálogo."""
        from src.catalog.pipe_schedule import FlangeCatalog
        return FlangeCatalog.get_flange_dimensions(nps, flange_class)


class ViewProviderFlange:
    """View provider para brida."""

    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        return "flange_wn"

    def attach(self, vobj):
        self.ViewObject = vobj

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


def make_flange_wn(diameter=6.0, flange_class="150"):
    """Crea una brida WN en el documento activo."""
    doc = FreeCAD.ActiveDocument
    if doc is None:
        doc = FreeCAD.newDocument("Piping")

    obj = doc.addObject("Part::FeaturePython", "FlangeWN")
    FlangeWN(obj)
    
    try:
        import FreeCADGui
        if FreeCADGui.GuiUp:
            ViewProviderFlange(obj.ViewObject)
    except Exception:
        pass

    obj.Diameter = diameter
    obj.Class = flange_class

    doc.recompute()
    return obj
