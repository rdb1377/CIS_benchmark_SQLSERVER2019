import csv
import pyodbc
import pandas


class Benchmarks:
    def __init__(self , cnxn):
        self.cnxn = cnxn
        self.csvreader = []
        self.data_list = []
        with open("config.csv", 'r' ) as file:
            self.data_list = list(csv.reader(file , delimiter= ','))

        self.connectionstring = self.buildCNXN('')


    def buildCNXN(self , database):
        if (database =='') :
            database = 'master'
        if self.cnxn.authmethod== 'Windows Authetication':
            connectionstring = pyodbc.connect("Driver={" + self.cnxn.driver + "};"
                              "Server=" + self.cnxn.servername + ";"
                              "Database="+database+";"
                              "Trusted_Connection=yes;"
                              "TrustServerCertificate=yes;"
                              "NeedODBCTypesOnly=1;"
                               ,autocommit=True
                              )

        elif self.cnxn.authmethod == 'SQL Server Authetication':
            connectionstring = pyodbc.connect('DRIVER={' + self.cnxn.driver + '};SERVER=' + self.cnxn.servername + ';Database ='+ database+ ';UID=' + self.cnxn.username + ';PWD=' + self.cnxn.password ,autocommit=True )
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

    def runAudit(self):
        rows = []
        cur = self.connectionstring.cursor()
        with open("config.csv", 'r' ) as file:

            self.csvreader = csv.reader(file , delimiter= ',')
            header = next(self.csvreader)
            for row in self.csvreader:
                print(row[0] , row[7])
                QueryResult = []
                result = []
                if (row[4] == "0"):  #manual
                    rows.append([row[1], row[15], "MANUAL", row[2], row[0] ]) #index , dsc , result , dsc
                elif (row[4] == "1"):  # type one
                    print("%%%%%%%" , row[5])
                    print((row[3]))
                    try:
                        cur.execute(row[3])
                        QueryResult = cur.fetchall()
                        print("despripppppppppp", cur.description)

                        widths = []
                        columns = []
                        tavnit = '|'
                        separator = '+'

                        for i in range(len(cur.description)):
                            print("&&j",cur.description[i])
                            widths.append(max(len(cur.description[i][0]) , len(str(QueryResult[0][i]))))
                            columns.append(cur.description[i][0])

                        for w in widths:
                            tavnit += " %-" + "%ss |" % (w,)
                            separator += '-' * w + '--+'

                        print(separator)
                        result += separator
                        result += '\n'
                        print(tavnit % tuple(columns))
                        result += tavnit % tuple(columns)
                        result += '\n'
                        print(separator)
                        result += separator
                        result += '\n'
                        for ro in QueryResult:
                            print(tavnit % tuple(ro))
                            result += tavnit % tuple(ro)
                            result += '\n'
                        print(separator)
                        result += separator
                        result += '\n'
                        res = ''

                        for i in result:
                            res += str(i)

                        print(res)
                        j= 0
                        for i in range(len(result)):
                            if result[i] =='\n':
                                print(result[j:i])
                            j = i

                        flag= 1
                    except pyodbc.Error as e:
                        print ("EEEEEEEEEEEEERRRRRRRRR")
                    if QueryResult:
                        for index in range(6,int(row[5])+6):
                           print("!!!!!!!!!!",row[index] , QueryResult[0])
                           if(row[index] != str(QueryResult[0][index-5])):
                               print("biobio" ,index, row[index] , QueryResult[0][index-5])
                               flag = 0


                    #print("expected:", int(row[3]) == QueryResult[0][1], "result:", QueryResult[0][1])


                        rows.append([row[1] ,row[15]  , flag , row[2], row[0] , res ])  #index , queryname , result , dsc

                elif (row[4] == "2"):
                    print("type 2")
                    flag = 1
                    try:
                        cur.execute(row[3])
                        QueryResult = cur.fetchall()

                    except pyodbc.Error as e:
                        print ("EEEEEEEEEEEEERRRRRRRRR")
                    if QueryResult:
                        flag = 0
                    rows.append([row[1], row[15], flag, row[2],row[0],QueryResult])

                elif (row[4] == "3"):
                    print("type 3")
                    flag = 0
                    try:
                        cur.execute(row[3])
                        QueryResult = cur.fetchall()

                    except pyodbc.Error as e:
                        print ( cur.messages,QueryResult)


                    if QueryResult:
                        if (int(row[6]) <= QueryResult[0][0]):
                            print(row[6] , QueryResult[0][0])
                            flag = 1
                    else:
                        QueryResult = cur.messages
                    rows.append([row[1], row[15], flag, row[2],row[0],QueryResult ])

                elif(row[4] == "4"):
                    print("type 4")
                    flag = 0
                    count = 0
                    cur.execute(row[3])
                    QueryResult = cur.fetchall()

                    for res in QueryResult:
                        if res[5] == row[6] or res[5] == row[7] or res[5] == row[8]:
                            count +=1

                    if count == 3:
                        flag = 1

                    rows.append([row[1], row[15], flag, row[2],row[0],QueryResult])

                elif (row[4] == "5"):
                    print("type 5")
                    flag = 0
                    try:
                        cur.execute(row[3])
                        QueryResult = cur.fetchall()

                    except pyodbc.Error as e:
                        print ("EEEEEEEEEEERRRRRRRRRRRR")

                    if QueryResult:
                        if ((row[6]) != QueryResult[0][0]):
                            print(row[6] , QueryResult[0][0])
                            flag = 1
                    rows.append([row[1], row[15], flag, row[2],row[0],QueryResult ])

                elif (row[4] == "6"):
                    print("type 6")
                    flag = 1

                    try:
                        cur.execute(row[3])
                        QueryResult = cur.fetchall()

                    except pyodbc.Error as e:
                        print ("EEEEEEEEEEERRRRRRRRRRRR")

                    if QueryResult:
                        for res in QueryResult:
                            if res[1] != row[6]:
                                flag = 0

                    rows.append([row[1], row[15], flag, row[2],])



        # cur = self.cnxn.cursor()
        # cur.execute("SELECT * FROM sys.servers")
        # rows = cur.fetchall()
        # print(rows)
        #cur.close()
        for row in rows:
            if row[2] == 0:
                row[2] ='FAIL'
            elif row[2] == 1:
                row[2] = 'PASS'
        return rows

    def runRemediation(self, remedition,replaceName ):
        rows = []
        result = []
        if (self.data_list[remedition][9] == "0"):
            return 0;

        print("##########", self.data_list[remedition][9])

        if(self.data_list[remedition][9]=="1"):
            for i in range(0,int(self.data_list[remedition][10])) :
                cur = self.connectionstring.cursor()
                try:
                    cur.execute(self.data_list[remedition][12+i])
                    print("###############",i ,int(self.data_list[remedition][10]) ,cur.messages)
                    result = result + cur.messages
                    self.connectionstring.commit()
                    cur.commit()
                except pyodbc.Error as e:
                    result.append(e.args[1])

        if (self.data_list[remedition][9]=="2"):
            for i in range(0,int(self.data_list[remedition][10])) :
                cur = self.connectionstring.cursor()
                try:
                    tsql = self.data_list[remedition][12+i].replace(self.data_list[remedition][11] , replaceName.get())
                    cur.execute(tsql)
                    print("ee####1025468#####", tsql,cur.messages)
                    result = result + cur.messages
                    self.connectionstring.commit()
                    cur.commit()
                except pyodbc.Error as e:
                    result.append(e.args[1])
                    print(result)


        return result
