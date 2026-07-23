# SPDX-License-Identifier: LGPL-3.0-or-later
# PipingHF — Workbench de FreeCAD para diseño 3D de tuberías

import os
import FreeCAD
import FreeCADGui
from FreeCADGui import Workbench

Log = FreeCAD.Console.PrintLog


class PipingHFWorkbench(Workbench):
    """PipingHF: Diseño 3D de tuberías con isométricos, BOM y spools."""

    def __init__(self):
        from pipinghf_config import TRANSLATIONSPATH, ICONPATH
        
        FreeCADGui.addIconPath(ICONPATH)
        
        self.__class__.MenuText = "PipingHF"
        self.__class__.ToolTip = (
            "PipingHF — Diseño 3D de tuberías con isométricos, BOM, spools y soldaduras"
        )
        self.__class__.Icon = os.path.join(ICONPATH, "pipinghf.svg")

    def Initialize(self):
        Log("Loading PipingHF workbench...\n")

        from src.core.piping_commands import PipingHF_Commands
        PipingHF_Commands.register()

        QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP

        pipe_tools = [
            "PipingHF_PipeSegment",
            "PipingHF_Elbow90",
            "PipingHF_FlangeWN",
        ]
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Tubería"), pipe_tools)

        doc_tools = [
            "PipingHF_GenerateIsometric",
            "PipingHF_GenerateBOM",
        ]
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Documentos"), doc_tools)

        Log("PipingHF: 5 comandos, 2 toolbars, iconos listos.\n")

    def GetClassName(self):
        return "Gui::PythonWorkbench"


FreeCADGui.addWorkbench(PipingHFWorkbench)
