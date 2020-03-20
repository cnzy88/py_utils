#coding: utf-8
import pymongo

class MongoDbHelp(object):

    def __init__(self, db, host='localhost', port=27017):
        self.db_client = pymongo.MongoClient("mongodb://%s:%d/" % (host, port))
        self.db = db

    def insert(self, table, obj):
        self.db_client[self.db][table].insert_one(obj)

    def find(self, table, query):
        return self.db_client[self.db][table].find(query)

    def delete(self, table, query):
        return self.db_client[self.db][table].delete_many(query)



if __name__ == '__main__':
    db = MongoDbHelp(db='insurance_compare')
    # print mongo.find('product', {'product_name': '达尔文2号'})
    db.delete('product', {})