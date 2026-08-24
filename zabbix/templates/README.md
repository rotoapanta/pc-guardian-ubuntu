# Templates Zabbix

Desde PC Guardian Ubuntu v2.4.9, la **fuente autoritativa** del template es el
provisionamiento API ubicado en `zabbix/provisioning/`.

No se incluye un export YAML estático porque la lista de items de procesos se
genera a partir de `watchlist`, y mantener un YAML duplicado provocaba deriva
entre el código y Zabbix.

Para crear o sincronizar el template:

```bash
python zabbix/provisioning/provision.py
```
