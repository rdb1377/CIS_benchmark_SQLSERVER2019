import csv
import pyodbc


class Benchmarks:
    def __init__(self , cnxn):
        self.cnxn = cnxn
        if self.cnxn.authmethod == 'Windows Authetication':
            # self.connectionstring = pyodbc.connect(
            #     'DRIVER={' + self.cnxn.driver + '};SERVER=' + self.cnxn.servername +  ';Trusted_Connection={yes} ;TrustServerCertificate={yes};  NeedODBCTypesOnly=1')

            self.connectionstring = pyodbc.connect("Driver={" + self.cnxn.driver + "};"
                      "Server="+ self.cnxn.servername +";"
                      "Database=bon;"
                      "Trusted_Connection=yes;"
                      "TrustServerCertificate=yes;"
                      "NeedODBCTypesOnly=1")

            self.connectionstring = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=localhost;"
                      "Database=bon;"
                      "Trusted_Connection=yes;")


        elif self.cnxn.authmethod == 'SQL Server Authetication':
            self.connectionstring = pyodbc.connect(
                'DRIVER={' + self.cnxn.driver + '};SERVER=' + self.cnxn.servername +  ';Database = {Mokhaberat} ;UID=' + self.cnxn.username + ';PWD=' + self.cnxn.password)

    def buildCNXN(self , database):
        if (database =='') :
            database = 'master'

        if self.cnxn.authmethod== 'Windows Authetication':
            connectionstring = pyodbc.connect("Driver={" + self.cnxn.driver + "};"
                              "Server=" + self.cnxn.servername + ";"
                              "Database="+database+";"
                              "Trusted_Connection=yes;"
                              "TrustServerCertificate=yes;"
                              "NeedODBCTypesOnly=1")

        elif self.cnxn.authmethod == 'SQL Server Authetication':
            connectionstring = pyodbc.connect('DRIVER={' + self.cnxn.driver + '};SERVER=' + self.cnxn.servername + ';Database ='+ database+ ';UID=' + self.cnxn.username + ';PWD=' + self.cnxn.password)
        self.connectionstring = connectionstring
        print(database , self.connectionstring)
        return connectionstring

    def get_databases(self):
        cursor = self.buildCNXN('')
        cur = cursor.cursor()
        cursor.add_output_converter(-150, self.handle_sql_variant_as_string)
        res = cur.execute("""SELECT name FROM sys.databases""").fetchall()

        return list(zip(*res))[0]

    def handle_sql_variant_as_string(value):

            return value.decode('utf-16le')

    def view(self ):
        rows = []
        cur = self.connectionstring.cursor()
        with open("queries3.csv", 'r') as file:
            csvreader = csv.reader(file , delimiter= '')
            header = next(csvreader)
            for row in csvreader:
                if (row[2] != ""):
                    cur.execute(row[2])
                    QueryResult = cur.fetchall()

                    for index in range(3,len(row)):
                       if(int(row[index]) == QueryResult[0][index-2]):
                           print("biobio")


                    print("expected:", int(row[3]) == QueryResult[0][1], "result:", QueryResult[0][1])
                    rows.append(tuple(QueryResult[0]))

        print(rows)

        # cur = self.cnxn.cursor()
        # cur.execute("SELECT * FROM sys.servers")
        # rows = cur.fetchall()
        # print(rows)
        return rows
