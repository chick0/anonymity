# Anonymity
'Anonymity' is an **Anonymous** board service

## How to run?
1. Install requirements
   ```
   $ pip intall -r requirements.txt
   ```
2. Set Database connection URL
   ```
   $ export anonymity_sql='mysql://<id>:<password>@<host>:<port>/<db name>'
   ```
3. do database migration
   ```
   $ flask db upgrade
   ```
4. Set Redis connection URL
   ```
   $ export anonymity_redis='redis://:<password>@<host>:<port>/<id>'
   ```
4. Launch Server
   ```
   $ python launch.py --port <port default:8082>
   ```
