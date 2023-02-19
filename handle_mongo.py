import pymongo

class Store_Mongo:
    def __init__(self, connection_string: str):
        self.connect = connection_string
    
    def test(self) -> bool:
        try:
            self.client = pymongo.MongoClient(self.connect)
            return True
        except:
            return False

    def upload(self, data):
        db = self.client['iNeuron_Courses_Data']
        collection = db['iNeuron_Courses']
        collection.insert_many(list(data.values()))
        return 'Data Uploaded Successfully'