from parser import OracleToMySQLConverter

if __name__ == "__main__":
    with open("oracle.sql", "r") as f:
        oracle_sql = f.read()

    converter = OracleToMySQLConverter()
    mysql_sql = converter.convert(oracle_sql)

    with open("mysql.sql", "w") as f:
        f.write(mysql_sql)