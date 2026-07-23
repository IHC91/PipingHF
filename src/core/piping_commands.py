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
    """Comando: Insertar codo 90° LR con geometría real."""

    def GetResources(self):
        return {
            "Pixmap": "elbow_90",
            "MenuText": "Codo 90° LR",
            "ToolTip": "Inserta un codo 90° Long Radius con geometría 3D (ASME B16.9)"
        }

    def Activated(self):
        from PySide import QtGui
        
        diameter, ok1 = QtGui.QInputDialog.getDouble(
            None, "Codo 90° LR", "Diámetro NPS (pulgadas):",
            6.0, 0.5, 36.0, 2
        )
        if not ok1:
            return
            
        items = ["SCH 40", "SCH 80", "SCH STD", "SCH XS", "SCH XXS", "SCH 160"]
        schedule, ok2 = QtGui.QInputDialog.getItem(
            None, "Codo 90° LR", "Cédula:", items, 1, False
        )
        if not ok2:
            return

        angle, ok3 = QtGui.QInputDialog.getDouble(
            None, "Codo 90° LR", "Ángulo (°):",
            90.0, 1.0, 90.0, 0
        )
        if not ok3:
            return

        from src.components.elbow_feature import make_elbow
        elbow = make_elbow(diameter, schedule, angle)
        if elbow:
            FreeCAD.Console.PrintMessage(
                f"Codo creado: NPS {diameter}\" {schedule} {angle}°\n"
            )

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None


class CmdFlangeWN:
    """Comando: Insertar brida WN con geometría real."""

    def GetResources(self):
        return {
            "Pixmap": "flange_wn",
            "MenuText": "Brida WN",
            "ToolTip": "Inserta una brida Weld Neck con geometría 3D (ASME B16.5)"
        }

    def Activated(self):
        from PySide import QtGui

        diameter, ok1 = QtGui.QInputDialog.getDouble(
            None, "Brida Weld Neck", "Diámetro NPS (pulgadas):",
            6.0, 0.5, 24.0, 2
        )
        if not ok1:
            return

        items = ["150", "300", "600"]
        cls, ok2 = QtGui.QInputDialog.getItem(
            None, "Brida Weld Neck", "Clase ASME:", items, 0, False
        )
        if not ok2:
            return

        from src.components.flange_feature import make_flange_wn
        flange = make_flange_wn(diameter, cls)
        if flange:
            FreeCAD.Console.PrintMessage(
                f"Brida WN creada: NPS {diameter}\" Class {cls}\n"
            )

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None


class CmdGenerateIsometric:
    """Comando: Generar isométrico 2D desde el modelo."""

    def GetResources(self):
        return {
            "Pixmap": "iso_generate",
            "MenuText": "Isométrico",
            "ToolTip": "Genera isométrico 2D del modelo de tubería seleccionado"
        }

    def Activated(self):
        from PySide import QtGui, QtCore
        from src.iso_generator.iso_generator import IsoGenerator
        
        doc = FreeCAD.ActiveDocument
        sel = FreeCADGui.Selection.getSelection()
        
        if not sel:
            QtGui.QMessageBox.warning(
                None, "Isométrico",
                "Seleccioná un grupo o un tubo para generar el isométrico."
            )
            return

        gen = IsoGenerator(doc)
        gen.generate(sel)

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None


class CmdGenerateBOM:
    """Comando: Generar lista de materiales."""

    def GetResources(self):
        return {
            "Pixmap": "bom",
            "MenuText": "Lista de Materiales (BOM)",
            "ToolTip": "Genera lista de materiales del modelo de tubería seleccionado"
        }

    def Activated(self):
        from PySide import QtGui
        from src.iso_generator.bom_generator import BOMGenerator
        
        doc = FreeCAD.ActiveDocument
        sel = FreeCADGui.Selection.getSelection()
        
        if not sel:
            QtGui.QMessageBox.warning(
                None, "BOM",
                "Seleccioná objetos del modelo para generar el BOM."
            )
            return

        gen = BOMGenerator()
        bom = gen.generate(sel)
        gen.show_bom(bom)

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
