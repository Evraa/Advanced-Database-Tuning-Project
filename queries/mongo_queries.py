import pymongo
import json
from bson.objectid import ObjectId
import numpy as np

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


def view_one_doc(cols):
    for col in cols:
        print (col.find_one())

def q_1(match_obj,match_id=ObjectId('84eb185ed16d7a6b818d2389')):
    '''
        1- Given a matchid get set of free seats in the stadium.
    '''

    #first get the match we are taking about
    #we know it's only one
    match_doc = match_obj.find_one({'_id':match_id})
    #get stad x and y [11,7]
    x,y = match_doc['stadium']['width'],match_doc['stadium']['height']
    stadium = np.zeros([x,y])
    #secondly get the user reserved seats to mark them.
    user_reserved = match_doc['users_reserved']
    for usr_rsv in user_reserved:
        y_i,x_i = usr_rsv['y_i'], usr_rsv['x_i']
        stadium[x_i,y_i] = 1
    
    results = []
    for i in range(x):
        for j in range(y):
            if stadium[i,j] == 0: results.append((i,j))

    return results

def q_2(user_obj,match_obj,date='1981-07-02T07:57:33.000000'):
    '''
        2- Get set of attendence of matches in specific day.
        Note: faker is so good, that each match is played at exactly one day!
        but the code is fine to be applcable with multiple matches within the same day.
    '''

    #first get matches played at that day
    match_docs = match_obj.find({'date_time':date})
    results = []
    for match_doc in match_docs:
        reservations = match_doc['users_reserved']
        for reservation in reservations:
            #fetch user
            user_id = reservation['user_id']
            user_doc = user_obj.find_one({'_id':user_id})
            result = [
                    user_doc['fname'],
                    user_doc['lname'],
                    reservation['x_i'],
                    reservation['y_i'],
                    match_doc['teams']['home'], 
                    match_doc['teams']['away'],
                    match_doc['stadium']['name']
            ]
            results.append(result)
    return (results)

def q_3_fan(user_obj, match_obj, user_id=ObjectId('5ca3958688a8c7d732c0526f')):
    '''
    3- For a user get history of all his matches // ATTENDED
    '''
    pass


def q_3_man(user_obj, match_obj, user_id=ObjectId('b4981db546aff323e9e0678f')):
    
    #get managers
    man_ids = user_obj.find({'role':'manager'},{'_id':1, 'username':1})
    results = []
    for i,man in enumerate(man_ids):
        if i%1000==0:print (f'Processing Q:3_2, \tManager:{i}')
        matches_managed = match_obj.find({'manager_scheduled':man['_id']}, 
                                        {'_id':0,'teams':1,'stadium':1,'date_time':1})
        for match in matches_managed:
            result = [
                man['username'],
                match['teams']['home'],
                match['teams']['away'],
                match['stadium']['name'],
                match['date_time'] 
            ]
            results.append(result)
    
    
    print (len(results))

def q_4(team_obj, match_obj, team_id=ObjectId('2f884164f21ba9602d8263db')):
    '''
    4- Set of Matches for specific team.
    '''
    
    #get team name
    team_name = team_obj.find_one({'_id':team_id})
    #get matches
    matches = match_obj.find({
        '$or':[
            {'teams.home':team_name['team_name']},
            {'teams.away':team_name['team_name']}
        ]
        })
    results = []
    for match in matches:
        result = [
            match['teams']['home'],
            match['teams']['away'],
            match['referee'],
            len(match['users_reserved']),
            match['stadium']['name'],
            match['date_time']            
        ]
        results.append(result)
    return results

if __name__ == "__main__":
    mydb, myclient = create_client("adv_db_prj")
    users, matches, stadiums, teams = mydb['users'], mydb['matches'],mydb['stadiums'],mydb['teams']
    # view_one_doc([teams])
    
    # q_1(matches)
    # q_2(users,matches)
    q_3_man(users, matches)
    # q_4(teams, matches)

    # first_five = users.find().limit(50)
    # for f in first_five:
    #     print (f['_id'], f['role'])
    #when finished
    myclient.close()
