brew install mariadb

docker run -e DOLT_ROOT_PASSWORD=secret2 -e DOLT_ROOT_HOST=% -p 3307:3306 dolthub/dolt-sql-server:latest

# run docker with persistent database
docker run -e DOLT_ROOT_PASSWORD=secret2 -e DOLT_ROOT_HOST=% -v ~/NSRI-Dolt/FastAPI/dolt:/var/lib/dolt/edb -p 3307:3306 dolthub/dolt-sql-server:latest

mysql --host 0.0.0.0 -P 3307 -u root --password=secret2

# port out database to store for future


# create and use the edb if it isn't there already
create database edb;
show tables;
use edb;

streamlit run dolt_streamlit.py

fastapi dev dolt_server.py

