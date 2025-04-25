import oracledb
def get_connection():
    oracledb.init_oracle_client(lib_dir=r"C:\oraclexe\instantclient-basic-windows.x64-19.26.0.0.0dbru\instantclient_19_26")  

    dsn = oracledb.makedsn("localhost", 1521, sid="XE")
    connection = oracledb.connect(
        user="cricket123",
        password="123",
        dsn=dsn
    )

    return connection
