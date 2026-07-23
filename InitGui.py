# SPDX-License-Identifier: LGPL-3.0-or-later
# PipingHF — Workbench de FreeCAD para diseño 3D de tuberías
# Basado en Quetzal/Dodo. No modifica archivos de Quetzal.

import FreeCAD
import FreeCADGui
from FreeCADGui import Workbench

Log = FreeCAD.Console.PrintLog


class PipingHFWorkbench(Workbench):
    """PipingHF: Diseño 3D de tuberías con isométricos, BOM y spools."""

    def __init__(self):
        self.__class__.MenuText = "PipingHF"
        self.__class__.ToolTip = (
            "PipingHF — Diseño 3D de tuberías con isométricos, BOM, spools y soldaduras"
        )

    def Initialize(self):
        """Called when workbench is first activated."""
        Log("Loading PipingHF workbench...\n")

        # Importar y registrar comandos
        from src.core.piping_commands import PipingHF_Commands
        PipingHF_Commands.register()

        # Crear toolbars
        from PySide import QtCore
        QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP

        # Toolbar: Tubería
        pipe_tools = [
            "PipingHF_PipeSegment",
            "PipingHF_Elbow90",
            "PipingHF_FlangeWN",
        ]
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Tubería"), pipe_tools)

        # Toolbar: Documentos
        doc_tools = [
            "PipingHF_GenerateIsometric",
            "PipingHF_GenerateBOM",
        ]
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Documentos"), doc_tools)

        Log("PipingHF workbench loaded: 5 commands, 2 toolbars.\n")

    def GetClassName(self):
        return "Gui::PythonWorkbench"


FreeCADGui.addWorkbench(PipingHFWorkbench)
