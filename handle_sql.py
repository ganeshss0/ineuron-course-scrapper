from sqlalchemy import create_engine

class Store_Sql:
    def __init__(self, server, db, user, password, port):
        self.server = server
        self.db = db
        self.user = user
        self.pswd = password
        self.port = port

    
    def test(self):
        url = f'postgresql://{self.user}:{self.pswd}@{self.server}:{self.port}/{self.db}'
        try:
            self.connection = create_engine(url)
            return True
        except:
            return False


    def upload(self, data) -> bool:
        try:
            for bundle_name, courses in data.items():
                self.connection.execute(f'CREATE TABLE {bundle_name} (CourseName VARCHAR(255));')
                for course in courses['courses']:
                    self.connection.execute(f"""INSERT INTO {bundle_name} VALUES('{course["title"]}')""")
            return True
        except:
            return False
            


 