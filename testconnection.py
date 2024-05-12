import pyodbc
database = 'danadb'
cursor = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=localhost;"
                      "Database=bon;"
                      "Trusted_Connection=yes;")

cur = cursor.cursor()
print(cur.execute("""SELECT name FROM sys.tables""").fetchall())


def detect_driver():
    driver_name = ''
    driver_names = [x for x in pyodbc.drivers() if x.endswith('SQL Server')]
    print(driver_names)
    if driver_names:
        driver_name = driver_names[0]

    if driver_name:
        conn_str = 'DRIVER={}; ...'.format(driver_name)

    else:
        print('(No suitable driver found. Cannot connect. please install driver 17 or 18.)')

    return driver_names
detect_driver()

