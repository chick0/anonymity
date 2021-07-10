# Anonymity
'Anonymity' anon board service

## How to run?
1. Install requirements
   ```
   pip intall -r requirements.txt
   ```
2. Set Database connection URL
   ```
   mysql://<id>:<password>@localhost:<port>/<db name>
   ```
   - add to your 'Environment' key is 'anonymity_sql'
3. do database migration
   ```
   flask db upgrade
   ```
4. Launch Server
   ```
   launch.py --port <port default:8082>
   ```
