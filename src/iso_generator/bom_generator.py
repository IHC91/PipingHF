# SPDX-License-Identifier: LGPL-3.0-or-later
# PipingHF - Generador de Lista de Materiales (BOM)

import FreeCAD
import FreeCADGui


class BOMGenerator:
    """Genera lista de materiales desde el modelo 3D de tubería."""

    def __init__(self):
        self.bom_entries = []

    def generate(self, objects):
        """Recorre los objetos seleccionados y extrae el BOM.
        
        Args:
            objects: Lista de objetos FreeCAD
        
        Returns:
            Lista de dicts con: tipo, nps, schedule, material, cantidad, descripcion
        """
        self.bom_entries = []
        counts = {}

        for obj in objects:
            entry = self._inspect_object(obj)
            if entry:
                key = (entry["tipo"], entry["nps"], entry["schedule"], entry["material"])
                if key in counts:
                    counts[key]["cantidad"] += 1
                else:
                    counts[key] = entry
                    counts[key]["cantidad"] = 1

        self.bom_entries = sorted(
            counts.values(),
            key=lambda x: (x["tipo"], x["nps"])
        )
        return self.bom_entries

    def _inspect_object(self, obj):
        """Inspecciona un objeto FreeCAD y extrae info para BOM."""
        entry = {
            "tipo": "Desconocido",
            "nps": "-",
            "schedule": "-",
            "material": "-",
            "cantidad": 0,
            "descripcion": obj.Label,
            "largo_mm": 0,
        }

        # PipeSegment
        if hasattr(obj, "Diameter") and hasattr(obj, "Schedule"):
            entry["tipo"] = "Tubería recta"
            entry["nps"] = f'{obj.Diameter:.1f}"'
            entry["schedule"] = obj.Schedule
            entry["material"] = getattr(obj, "Material", "-")
            entry["largo_mm"] = getattr(obj, "Length", 0)
            entry["descripcion"] = f'Tubo {obj.Diameter:.1f}" SCH {obj.Schedule} L={entry["largo_mm"]:.0f}mm'

        # Elbow90
        elif hasattr(obj, "Angle") and hasattr(obj, "Radius"):
            entry["tipo"] = "Codo 90° LR"
            entry["nps"] = f'{getattr(obj, "Diameter", 0):.1f}"'
            entry["schedule"] = getattr(obj, "Schedule", "-")
            entry["descripcion"] = (
                f'Codo 90° LR {getattr(obj, "Diameter", 0):.1f}" '
                f'SCH {getattr(obj, "Schedule", "-")} '
                f'R={getattr(obj, "Radius", 0):.0f}mm'
            )

        # FlangeWN
        elif hasattr(obj, "Class") and hasattr(obj, "BoltHoles"):
            entry["tipo"] = "Brida WN"
            entry["nps"] = f'{getattr(obj, "Diameter", 0):.1f}"'
            entry["schedule"] = f'Class {getattr(obj, "Class", "-")}'
            entry["descripcion"] = (
                f'Brida Weld Neck {getattr(obj, "Diameter", 0):.1f}" '
                f'Class {getattr(obj, "Class", "-")} '
                f'{getattr(obj, "BoltHoles", 0)} agujeros'
            )

        return entry

    def show_bom(self, bom):
        """Muestra el BOM en una ventana de FreeCAD."""
        if not bom:
            FreeCAD.Console.PrintMessage("BOM vacío: no se encontraron componentes.\n")
            return

        try:
            from PySide import QtGui, QtWidgets

            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle("Lista de Materiales - PipingHF")
            dialog.resize(700, 400)

            layout = QtWidgets.QVBoxLayout(dialog)

            # Tabla
            table = QtWidgets.QTableWidget(len(bom), 6, dialog)
            table.setHorizontalHeaderLabels([
                "Tipo", "NPS", "Schedule", "Material", "Cant.", "Descripción"
            ])
            table.setAlternatingRowColors(True)

            for i, entry in enumerate(bom):
                table.setItem(i, 0, QtWidgets.QTableWidgetItem(entry["tipo"]))
                table.setItem(i, 1, QtWidgets.QTableWidgetItem(entry["nps"]))
                table.setItem(i, 2, QtWidgets.QTableWidgetItem(entry["schedule"]))
                table.setItem(i, 3, QtWidgets.QTableWidgetItem(entry["material"]))
                table.setItem(i, 4, QtWidgets.QTableWidgetItem(str(entry["cantidad"])))
                desc = entry["descripcion"]
                if entry["largo_mm"] > 0:
                    desc += f' | {entry["largo_mm"]:.0f} mm'
                table.setItem(i, 5, QtWidgets.QTableWidgetItem(desc))

            table.resizeColumnsToContents()
            layout.addWidget(table)

            # Botón para copiar/csv
            btn_layout = QtWidgets.QHBoxLayout()

            close_btn = QtWidgets.QPushButton("Cerrar")
            close_btn.clicked.connect(dialog.close)

            export_btn = QtWidgets.QPushButton("Exportar CSV")
            export_btn.clicked.connect(lambda: self._export_csv(bom))

            btn_layout.addWidget(export_btn)
            btn_layout.addWidget(close_btn)
            layout.addLayout(btn_layout)

            dialog.exec_()

        except Exception as e:
            # Fallback: imprimir en consola
            FreeCAD.Console.PrintMessage("\n=== LISTA DE MATERIALES ===\n")
            FreeCAD.Console.PrintMessage(
                f"{'Tipo':20s} {'NPS':8s} {'SCH':10s} {'Cant':6s} {'Descripción'}\n"
            )
            FreeCAD.Console.PrintMessage("-" * 70 + "\n")
            for entry in bom:
                FreeCAD.Console.PrintMessage(
                    f"{entry['tipo']:20s} {entry['nps']:8s} "
                    f"{entry['schedule']:10s} {str(entry['cantidad']):6s} "
                    f"{entry['descripcion']}\n"
                )
            FreeCAD.Console.PrintMessage("=" * 70 + "\n")

    def _export_csv(self, bom, filepath=None):
        """Exporta BOM a CSV."""
        if not filepath:
            from PySide import QtGui
            filepath, _ = QtGui.QFileDialog.getSaveFileName(
                None, "Guardar BOM", "bom_pipinghf.csv", "CSV (*.csv)"
            )
        
        if not filepath:
            return

        import csv
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Tipo", "NPS", "Schedule", "Material", "Cantidad", "Descripción", "Largo (mm)"])
            for entry in bom:
                writer.writerow([
                    entry["tipo"], entry["nps"], entry["schedule"],
                    entry["material"], entry["cantidad"],
                    entry["descripcion"], entry["largo_mm"]
                ])
        
        FreeCAD.Console.PrintMessage(f"BOM exportado: {filepath}\n")


def generate_bom():
    """Genera BOM para los objetos seleccionados."""
    doc = FreeCAD.ActiveDocument
    if not doc:
        FreeCAD.Console.PrintError("No hay documento abierto.\n")
        return

    sel = FreeCADGui.Selection.getSelection()
    if not sel:
        FreeCAD.Console.PrintError("Seleccioná objetos para generar BOM.\n")
        return

    gen = BOMGenerator()
    bom = gen.generate(sel)
    gen.show_bom(bom)
    return bom
