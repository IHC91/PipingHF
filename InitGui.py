# SPDX-License-Identifier: LGPL-3.0-or-later

import os
import sys

import FreeCAD
import FreeCADGui
from FreeCADGui import ActiveDocument, Workbench


Log = FreeCAD.Console.PrintLog
Msg = FreeCAD.Console.PrintMessage


class PipingHFWorkbench(Workbench):
    def __init__(self):
        from pipinghf_config import TRANSLATIONSPATH, ICONPATH

        # Add translations path
        FreeCADGui.addLanguagePath(TRANSLATIONSPATH)
        FreeCADGui.updateLocale()

        self.__class__.MenuText = FreeCAD.Qt.translate("Workbench", "PipingHF")
        self.__class__.ToolTip = FreeCAD.Qt.translate(
            "Workbench",
            "PipingHF — Diseño 3D de tuberías con generación automática de "
            "isométricos, BOM, spools y soldaduras. Basado en Quetzal/Dodo.",
        )
        self.__class__.Icon = os.path.join(ICONPATH, "pipinghf.svg")
        FreeCADGui.addIconPath(ICONPATH)

    try:
        import DraftSnap
    except Exception:
        import draftguitools.gui_snapper as DraftSnap

    if not hasattr(FreeCADGui, "Snapper"):
        FreeCADGui.Snapper = DraftSnap.Snapper()

    v = sys.version_info[0]
    if v < 3:
        FreeCAD.Console.PrintWarning(
            "PipingHF is written for Py3 and Qt5\n You may experience mis-behaviuors\n"
        )

    def Initialize(self):
        """
        This function is called at the first activation of the workbench,
        here is the place to import all the commands.
        """
        QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP
        import CUtils  # noqa: F401

        self.utilsList = [
            "PipingHF_SelectSolids",
            "PipingHF_QueryModel",
            "PipingHF_MoveWorkPlane",
            "PipingHF_OffsetWorkPlane",
            "PipingHF_RotateWorkPlane",
            "PipingHF_HackedLine",
            "PipingHF_MoveHandle",
            "PipingHF_PressureLossCalculator",
        ]
        self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Utils"), self.utilsList)
        Log("Loading Utils: done\n")

        import CFrame  # noqa: F401

        self.frameList = [
            "PipingHF_Route",
            "PipingHF_RouteBranchManager",
            "PipingHF_InsertComponent",
            "PipingHF_SpinComponent",
            "PipingHF_Reverse",
            "PipingHF_Shift",
            "PipingHF_Pivot",
            "PipingHF_Level",
            "PipingHF_AlignEdge",
            "PipingHF_RotateJoin",
            "PipingHF_RemoveJoin",
            "PipingHF_EndJoin",
            "PipingHF_2PointsJoin",
            "PipingHF_3PointsJoin",
            "PipingHF_BeamJoin",
            "PipingHF_PolyLine",
            "PipingHF_Cleaner",
            "PipingHF_SectionEditor",
            "PipingHF_StandardizeRoute",
            "PipingHF_CreatePipe",
            "PipingHF_CreateElbow",
            "PipingHF_CreateTee",
            "PipingHF_CreateReducer",
            "PipingHF_CreateFlange",
            "PipingHF_CreateValve",
        ]
        self.appendToolbar(
            QT_TRANSLATE_NOOP("Workbench", "Piping"), self.frameList
        )
        Log("Loading Piping components: done\n")

        from cut_list.cut_list_commands import cutListCommand  # noqa: F401

        self.isoList = [
            "PipingHF_Isometric",
            "PipingHF_BOM",
            "PipingHF_WeldTable",
            "PipingHF_SpoolSplit",
            "PipingHF_ExportDXF",
            "PipingHF_ExportSVG",
            "PipingHF_ExportPDF",
        ]
        self.appendToolbar(
            QT_TRANSLATE_NOOP("Workbench", "Isometrics & Docs"), self.isoList
        )
        Log("Loading Isometrics tools: done\n")

        import CPipe  # noqa: F401

        self.pipeList = [
            "PipingHF_PipeLine",
            "PipingHF_PipeSegment",
            "PipingHF_Valve",
            "PipingHF_Support",
            "PipingHF_Annotate",
            "PipingHF_Dimension",
        ]
        self.appendToolbar(
            QT_TRANSLATE_NOOP("Workbench", "Line Components"), self.pipeList
        )
        Log("Loading Line Components: done\n")

        FreeCADGui.addCommand("PipingHF_Isometric", cutListCommand())
        FreeCADGui.addCommand("PipingHF_BOM", cutListCommand())

    def GetClassName(self):
        return "Gui::PythonWorkbench"


FreeCADGui.addWorkbench(PipingHFWorkbench)
