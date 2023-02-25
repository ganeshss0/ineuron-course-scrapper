import psycopg2
import logging

logging.basicConfig(filename = 'app.log', filemode='a', level = logging.DEBUG, format = '%(asctime)s %(levelname)s: %(message)s')

class Store_Sql:
    def __init__(self, server, db, user, password, port):
        self.server = server
        self.db = db
        self.user = user
        self.pswd = password
        self.port = port
        self.sslmode = 'require'

    
    def test(self):
       
        try:
            conn_string = f'host={self.server} port={self.port} dbname={self.db} user={self.user} password={self.pswd} sslmode={self.sslmode}'
            self.connection = psycopg2.connect(conn_string)
            logging.info('Connected SQL Server')
            return True
        except Exception as e:
            logging.error(f'Failed Connection SQL Server {e}')
            return False


    def upload(self, data) -> bool:
        try:
            cursor = self.connection.cursor()
            for bundle_name, courses in data.items():
                bundle_name = ''.join(bundle_name.split(' '))
                cursor.execute(f'CREATE TABLE {bundle_name} (CourseName VARCHAR(255));')
                for course in courses['courses']:
                    cursor.execute(f"""INSERT INTO {bundle_name} VALUES(%s)""", (course['title'],))
            self.connection.commit()
            cursor.close()
            self.connection.close()
            logging.info('Data Inserted SQL Server')
            return True
        except Exception as e:
            logging.error(f'Failed Data Inserted SQL Server {e}')
            return False
            


 
