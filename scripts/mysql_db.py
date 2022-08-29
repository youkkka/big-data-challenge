from __future__ import print_function
import mysql
import mysql.connector
from mysql.connector import errorcode

cnx = mysql.connector.connect(user='localuser', password='localpwd',
                                database='localdb', host='mysql',
                                auth_plugin='mysql_native_password')

DB_NAME = 'localdb'

TABLES = {}
TABLES['localdb'] = (
    "CREATE TABLE `counts` ("
    "  `parent` varchar(16) NOT NULL,"
    "  `count`  int(11) NOT NULL,"
    "  PRIMARY KEY (`parent`)"
    ") ENGINE=InnoDB")

cursor = cnx.cursor()

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

def update_table(par, val):
    update_df = "UPDATE counts SET count = %s WHERE parent = %s"
    cursor.execute(update_df, (val,par))
    cnx.commit()

add_df = ("INSERT INTO counts "
              "(parent, count) "
              "VALUES (%s, %s)")

data_df = ('mother', 3)

# cursor.execute(add_df, data_df)

select_df = ("SELECT * FROM counts "
               "WHERE parent='mother'")

cursor.execute(select_df)

# for (parent, count) in cursor:
#     print(parent, count)

new = 45
for (parent, count) in cursor:
    print(parent, count)
    update_table(parent, int(count) + new)


cursor.close()
cnx.close()


