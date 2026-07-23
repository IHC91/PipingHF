# SPDX-License-Identifier: LGPL-3.0-or-later
# PipingHF - Generador de isométricos 2D desde modelo 3D

import math
import FreeCAD
import FreeCADGui
import Part
from FreeCAD import Vector, Placement


class IsoGenerator:
    """Genera isométricos 2D desde un modelo 3D de tubería.
    
    Toma un grupo o selección de objetos y genera:
    - Proyección 2D (isométrica)
    - Cotas automáticas
    - Lista de componentes
    """

    def __init__(self, doc):
        self.doc = doc
        self.scale = 1.0
        self.page_width = 420  # A3 horizontal (mm)
        self.page_height = 297

    def generate(self, objects, output_type="svg"):
        """Genera el isométrico a partir de una selección de objetos.
        
        Args:
            objects: Lista de objetos FreeCAD seleccionados
            output_type: "svg", "dxf", o "techdraw"
        """
        if not objects:
            FreeCAD.Console.PrintError("No hay objetos para generar isométrico.\n")
            return

        FreeCAD.Console.PrintMessage(
            f"Generando isométrico para {len(objects)} objetos...\n"
        )

        # Proyectar objetos a 2D usando proyección isométrica
        vertices_2d = []
        edges_2d = []
        labels = []

        for obj in objects:
            if hasattr(obj, "Shape") and obj.Shape:
                self._project_shape(obj.Shape, vertices_2d, edges_2d, labels, obj.Label)

        # Si hay TechDraw disponible, generar página
        try:
            self._generate_techdraw(objects, vertices_2d, edges_2d, labels)
        except Exception as e:
            FreeCAD.Console.PrintWarning(
                f"No se pudo generar TechDraw: {e}. "
                f"Generando SVG inline...\n"
            )
            # Fallback: exportar SVG
            self._generate_svg_fallback(objects)

    def _project_shape(self, shape, vertices, edges, labels, label_name):
        """Proyecta una forma 3D a un plano 2D usando proyección isométrica."""
        for vertex in shape.Vertexes:
            p = vertex.Point
            # Proyección isométrica: x' = (x - z) * cos(30), y' = (x + z) * sin(30) - y
            iso_x = (p.x - p.z) * 0.866  # cos(30)
            iso_y = (p.x + p.z) * 0.5 - p.y  # sin(30) = 0.5
            vertices.append((iso_x, iso_y))

        for edge in shape.Edges:
            for vertex in edge.Vertexes:
                p = vertex.Point
                iso_x = (p.x - p.z) * 0.866
                iso_y = (p.x + p.z) * 0.5 - p.y
                vertices.append((iso_x, iso_y))

            if len(edge.Vertexes) >= 2:
                p1 = edge.Vertexes[0].Point
                p2 = edge.Vertexes[-1].Point
                iso_x1 = (p1.x - p1.z) * 0.866
                iso_y1 = (p1.x + p1.z) * 0.5 - p1.y
                iso_x2 = (p2.x - p2.z) * 0.866
                iso_y2 = (p2.x + p2.z) * 0.5 - p2.y
                edges_2d.append(((iso_x1, iso_y1), (iso_x2, iso_y2)))

        labels.append((label_name, vertices[-1] if vertices else (0, 0)))

    def _generate_techdraw(self, objects, vertices, edges, labels):
        """Genera una página de TechDraw con la proyección isométrica."""
        import TechDraw
        
        # Crear página
        page = self.doc.addObject("TechDraw::DrawPage", "IsoPage")
        template = self.doc.addObject(
            "TechDraw::DrawSVGTemplate", "Template"
        )
        template.Template = TechDraw.findTemplate(
            TechDraw.TEMPLATE_A3_Landscape
        ) or TechDraw.findTemplate("A3_Landscape.svg")
        page.Template = template

        # Crear vista del grupo de objetos
        group = self.doc.addObject("TechDraw::DrawViewGroup", "IsoView")
        group.addView(objects)
        page.addView(group)

        # Crear vista isométrica
        view = self.doc.addObject("TechDraw::DrawViewPart", "IsoView")
        view.Source = objects
        view.Direction = Vector(-1, -1, 1)  # Dirección isométrica
        view.X = self.page_width / 2
        view.Y = self.page_height / 2
        view.Scale = self.scale
        page.addView(view)

        # Agregar cotas para los bordes principales
        if edges:
            for i, (p1, p2) in enumerate(edges[:5]):  # Limitar a 5 cotas
                length = math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
                if length > 50:
                    dim = self.doc.addObject(
                        "TechDraw::DrawViewDimension", f"Dim_{i}"
                    )
                    dim.References2D = [(view, f"Edge{i+1}")]
                    dim.FormatSpec = f"{length:.0f}"
                    page.addView(dim)

        self.doc.recompute()
        FreeCAD.Console.PrintMessage(
            f"Isométrico generado en página: {page.Label}\n"
        )

    def _generate_svg_fallback(self, objects):
        """Genera isométrico como archivo SVG cuando TechDraw no está disponible."""
        import os
        
        svg_path = os.path.join(
            FreeCAD.ActiveDocument.TransientDir
            if hasattr(FreeCAD.ActiveDocument, 'TransientDir')
            else '/tmp',
            f"isometric_{FreeCAD.ActiveDocument.Label}.svg"
        )

        # SVG header
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{self.page_width}mm" height="{self.page_height}mm" '
            f'viewBox="0 0 {self.page_width} {self.page_height}">',
            '<g transform="translate(50,50)">'
        ]

        # Proyectar y dibujar cada objeto
        for obj in objects:
            if hasattr(obj, "Shape") and obj.Shape:
                shape = obj.Shape
                for edge in shape.Edges:
                    if len(edge.Vertexes) >= 2:
                        p1 = edge.Vertexes[0].Point
                        p2 = edge.Vertexes[-1].Point
                        # Proyección isométrica
                        x1 = (p1.x - p1.z) * 0.866 * self.scale + self.page_width/3
                        y1 = (p1.x + p1.z) * 0.5 * self.scale - p1.y * self.scale + self.page_height/3
                        x2 = (p2.x - p2.z) * 0.866 * self.scale + self.page_width/3
                        y2 = (p2.x + p2.z) * 0.5 * self.scale - p2.y * self.scale + self.page_height/3
                        lines.append(
                            f'<line x1="{x1:.1f}" y1="{y1:.1f}" '
                            f'x2="{x2:.1f}" y2="{y2:.1f}" '
                            f'stroke="black" stroke-width="0.5"/>'
                        )

        lines.append('</g></svg>')

        with open(svg_path, 'w') as f:
            f.write('\n'.join(lines))

        FreeCAD.Console.PrintMessage(
            f"Isométrico SVG generado: {svg_path}\n"
        )

        # Abrir en navegador para vista previa
        import subprocess
        try:
            subprocess.Popen(['xdg-open', svg_path])
        except Exception:
            pass


def generate_isometric(selection=None):
    """Función de acceso rápido para generar isométrico."""
    doc = FreeCAD.ActiveDocument
    if not doc:
        FreeCAD.Console.PrintError("No hay documento abierto.\n")
        return

    sel = selection or FreeCADGui.Selection.getSelection()
    if not sel:
        FreeCAD.Console.PrintError("Seleccioná objetos para generar isométrico.\n")
        return

    gen = IsoGenerator(doc)
    gen.generate(sel)
