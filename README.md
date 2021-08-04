# Anonymity
'Anonymity' is an **Anonymous** board service

## How to run
1. Install Requirements for Anonymity
   ```bash
   pip intall -r requirements.txt
   ```

2. Set Database connection URL
   ```bash
   export anonymity_sql='mysql://<id>:<password>@<host>:<port>/<db name>'
   ```

3. Create Database Table
   ```bash
   flask db upgrade
   ```

4. Set Redis connection URL
   ```bash
   export anonymity_redis='redis://:<password>@<host>:<port>/<id>'
   ```

5. Launch Server
   ```bash
   python launch.py --set-port <port>
   ```

## CLI Tools
### admin.py
```yaml
description: Admin token manager
options:
   --show   : show all admin sessions
   --create : create new one-time token
   --logout : delete all login sessions
```

### launch.py
```yaml
description: Server Launcher
options:
   --set-port PORT : set the port number to run the waitress server
```

### table.py
```yaml
description: Table manager
options:
   --show   : show all tables
   --add    : add new table
   --edit   : edit table data
   --delete : delete table
```

### redis_clear.py
```yaml
description: Delete All Item from Redis Server!
```
