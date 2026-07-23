# SPDX-License-Identifier: LGPL-3.0-or-later
# PipingHF - Pipe Feature (Part::FeaturePython paramétrico)

import FreeCAD
import FreeCADGui
import Part


class PipeSegment:
    """Tramo recto de tubería paramétrico.
    
    FeaturePython que crea un cilindro hueco con dimensiones según
    diámetro nominal (NPS) y cédula (SCH).
    
    Propiedades:
        Diameter: Diámetro nominal en pulgadas (float)
        Schedule: Cédula (STR: SCH 40, SCH 80, etc.)
        Length: Longitud del tramo (mm)
        Material: Material del tubo (STR)
    """

    def __init__(self, obj):
        """Inicializa el feature pipe."""
        obj.addProperty(
            "App::PropertyFloat", "Diameter",
            "Pipe", "Diámetro nominal (NPS) en pulgadas"
        ).Diameter = 6.0
        
        obj.addProperty(
            "App::PropertyEnumeration", "Schedule",
            "Pipe", "Cédula del tubo"
        )
        obj.Schedule = ["SCH 40", "SCH 80", "SCH 160", "SCH STD", "SCH XS", "SCH XXS", "SCH 10", "SCH 20"]
        obj.Schedule = "SCH 80"
        
        obj.addProperty(
            "App::PropertyLength", "Length",
            "Pipe", "Longitud del tramo (mm)"
        ).Length = 1000.0
        
        obj.addProperty(
            "App::PropertyString", "Material",
            "Pipe", "Material del tubo"
        ).Material = "API 5L X52"
        
        obj.addProperty(
            "App::PropertyFloat", "OD",
            "Pipe", "Diámetro exterior (mm) - solo lectura"
        ).OD = 0.0
        
        obj.addProperty(
            "App::PropertyFloat", "Wall",
            "Pipe", "Espesor de pared (mm) - solo lectura"
        ).Wall = 0.0
        
        obj.Proxy = self

    def execute(self, fp):
        """Genera la geometría del tubo cuando cambian las propiedades."""
        od, wall = self._get_pipe_dimensions(fp.Diameter, fp.Schedule)
        fp.OD = od
        fp.Wall = wall
        
        length = fp.Length
        
        # Cilindro exterior
        outer = Part.makeCylinder(od / 2.0, length)
        
        # Cilindro interior (hueco)
        inner = Part.makeCylinder((od / 2.0) - wall, length)
        
        # Tubo = cilindro exterior - cilindro interior
        fp.Shape = outer.cut(inner)

    def _get_pipe_dimensions(self, nps_inches, schedule):
        """Retorna (OD_mm, wall_mm) según NPS y schedule.
        
        Fuente: ASME B36.10M - Tabla de tubería de acero.
        """
        # OD según diámetro nominal (NPS en pulgadas → mm)
        od_table = {
            0.125: 10.29, 0.25: 13.72, 0.375: 17.15, 0.5: 21.34,
            0.75: 26.67, 1.0: 33.40, 1.25: 42.16, 1.5: 48.26,
            2.0: 60.33, 2.5: 73.03, 3.0: 88.90, 4.0: 114.30,
            5.0: 141.30, 6.0: 168.28, 8.0: 219.08, 10.0: 273.05,
            12.0: 323.85, 14.0: 355.60, 16.0: 406.40, 18.0: 457.20,
            20.0: 508.00, 24.0: 609.60, 30.0: 762.00, 36.0: 914.40,
        }
        od = od_table.get(nps_inches, 168.28)

        # Espesores de pared (mm) para SCH 40/80/STD/XS/160
        # Valores según ASME B36.10M para cada NPS
        wall_table = {
            "SCH 10":  {
                0.5: 1.65, 0.75: 1.65, 1.0: 2.11, 1.25: 2.11, 1.5: 2.11,
                2.0: 2.11, 2.5: 2.77, 3.0: 2.77, 4.0: 2.77, 5.0: 3.40,
                6.0: 3.40, 8.0: 4.06, 10.0: 4.06, 12.0: 4.57,
            },
            "SCH 40": {
                0.5: 2.77, 0.75: 2.77, 1.0: 3.38, 1.25: 3.56, 1.5: 3.68,
                2.0: 3.91, 2.5: 5.16, 3.0: 5.49, 4.0: 6.02, 5.0: 6.55,
                6.0: 7.11, 8.0: 8.18, 10.0: 9.27, 12.0: 10.31,
            },
            "SCH STD": {
                0.5: 2.77, 0.75: 2.77, 1.0: 3.38, 1.25: 3.56, 1.5: 3.68,
                2.0: 3.91, 2.5: 5.16, 3.0: 5.49, 4.0: 6.02, 5.0: 6.55,
                6.0: 7.11, 8.0: 8.18, 10.0: 9.27, 12.0: 10.31,
            },
            "SCH 80": {
                0.5: 3.73, 0.75: 3.91, 1.0: 4.55, 1.25: 4.85, 1.5: 5.08,
                2.0: 5.54, 2.5: 7.01, 3.0: 7.62, 4.0: 8.56, 5.0: 9.53,
                6.0: 10.97, 8.0: 12.70, 10.0: 15.09, 12.0: 17.48,
            },
            "SCH XS": {
                0.5: 3.73, 0.75: 3.91, 1.0: 4.55, 1.25: 4.85, 1.5: 5.08,
                2.0: 5.54, 2.5: 7.01, 3.0: 7.62, 4.0: 8.56, 5.0: 9.53,
                6.0: 10.97, 8.0: 12.70, 10.0: 15.09, 12.0: 17.48,
            },
            "SCH 160": {
                0.5: 4.78, 0.75: 5.56, 1.0: 6.35, 1.25: 7.14, 1.5: 7.14,
                2.0: 8.74, 2.5: 10.16, 3.0: 11.13, 4.0: 13.49, 5.0: 15.88,
                6.0: 18.26, 8.0: 23.01, 10.0: 28.45, 12.0: 33.32,
            },
            "SCH XXS": {
                0.5: 7.47, 0.75: 7.82, 1.0: 9.09, 1.25: 9.70, 1.5: 10.16,
                2.0: 11.07, 2.5: 14.02, 3.0: 15.24, 4.0: 17.12, 5.0: 19.05,
                6.0: 21.95, 8.0: 25.40, 10.0: 30.18, 12.0: 34.93,
            },
        }

        schedule_map = {
            "SCH 40": "SCH 40", "SCH 80": "SCH 80", "SCH 160": "SCH 160",
            "SCH STD": "SCH STD", "SCH XS": "SCH XS", "SCH XXS": "SCH XXS",
            "SCH 10": "SCH 10", "SCH 20": "SCH 10",
        }

        sch = schedule_map.get(schedule, "SCH 80")
        walls = wall_table.get(sch, {})
        wall = walls.get(nps_inches, 10.97)

        return od, wall


class ViewProviderPipe:
    """View provider para el PipeSegment - controla apariencia en 3D."""

    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        return """
        /* XPM icon for pipe */
        static const char *pipe_icon[] = {
            "16 16 2 1",
            "  c None",
            ". c #0000FF",
            "                ",
            "   ........     ",
            "  .        .    ",
            " .          .   ",
            " .          .   ",
            " .          .   ",
            " .          .   ",
            " .          .   ",
            " .          .   ",
            " .          .   ",
            " .          .   ",
            " .          .   ",
            "  .        .    ",
            "   ........     ",
            "                ",
            "                "};
        """

    def attach(self, vobj):
        self.ViewObject = vobj

    def updateData(self, obj, prop):
        return

    def onChanged(self, vobj, prop):
        return

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


def make_pipe_segment(diameter=6.0, schedule="SCH 80", length=1000.0, material="API 5L X52"):
    """Crea un PipeSegment en el documento activo de FreeCAD.
    
    Args:
        diameter: NPS en pulgadas
        schedule: Cédula
        length: Longitud en mm
        material: Material del tubo
    
    Returns:
        El objeto FeaturePython creado.
    """
    doc = FreeCAD.ActiveDocument
    if doc is None:
        FreeCAD.Console.PrintError("No hay documento activo.\n")
        return None

    obj = doc.addObject("Part::FeaturePython", "Pipe")
    PipeSegment(obj)
    
    # ViewProvider solo cuando hay GUI
    try:
        import FreeCADGui
        if FreeCADGui.GuiUp:
            ViewProviderPipe(obj.ViewObject)
    except Exception:
        pass

    obj.Diameter = diameter
    obj.Schedule = schedule
    obj.Length = length
    obj.Material = material

    doc.recompute()
    return obj
