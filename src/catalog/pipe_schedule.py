# SPDX-License-Identifier: LGPL-3.0-or-later
# PipingHF - Catálogo dimensional de tubería y fittings

"""
Catálogo dimensional según estándares ASME/API.

Fuentes:
    - ASME B36.10M: Tubería de acero al carbón (welded y seamless)
    - ASME B16.5: Bridas y accesorios bridados (Class 150-2500)
    - ASME B16.9: Codos, tees, reductores (factory-made wrought steel buttwelding)
    - API 5L: Tubería para hidrocarburos
"""


class PipeCatalog:
    """Catálogo de dimensiones de tubería según ASME B36.10M."""

    # Diámetro exterior (mm) por NPS (pulgadas)
    OD = {
        0.125: 10.29, 0.25: 13.72, 0.375: 17.15, 0.5: 21.34,
        0.75: 26.67, 1.0: 33.40, 1.25: 42.16, 1.5: 48.26,
        2.0: 60.33, 2.5: 73.03, 3.0: 88.90, 3.5: 101.60,
        4.0: 114.30, 5.0: 141.30, 6.0: 168.28, 8.0: 219.08,
        10.0: 273.05, 12.0: 323.85, 14.0: 355.60, 16.0: 406.40,
        18.0: 457.20, 20.0: 508.00, 22.0: 558.80, 24.0: 609.60,
        26.0: 660.40, 28.0: 711.20, 30.0: 762.00, 32.0: 812.80,
        34.0: 863.60, 36.0: 914.40,
    }

    # Espesores de pared (mm) por NPS y Schedule
    WALL = {
        "SCH 5":   {1.5: 1.65, 2: 2.11, 2.5: 2.77, 3: 3.05, 4: 3.05,
                    5: 3.40, 6: 3.40, 8: 4.06, 10: 4.06, 12: 4.57},
        "SCH 10":  {0.5: 1.65, 0.75: 1.65, 1: 2.11, 1.25: 2.11, 1.5: 2.11,
                    2: 2.11, 2.5: 2.77, 3: 2.77, 4: 2.77, 5: 3.40,
                    6: 3.40, 8: 4.06, 10: 4.06, 12: 4.57},
        "SCH 20":  {1: 2.77, 1.25: 2.77, 1.5: 2.77, 2: 2.77, 2.5: 3.53,
                    3: 3.53, 4: 3.53, 5: 3.53, 6: 3.53, 8: 4.78,
                    10: 5.54, 12: 6.35},
        "SCH 30":  {2: 3.53, 2.5: 3.53, 3: 4.24, 4: 4.24, 5: 4.24,
                    6: 4.78, 8: 5.54, 10: 6.35, 12: 7.14},
        "SCH STD": {0.5: 2.77, 0.75: 2.77, 1: 3.38, 1.25: 3.56, 1.5: 3.68,
                    2: 3.91, 2.5: 5.16, 3: 5.49, 4: 6.02, 5: 6.55,
                    6: 7.11, 8: 8.18, 10: 9.27, 12: 10.31,
                    14: 9.53, 16: 9.53, 18: 9.53, 20: 9.53,
                    22: 9.53, 24: 9.53, 30: 9.53, 36: 9.53},
        "SCH 40":  {0.5: 2.77, 0.75: 2.77, 1: 3.38, 1.25: 3.56, 1.5: 3.68,
                    2: 3.91, 2.5: 5.16, 3: 5.49, 4: 6.02, 5: 6.55,
                    6: 7.11, 8: 8.18, 10: 9.27, 12: 10.31},
        "SCH XS":  {0.5: 3.73, 0.75: 3.91, 1: 4.55, 1.25: 4.85, 1.5: 5.08,
                    2: 5.54, 2.5: 7.01, 3: 7.62, 4: 8.56, 5: 9.53,
                    6: 10.97, 8: 12.70, 10: 15.09, 12: 17.48,
                    14: 11.10, 16: 11.10, 18: 11.10, 20: 12.70,
                    22: 12.70, 24: 12.70, 30: 12.70, 36: 12.70},
        "SCH 60":  {2: 4.78, 2.5: 5.16, 3: 6.35, 4: 6.35, 5: 7.14,
                    6: 7.62, 8: 8.74, 10: 9.53, 12: 10.31},
        "SCH 80":  {0.5: 3.73, 0.75: 3.91, 1: 4.55, 1.25: 4.85, 1.5: 5.08,
                    2: 5.54, 2.5: 7.01, 3: 7.62, 4: 8.56, 5: 9.53,
                    6: 10.97, 8: 12.70, 10: 15.09, 12: 17.48},
        "SCH 100": {3: 6.35, 4: 6.35, 5: 8.13, 6: 8.74, 8: 10.31,
                    10: 12.70, 12: 14.27},
        "SCH 120": {4: 8.56, 5: 10.97, 6: 11.13, 8: 14.27, 10: 17.48,
                    12: 19.05},
        "SCH 140": {4: 10.31, 5: 12.70, 6: 14.27, 8: 18.26, 10: 21.44,
                    12: 23.83},
        "SCH 160": {0.5: 4.78, 0.75: 5.56, 1: 6.35, 1.25: 7.14, 1.5: 7.14,
                    2: 8.74, 2.5: 10.16, 3: 11.13, 4: 13.49, 5: 15.88,
                    6: 18.26, 8: 23.01, 10: 28.45, 12: 33.32},
        "SCH XXS": {0.5: 7.47, 0.75: 7.82, 1: 9.09, 1.25: 9.70, 1.5: 10.16,
                    2: 11.07, 2.5: 14.02, 3: 15.24, 4: 17.12, 5: 19.05,
                    6: 21.95, 8: 25.40, 10: 30.18, 12: 34.93},
    }

    @classmethod
    def get_pipe_dimensions(cls, nps, schedule):
        """Retorna (OD_mm, wall_mm) para un NPS y Schedule dados.
        
        Args:
            nps: Diámetro nominal en pulgadas (float)
            schedule: Cédula (str, ej: "SCH 40", "SCH 80")
        
        Returns:
            Tuple[float, float]: (OD en mm, espesor de pared en mm)
        """
        od = cls.OD.get(nps)
        if od is None:
            # Buscar el NPS más cercano
            closest = min(cls.OD.keys(), key=lambda k: abs(k - nps))
            od = cls.OD[closest]
        
        walls = cls.WALL.get(schedule, cls.WALL["SCH 80"])
        wall = walls.get(nps)
        if wall is None:
            # Buscar valor más cercano disponible
            available = sorted(walls.keys())
            closest_nps = min(available, key=lambda k: abs(k - nps))
            wall = walls[closest_nps]
            # Si no hay cercano, default
            if wall is None:
                wall = 10.97  # Default SCH 80 NPS 6"
        
        return od, wall

    @classmethod
    def list_schedules(cls):
        """Lista los schedules disponibles."""
        return sorted(cls.WALL.keys())

    @classmethod
    def list_nps(cls):
        """Lista los NPS disponibles."""
        return sorted(cls.OD.keys())


class ElbowCatalog:
    """Catálogo de codos según ASME B16.9.
    
    Dimensión A = center-to-end (mm) para codos LR y SR.
    """

    # Center-to-end dimension (mm) — Codo 90° Long Radius
    A_LR_90 = {
        0.5: 38, 0.75: 38, 1: 38, 1.25: 38, 1.5: 38,
        2: 51, 2.5: 64, 3: 76, 3.5: 89, 4: 102,
        5: 127, 6: 152, 8: 203, 10: 254, 12: 305,
        14: 356, 16: 406, 18: 457, 20: 508, 22: 559,
        24: 610, 30: 762, 36: 914,
    }

    # Center-to-end dimension (mm) — Codo 90° Short Radius
    A_SR_90 = {
        0.5: 25, 0.75: 25, 1: 25, 1.25: 25, 1.5: 25,
        2: 38, 2.5: 51, 3: 64, 4: 76, 5: 102,
        6: 127, 8: 178, 10: 229, 12: 279, 14: 330,
        16: 381, 18: 432, 20: 483, 24: 584,
    }

    # Center-to-end dimension (mm) — Codo 45° LR
    A_LR_45 = {
        0.5: 19, 0.75: 19, 1: 22, 1.25: 25, 1.5: 29,
        2: 35, 2.5: 44, 3: 51, 4: 64, 5: 79,
        6: 95, 8: 127, 10: 159, 12: 190, 14: 222,
        16: 254, 18: 286, 20: 318, 24: 381,
    }

    @classmethod
    def get_center_to_end(cls, nps, angle=90, radius="LR"):
        """Retorna dimensión center-to-end (mm) para un codo."""
        if angle == 45:
            return cls.A_LR_45.get(nps, 95)
        elif radius == "SR":
            return cls.A_SR_90.get(nps, 127)
        else:
            return cls.A_LR_90.get(nps, 152)


class FlangeCatalog:
    """Catálogo de bridas según ASME B16.5.
    
    Dimensiones principales para bridas Weld Neck (WN):
    - OD: Diámetro exterior
    - t: Espesor
    - X: Hub diameter at base
    - H: Hub length
    - Bolt circle & holes (para BOM de pernos)
    """

    # Bridas Class 150 — Weld Neck (dimensiones en mm)
    WN_150 = {
        0.5: {"OD": 88.9, "t": 11.2, "X": 30.2, "H": 22.4, "BC": 60.3, "Holes": 4, "Bolt": "1/2"},
        0.75: {"OD": 98.6, "t": 12.7, "X": 38.1, "H": 25.4, "BC": 69.9, "Holes": 4, "Bolt": "1/2"},
        1: {"OD": 108.0, "t": 14.2, "X": 49.3, "H": 28.4, "BC": 79.4, "Holes": 4, "Bolt": "1/2"},
        1.25: {"OD": 117.5, "t": 15.7, "X": 59.2, "H": 31.8, "BC": 88.9, "Holes": 4, "Bolt": "1/2"},
        1.5: {"OD": 127.0, "t": 17.5, "X": 65.0, "H": 34.9, "BC": 98.4, "Holes": 4, "Bolt": "1/2"},
        2: {"OD": 152.4, "t": 19.1, "X": 78.0, "H": 38.1, "BC": 120.7, "Holes": 4, "Bolt": "5/8"},
        2.5: {"OD": 177.8, "t": 22.4, "X": 90.4, "H": 44.5, "BC": 139.7, "Holes": 4, "Bolt": "5/8"},
        3: {"OD": 190.5, "t": 23.9, "X": 108.0, "H": 47.8, "BC": 152.4, "Holes": 4, "Bolt": "5/8"},
        4: {"OD": 228.6, "t": 23.9, "X": 135.0, "H": 47.8, "BC": 190.5, "Holes": 8, "Bolt": "5/8"},
        5: {"OD": 254.0, "t": 23.9, "X": 164.0, "H": 47.8, "BC": 215.9, "Holes": 8, "Bolt": "3/4"},
        6: {"OD": 279.4, "t": 25.4, "X": 192.0, "H": 50.8, "BC": 241.3, "Holes": 8, "Bolt": "3/4"},
        8: {"OD": 342.9, "t": 28.6, "X": 246.0, "H": 57.2, "BC": 298.5, "Holes": 8, "Bolt": "3/4"},
        10: {"OD": 406.4, "t": 30.2, "X": 304.0, "H": 60.5, "BC": 361.9, "Holes": 12, "Bolt": "7/8"},
        12: {"OD": 482.6, "t": 31.8, "X": 365.0, "H": 63.5, "BC": 431.8, "Holes": 12, "Bolt": "7/8"},
    }

    # Bridas Class 300 — Weld Neck
    WN_300 = {
        0.5: {"OD": 95.2, "t": 14.2, "X": 30.2, "H": 22.4, "BC": 66.7, "Holes": 4, "Bolt": "1/2"},
        0.75: {"OD": 117.5, "t": 15.7, "X": 38.1, "H": 25.4, "BC": 82.6, "Holes": 4, "Bolt": "5/8"},
        1: {"OD": 123.8, "t": 17.5, "X": 49.3, "H": 28.4, "BC": 88.9, "Holes": 4, "Bolt": "5/8"},
        1.25: {"OD": 133.4, "t": 19.1, "X": 59.2, "H": 31.8, "BC": 98.4, "Holes": 4, "Bolt": "5/8"},
        1.5: {"OD": 155.6, "t": 20.6, "X": 65.0, "H": 34.9, "BC": 114.3, "Holes": 4, "Bolt": "3/4"},
        2: {"OD": 165.1, "t": 22.4, "X": 78.0, "H": 38.1, "BC": 127.0, "Holes": 8, "Bolt": "5/8"},
        2.5: {"OD": 190.5, "t": 25.4, "X": 90.4, "H": 44.5, "BC": 149.2, "Holes": 8, "Bolt": "3/4"},
        3: {"OD": 209.6, "t": 28.6, "X": 108.0, "H": 47.8, "BC": 168.3, "Holes": 8, "Bolt": "3/4"},
        4: {"OD": 254.0, "t": 31.8, "X": 135.0, "H": 50.8, "BC": 200.0, "Holes": 8, "Bolt": "3/4"},
        5: {"OD": 279.4, "t": 34.9, "X": 164.0, "H": 53.8, "BC": 235.0, "Holes": 8, "Bolt": "3/4"},
        6: {"OD": 317.5, "t": 36.5, "X": 192.0, "H": 57.2, "BC": 269.9, "Holes": 12, "Bolt": "3/4"},
        8: {"OD": 381.0, "t": 41.3, "X": 246.0, "H": 63.5, "BC": 330.2, "Holes": 12, "Bolt": "7/8"},
        10: {"OD": 444.5, "t": 47.6, "X": 304.0, "H": 69.9, "BC": 387.4, "Holes": 16, "Bolt": "1"},
        12: {"OD": 520.7, "t": 50.8, "X": 365.0, "H": 73.2, "BC": 450.9, "Holes": 16, "Bolt": "1"},
    }

    # Bridas Class 600 — Weld Neck (dimensiones clave)
    WN_600 = {
        0.5: {"OD": 95.2, "t": 14.2, "X": 30.2, "BC": 66.7, "Holes": 4, "Bolt": "1/2"},
        0.75: {"OD": 117.5, "t": 15.7, "X": 38.1, "BC": 82.6, "Holes": 4, "Bolt": "5/8"},
        1: {"OD": 123.8, "t": 17.5, "X": 49.3, "BC": 88.9, "Holes": 4, "Bolt": "5/8"},
        1.5: {"OD": 155.6, "t": 22.4, "X": 65.0, "BC": 114.3, "Holes": 4, "Bolt": "3/4"},
        2: {"OD": 165.1, "t": 25.4, "X": 78.0, "BC": 127.0, "Holes": 8, "Bolt": "5/8"},
        3: {"OD": 209.6, "t": 31.8, "X": 108.0, "BC": 168.3, "Holes": 8, "Bolt": "3/4"},
        4: {"OD": 273.1, "t": 38.1, "X": 135.0, "BC": 215.9, "Holes": 8, "Bolt": "7/8"},
        6: {"OD": 355.6, "t": 47.6, "X": 192.0, "BC": 292.1, "Holes": 12, "Bolt": "1"},
        8: {"OD": 419.1, "t": 55.6, "X": 246.0, "BC": 349.3, "Holes": 12, "Bolt": "1"},
        10: {"OD": 508.0, "t": 63.5, "X": 304.0, "BC": 431.8, "Holes": 16, "Bolt": "1"},
        12: {"OD": 558.8, "t": 66.7, "X": 365.0, "BC": 489.0, "Holes": 20, "Bolt": "1"},
    }

    CLASSES = {
        "150": WN_150,
        "300": WN_300,
        "600": WN_600,
    }

    @classmethod
    def get_flange_dimensions(cls, nps, flange_class="150", flange_type="WN"):
        """Retorna dimensiones de brida según ASME B16.5."""
        catalog = cls.CLASSES.get(flange_class, cls.WN_150)
        return catalog.get(nps)
