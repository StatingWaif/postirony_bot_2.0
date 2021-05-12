import mysql.connector
import config


class DataBase:
        def __init__(self):
                self.mydb = mysql.connector.connect(
                        host=config.host,
                        user=config.user,
                        passwd=config.passwd,
                        database=config.database,
                        buffered=True
                        )

        async def getInDataBase(self, group, pic):
                mycursor = self.mydb.cursor()
                if not self.isInBase(group, pic):
                    try:
                            mycursor.execute(f'INSERT INTO group_{group} VALUE ({pic})')
                    except mysql.connector.errors.ProgrammingError:
                            mycursor.execute(f"CREATE TABLE group_{group} (pic INTEGER(10))")
                            mycursor.execute(f'INSERT INTO group_{group} VALUE ({pic})')
                    self.mydb.commit()
                else:
                    print('не засунул, уже есть')

        async def isInBase(self, group, pic):
                mycursor = self.mydb.cursor()
                listOfValues = []
                mycursor.execute(f'SELECT * FROM group_{group}')
                for value in mycursor:
                        listOfValues.append(value[0])

                if int(pic) in listOfValues:
                        return True
                else:
                        return False