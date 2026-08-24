# Actualización a PC Guardian Ubuntu 2.4.9

1. Conserve su `config/config.yaml` anterior solo como referencia.
2. Use el nuevo `config/config.yaml` y vuelva a colocar el token API mediante:

   ```bash
   export ZABBIX_API_TOKEN='TOKEN_REAL'
   ```

   o escribiéndolo únicamente en su `config/config.yaml` local.
3. Reinstale/actualice el entorno:

   ```bash
   ./scripts/install.sh
   source pc-guardian-ubuntu-env/bin/activate
   ```

4. Valide:

   ```bash
   ./scripts/validate_project.sh
   ```

5. Sincronice Zabbix:

   ```bash
   python zabbix/provisioning/provision.py
   ```

6. Ejecute:

   ```bash
   python main.py
   ```

La versión 2.4.9 no contiene motor de acciones, terminación de procesos ni remediación automática.
