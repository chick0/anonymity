# Anonymity
'Anonymity' anon board service

## How to run?
1. Install requirements
   ```
   $ pip intall -r requirements.txt
   ```
2. Set Database connection URL
   ```
   mysql://<id>:<password>@<host>:<port>/<db name>
   ```
    - add to your 'Environment' key is 'anonymity_sql'
3. do database migration
   ```
   $ flask db upgrade
   ```
4. Set Redis connection URL
   ```
   redis://:<password>@<host>:<port>/<id>
   ```
    - add to your 'Environment' key is 'anonymity_redis'
4. Launch Server
   ```
   $ python launch.py --port <port default:8082>
   ```
