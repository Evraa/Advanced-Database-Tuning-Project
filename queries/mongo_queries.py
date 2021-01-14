import pymongo
import json


def create_client(db_name):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[db_name]
    return mydb, myclient

def create_collection(name,mydb):
    '''
        + Give it a name and a mydb object, open the db and it will read it from json.
        + Don't forgt to add your json files at the data directory.
    '''
    mycol = mydb[name]
    file_name = '../data/' + name+'.json'
    with open(file_name) as f:
        file_data = json.load(f)
    mycol.insert_many(file_data)



if __name__ == "__main__":
    mydb, myclient = create_client("adv_db_prj")
    users   = mydb['useusersrs']
    matcehs = mydb['matcehs']
    stadiums = mydb['stadiums']
    teams   = mydb['teams']
    
    myclient.close()
