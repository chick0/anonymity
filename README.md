# Anonymity
'Anonymity' is an **Anonymous** board service

## How to run
1. Install requirements
   ```bash
   pip intall -r requirements.txt
   ```

2. Set Database connection URL
   ```bash
   export anonymity_sql='mysql://<id>:<password>@<host>:<port>/<db name>'
   ```

3. do database migration
   ```bash
   flask db upgrade
   ```

4. Set Redis connection URL
   ```bash
   export anonymity_redis='redis://:<password>@<host>:<port>/<id>'
   ```

5. Launch Server
   ```bash
   python launch.py --port <port default:8082>
   ```

## CLI Tools
### admin.py
```yaml
options:
   --show   : show all admin sessions
   --create : create new one-time token
   --logout : delete all login sessions
```

### launch.py
```yaml
options:
   --set-port PORT : set the port number to run the waitress server
   --no-cron-job   : disable cron job working with multiprocessing 
```

### table.py
```yaml
options:
   --show   : show all tables
   --add    : add new table
   --edit   : edit table data
   --delete : delete table
```
