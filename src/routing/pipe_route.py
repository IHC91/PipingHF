# SPDX-License-Identifier: LGPL-3.0-or-later
# PipingHF - Motor de routing de tuberías

"""
Sistema de routing para líneas de tubería.
Convierte una secuencia de puntos 3D en una línea completa
con tramos rectos + codos automáticos.
"""

import math
import FreeCAD
import FreeCADGui
import Part
from FreeCAD import Vector


class RoutePoint:
    """Punto de ruta con información de conexión."""

    def __init__(self, position, direction_before=None, direction_after=None):
        self.position = position  # Vector(x, y, z)
        self.dir_before = direction_before  # Vector dirección entrante
        self.dir_after = direction_after  # Vector dirección saliente
        self.has_elbow = False
        self.elbow_angle = 0.0
        self.component = None  # FeaturePython del fitting en este punto


class PipeRoute:
    """Línea de tubería definida por puntos de ruta."""

    def __init__(self, name="PipeRoute"):
        self.name = name
        self.points = []  # Lista de RoutePoint
        self.segments = []  # Lista de FeaturePython (tramos rectos)
        self.fittings = []  # Lista de FeaturePython (codos, tees, etc.)
        self.diameter = 6.0
        self.schedule = "SCH 80"
        self.material = "API 5L X52"

    def add_point(self, x, y, z):
        """Agrega un punto de ruta."""
        self.points.append(RoutePoint(Vector(x, y, z)))

    def add_points_from_list(self, coords_list):
        """Agrega múltiples puntos desde lista de (x,y,z)."""
        for x, y, z in coords_list:
            self.add_point(x, y, z)

    def calculate_directions(self):
        """Calcula las direcciones entre puntos consecutivos."""
        if len(self.points) < 2:
            return

        for i in range(len(self.points) - 1):
            p0 = self.points[i].position
            p1 = self.points[i + 1].position
            direction = p1.sub(p0)
            direction.normalize()

            self.points[i].dir_after = direction
            self.points[i + 1].dir_before = direction

    def calculate_elbows(self):
        """Calcula ángulos de codos en cada punto de ruta intermedio."""
        for i in range(1, len(self.points) - 1):
            p = self.points[i]
            if p.dir_before and p.dir_after:
                dot = p.dir_before.dot(p.dir_after)
                dot = max(-1.0, min(1.0, dot))
                angle = math.degrees(math.acos(dot))
                p.elbow_angle = 180.0 - angle
                p.has_elbow = abs(p.elbow_angle) > 1.0

    def build(self, doc=None):
        """Construye la línea de tubería completa en el documento de FreeCAD.
        
        Este método crea los objetos 3D (tramos + codos) y los agrupa.
        """
        if doc is None:
            doc = FreeCAD.ActiveDocument
        if doc is None:
            doc = FreeCAD.newDocument(self.name)

        self.calculate_directions()
        self.calculate_elbows()

        group = doc.addObject("App::DocumentObjectGroup", self.name)
        self.segments = []
        self.fittings = []

        # Crear tramos rectos entre puntos
        for i in range(len(self.points) - 1):
            p0 = self.points[i]
            p1 = self.points[i + 1]
            start = p0.position
            end = p1.position

            # Calcular vector y longitud
            vec = end.sub(start)
            length = vec.Length

            if length < 1.0:
                continue

            direction = vec
            direction.normalize()

            # Crear tramo recto
            pipe = self._create_pipe_segment(doc, start, direction, length, i)
            self.segments.append(pipe)
            group.addObject(pipe)

            # Crear codo en punto intermedio (excepto primero y último)
            if i > 0 and self.points[i].has_elbow:
                elbow = self._create_elbow(
                    doc, self.points[i], self.points[i - 1].dir_after, direction
                )
                self.fittings.append(elbow)
                group.addObject(elbow)

        doc.recompute()
        return group

    def _create_pipe_segment(self, doc, start, direction, length, index):
        """Crea un tramo recto de tubería."""
        from src.core.pipe_feature import PipeSegment, ViewProviderPipe
        
        obj = doc.addObject("Part::FeaturePython", f"Pipe_{index+1:03d}")
        PipeSegment(obj)
        ViewProviderPipe(obj.ViewObject)
        
        obj.Diameter = self.diameter
        obj.Schedule = self.schedule
        obj.Length = length
        obj.Material = self.material

        # Posicionar: el tubo se crea en origen, lo movemos
        # Calcular rotación para alinear con la dirección
        # El tubo se crea a lo largo del eje Z
        z_axis = Vector(0, 0, 1)
        
        if abs(direction.dot(z_axis)) < 0.999:
            cross = z_axis.cross(direction)
            cross.normalize()
            angle = math.degrees(math.acos(z_axis.dot(direction)))
            obj.Placement.Rotation = FreeCAD.Rotation(cross, angle)
        elif direction.z < 0:
            obj.Placement.Rotation = FreeCAD.Rotation(Vector(1, 0, 0), 180)

        # Mover al punto de inicio
        obj.Placement.Base = start

        return obj

    def _create_elbow(self, doc, point, dir_in, dir_out):
        """Crea un codo 3D en un punto de ruta."""
        obj = doc.addObject("Part::FeaturePython", f"Elbow_at_{point.position.x:.0f}_{point.position.y:.0f}")
        
        # Calcular radio del codo
        od, wall = self._get_dimensions()
        radius = 1.5 * od  # LR = 1.5 * OD
        
        # Crear geometría del codo: toroide de 90°
        angle = point.elbow_angle
        
        # Posicionar el codo en el punto
        obj.addProperty("App::PropertyFloat", "Angle", "Elbow", "Ángulo del codo (°)")
        obj.Angle = angle
        obj.addProperty("App::PropertyFloat", "Radius", "Elbow", "Radio del codo (mm)")
        obj.Radius = radius
        obj.addProperty("App::PropertyFloat", "PipeOD", "Elbow", "OD del tubo (mm)")
        obj.PipeOD = od
        
        obj.Proxy = self
        obj.Placement.Base = point.position
        
        return obj

    def _get_dimensions(self):
        """Obtiene OD y wall del catálogo."""
        from src.catalog.pipe_schedule import PipeCatalog
        return PipeCatalog.get_pipe_dimensions(self.diameter, self.schedule)

    def clear(self):
        """Limpia todos los objetos de la ruta del documento."""
        # TODO: implementar limpieza
        pass


def create_route_from_coords(coords, diameter=6.0, schedule="SCH 80"):
    """Función de alto nivel para crear una ruta desde coordenadas.
    
    Args:
        coords: Lista de tuplas (x, y, z)
        diameter: NPS en pulgadas
        schedule: Cédula
    
    Returns:
        PipeRoute con la línea construida en el documento activo.
    """
    route = PipeRoute(f"Route_{len(coords)}pts")
    route.diameter = diameter
    route.schedule = schedule
    route.add_points_from_list(coords)
    route.build()
    return route
