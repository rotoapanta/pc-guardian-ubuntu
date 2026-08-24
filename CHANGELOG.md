# Changelog

## 2.4.9 - 2026-08-24

### Consolidación y limpieza

- PC Guardian queda formalmente limitado a diagnóstico y monitoreo de solo lectura.
- Eliminados restos de Actions/remediación y cualquier referencia de packaging relacionada.
- Eliminado el template YAML obsoleto; el provisionamiento API pasa a ser la fuente autoritativa.
- Actualizados VERSION, banner, configuración, FastAPI y metadata del paquete a 2.4.9.
- Eliminados del paquete el entorno virtual, logs, incidentes, `__pycache__` y `*.egg-info`.
- Token API reemplazado por `CHANGE_ME` y soporte para `ZABBIX_API_TOKEN` por variable de entorno.
- Logger consolidado: niveles estándar + `SUCCESS`; eliminado el nivel `ACTION`.
- Rutas de configuración, logs e incidentes resueltas desde la raíz del proyecto.
- Manejo de excepciones afinado en PSI, temperaturas, incidentes e i915.
- Mantiene unidades base para memoria/disco (`B`) y throughput (`Bps`).
- Mantiene el estado Zabbix `PENDING → OK/ERROR`.
- Armonizados umbrales locales de swap/PSI para reducir falsos positivos.
- Provisionamiento Zabbix conserva idempotencia para Items, Triggers y Graphs.
- Tests actualizados a las keys actuales y añadidas pruebas de conteo, unidades y modo read-only.
- Añadido `scripts/validate_project.sh` para compileall + pytest + ruff.

## 2.3.0 - 2026-08-20

- Arquitectura modular inicial.
- Integración Zabbix Sender y aprovisionamiento API.
- Diagnóstico D-state/i915, PSI, temperaturas y evidencia de incidentes.
