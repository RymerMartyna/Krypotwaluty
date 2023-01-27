import psycopg2
import os

# pg_user = os.environ["POSTGRES_USER"]
# pg_password = os.environ["POSTGRES_PASSWORD"]
# pg_database = os.environ["POSTGRES_DATABASE"]
# pg_host = "postgres"


pg_user = "admin"
pg_password = "password"
pg_database = "default"
pg_host = "postgres"

#lista pythonowa, do ktorej beda dodane maile: 




print(select_from_db())