# Implementation Plan: PipingHF v0.1.0

## Overview

Workbench de FreeCAD para diseño 3D de tuberías con generación automática de isométricos, BOM, spools y soldaduras. Partimos de la base de Quetzal (Dodo fork), adaptando frames → piping routing, cut_list → BOM/spools, isométricos de vigas → isométricos de tubería.

## Architecture Decisions

- **Formato:** Workbench FreeCAD con pestaña propia (Init.py + InitGui.py)
- **Base:** Quetzal v1.8.9 (fork de Dodo) — reusamos sistema de comandos, features, forms, tablas dimensionales
- **Componentes paramétricos:** Part::FeaturePython, catálogo dimensional vía CSV (ya existente en tablez/)
- **Routing:** Adaptar CFrame.py (beam routing) → CRoute.py (pipe routing con fittings)
- **Isométricos:** Adaptar quetzal_isometric.py (proyección de vigas) → proyección de línea de tubería
- **BOM/Soldaduras/Spools:** Adaptar cut_list/ → bom_generator/, spool_generator/, weld_table.py

## Task List

### Phase 1: Fundación — Adaptar Quetzal a PipingHF

- [ ] **Task 1: Rebranding base** — Iconos, tooltips, InitGui.py con comandos reales de piping
- [ ] **Task 2: Comandos de piping** — Registrar comandos FreeCAD: Insertar tubería, Insertar codo, etc.
- [ ] **Task 3: FeaturePipe** — FeaturePython paramétrico para tramo recto con diámetro/cédula/longitud

### Checkpoint: Fundación
- [ ] InitGui.py carga sin errores en FreeCAD
- [ ] Toolbar con botones de piping visibles
- [ ] FeaturePipe crea un tubo 3D parametrizable

### Phase 2: Motor de Routing

- [ ] **Task 4: CRoute** — Adaptar CFrame.py: ruteo punto a punto con pipe + fittings automáticos
- [ ] **Task 5: Catálogo dimensional** — Pipe schedule API (ASME B36.10), soporte OD/wall desde tablez/
- [ ] **Task 6: Comandos de fittings** — Insertar codo, brida, tee, reductor, válvula (desde shapez/)

### Checkpoint: Routing
- [ ] Ruta de 3 puntos genera: tubo + codo + tubo
- [ ] Fittings se insertan manualmente entre tramos
- [ ] Catálogo devuelve OD/wall correctos para SCH 40/80/160

### Phase 3: Isométricos & Documentos

- [ ] **Task 7: IsoGenerator** — Adaptar quetzal_isometric.py → proyectar línea de tubería en 2D con símbolos
- [ ] **Task 8: Dimensionado** — Cotas automáticas en el isométrico (longitudes, centros, elevaciones)
- [ ] **Task 9: BOM** — Lista de materiales desde el modelo: fittings, cantidades, NPS, SCH
- [ ] **Task 10: Tabla de soldaduras** — Identificar uniones entre fittings y generar tabla
- [ ] **Task 11: Spool splitting** — Dividir línea numerando spools

### Checkpoint: Isométricos
- [ ] Isométrico 2D generado desde modelo 3D simple
- [ ] BOM exportable con cantidades y descripciones
- [ ] Spool numerado y dibujado

### Phase 4: Integración & Polish

- [ ] **Task 12: UI Panels** — Task panels para routing, inserción de componentes, config de isométrico
- [ ] **Task 13: Exportación** — Exportar isométrico a SVG, DXF, PDF
- [ ] **Task 14: Tests** — pytest para lógica de routing, catálogo, BOM
- [ ] **Task 15: Ejemplos** — Demo: línea simple con fittings e isométrico

### Checkpoint: Final
- [ ] Flujo completo: modelar 3D → isométrico → BOM → soldaduras → spool
- [ ] Tests >80% en lógica pura
- [ ] Ejemplo funcional

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| API de FreeCAD cambia entre versiones | Medium | Apuntar a FreeCAD 1.0+, testear en la versión instalada de Iván |
| Isométricos de tubería son más complejos que de vigas | High | Empezar con proyección ortogonal simple, luego añadir simbología |
| Integración con Quetzal features es frágil | Medium | Mantener Quetzal como submodule o referencia, no modificar su código |
| Catálogo dimensional incompleto en tablez/ | Low | Ya tiene pipe schedules, flanges, elbows - completar sobre la marcha |

## Open Questions

- ¿FreeCAD de escritorio o también versión portable? → Preguntar a Iván
- ¿Versión de FreeCAD instalada? → Verificar
