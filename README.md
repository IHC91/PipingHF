# PipingHF 🏗️🔧

**FreeCAD Workbench para diseño 3D de tuberías industriales**

Workbench nativo de FreeCAD para modelado 3D de tuberías con generación automática de isométricos, BOM, tablas de soldaduras y despiece de spools.

> Basado en **[Quetzal](https://github.com/EdgarJRobles/quetzal)** (fork de Dodo workbench) — LGPL-3.0

## Capacidades

| Módulo | Descripción |
|--------|-------------|
| 🛤️ **Pipe Routing** | Ruteo 3D de líneas con fittings paramétricos |
| 🔧 **Componentes** | Tubería recta, codos LR/SR, tees, reductores, bridas, válvulas, empaques |
| 📏 **Catálogo** | Dimensiones estándar: ASME B36.10, B16.5, B16.9, API 5L |
| 📐 **Isométrico 2D** | Proyección automática con dimensionado |
| 📊 **BOM** | Lista de materiales desde el modelo 3D |
| 🔥 **Soldaduras** | Tabla de cortes y uniones soldadas |
| 🔢 **Spools** | División y numeración de spools para fabricación |

## Instalación

```bash
# Clonar en la carpeta Mod de FreeCAD
cd ~/.local/share/FreeCAD/Mod/
git clone https://github.com/IHC91/PipingHF.git
```

Reiniciar FreeCAD → Seleccionar **PipingHF** del selector de workbenches.

## Estructura

```
PipingHF/
├── Init.py / InitGui.py       # Registro del workbench
├── package.xml                 # Metadatos para Addon Manager
├── pipinghf_config.py          # Configuración global
├── CFrame.py                   # Sistema de frames → routing
├── CPipe.py                    # Tubería paramétrica
├── CUtils.py                   # Utilidades
├── fCmd.py / fFeatures.py      # Comandos y features paramétricos
├── cut_list/                   # → BOM / spool generator
├── shapez/                     # Componentes paramétricos
├── tablez/                     # Tablas y reportes
├── dialogz/                    # Diálogos y task panels
├── src/
│   ├── pipe_routing/           # Motor de ruteo
│   ├── components/             # Fittings + catálogo dimensional
│   ├── iso_generator/          # Isométricos, BOM, soldaduras
│   └── ui/                     # Interfaz de usuario
├── tests/                      # Tests unitarios
└── docs/                       # Documentación
```

## Licencia

LGPL-3.0-or-later
