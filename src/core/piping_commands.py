# SPDX-License-Identifier: LGPL-3.0-or-later
# PipingHF - Sistema de comandos

import FreeCAD
import FreeCADGui
from PySide import QtGui


class CmdPipeSegment:
    """Comando: Insertar tramo recto de tubería."""

    def GetResources(self):
        return {
            "Pixmap": "pipe_segment",
            "MenuText": "Tubo recto",
            "ToolTip": "Inserta un tramo recto de tubería paramétrico (NPS, SCH, longitud)"
        }

    def Activated(self):
        from src.core.pipe_feature import make_pipe_segment
        doc = FreeCAD.ActiveDocument
        if doc is None:
            doc = FreeCAD.newDocument("Piping")
        
        import FreeCADGui
        from PySide import QtGui
        
        # Diálogo simple para parámetros del tubo
        diameter, ok1 = QtGui.QInputDialog.getDouble(
            None, "Tubo recto", "Diámetro NPS (pulgadas):",
            6.0, 0.125, 36.0, 2
        )
        if not ok1:
            return
            
        items = ["SCH 10", "SCH 40", "SCH STD", "SCH 80", "SCH XS", "SCH 160", "SCH XXS"]
        schedule, ok2 = QtGui.QInputDialog.getItem(
            None, "Tubo recto", "Cédula:", items, 3, False
        )
        if not ok2:
            return
            
        length, ok3 = QtGui.QInputDialog.getDouble(
            None, "Tubo recto", "Longitud (mm):",
            1000.0, 10.0, 12000.0, 0
        )
        if not ok3:
            return
        
        pipe = make_pipe_segment(diameter, schedule, length)
        if pipe:
            FreeCAD.Console.PrintMessage(
                f"Pipe creado: NPS {diameter}\" SCH {schedule} L={length}mm\n"
            )

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None


class CmdElbow90:
    """Comando: Insertar codo 90° LR."""

    def GetResources(self):
        return {
            "Pixmap": "elbow_90",
            "MenuText": "Codo 90° LR",
            "ToolTip": "Inserta un codo 90° Long Radius (ASME B16.9)"
        }

    def Activated(self):
        FreeCAD.Console.PrintMessage("Codo 90°: pendiente implementar\n")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None


class CmdFlangeWN:
    """Comando: Insertar brida WN."""

    def GetResources(self):
        return {
            "Pixmap": "flange_wn",
            "MenuText": "Brida WN",
            "ToolTip": "Inserta una brida de cuello soldable (ASME B16.5)"
        }

    def Activated(self):
        FreeCAD.Console.PrintMessage("Brida WN: pendiente implementar\n")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None


class CmdGenerateIsometric:
    """Comando: Generar isométrico desde el modelo."""

    def GetResources(self):
        return {
            "Pixmap": "iso_generate",
            "MenuText": "Isométrico",
            "ToolTip": "Genera isométrico 2D del modelo de tubería seleccionado"
        }

    def Activated(self):
        FreeCAD.Console.PrintMessage("Isométrico: pendiente implementar\n")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None


class CmdGenerateBOM:
    """Comando: Generar lista de materiales."""

    def GetResources(self):
        return {
            "Pixmap": "bom",
            "MenuText": "Lista de Materiales (BOM)",
            "ToolTip": "Genera lista de materiales del modelo de tubería"
        }

    def Activated(self):
        FreeCAD.Console.PrintMessage("BOM: pendiente implementar\n")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None


# ===== Registro de comandos =====

class PipingHF_Commands:
    """Registra todos los comandos de PipingHF en FreeCAD."""

    @staticmethod
    def register():
        cmds = [
            ("PipingHF_PipeSegment", CmdPipeSegment()),
            ("PipingHF_Elbow90", CmdElbow90()),
            ("PipingHF_FlangeWN", CmdFlangeWN()),
            ("PipingHF_GenerateIsometric", CmdGenerateIsometric()),
            ("PipingHF_GenerateBOM", CmdGenerateBOM()),
        ]
        
        for name, cmd in cmds:
            FreeCADGui.addCommand(name, cmd)
        
        FreeCAD.Console.PrintMessage("PipingHF: 5 comandos registrados.\n")

    @staticmethod
    def get_toolbars():
        """Retorna las toolbars para InitGui.py."""
        return [
            {
                "name": "PipingHF - Tubería",
                "commands": [
                    "PipingHF_PipeSegment",
                    "PipingHF_Elbow90",
                    "PipingHF_FlangeWN",
                ]
            },
            {
                "name": "PipingHF - Documentos",
                "commands": [
                    "PipingHF_GenerateIsometric",
                    "PipingHF_GenerateBOM",
                ]
            },
        ]
