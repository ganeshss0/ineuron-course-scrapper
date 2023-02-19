import pyodbc


class Store_Sql:
    def __init__(self, server, db, user, password):
        self.server = server
        self.db = db
        self.user = user
        self.pswd = password
        self.driver= '{ODBC Driver 18 for SQL Server}'
    
    def upload(self, data) -> bool:
        try:
            with pyodbc.connect('DRIVER=' + self.driver + ';SERVER=tcp:' + self.server + ';PORT=1433;DATABASE=' + self.db + ';UID=' + self.user + ';PWD=' + self.pswd) as conn:
                with conn.cursor() as cursor:
                    for bundle_name, courses in data.items():
                        cursor.execute(f'CREATE TABLE {bundle_name} (CourseName VARCHAR(255));')
                        for course in courses['courses']:
                            cursor.execute(f"""INSERT INTO {bundle_name} VALUES('{course["title"]}')""")
            return True
        except:
            return False
            


 