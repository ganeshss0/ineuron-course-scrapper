import pymongo, logging

logging.basicConfig(filename = 'app.log', filemode='a', level = logging.DEBUG, format = '%(asctime)s %(levelname)s: %(message)s')

class Store_Mongo:
    def __init__(self, connection_string: str):
        self.connect = connection_string
    
    def test(self) -> bool:
        try:
            self.client = pymongo.MongoClient(self.connect)
            logging.info('Connected MongoAtlas')
            return True
        except Exception as e:
            logging.error(f'Failed Connection MongoAltas {e}')
            return False

    def upload(self, data):
        try:
            db = self.client['iNeuron_Courses_Data']
            collection = db['iNeuron_Courses']
            collection.insert_many(list(data.values()))
            logging.info('Data Inserted MongoAtlas')
            return True
        except Exception as e:
            logging.error(f'Failed Data Inserted MongoAtlas {e}')
            return False