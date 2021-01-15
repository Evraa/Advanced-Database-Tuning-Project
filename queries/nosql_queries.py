import pymongo
import json
from bson.objectid import ObjectId
import numpy as np
import pprint

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


def q_1(user_obj, match_obj,team_obj,team_id=ObjectId('2f884164f21ba9602d8263db'),city="South Tyrone"):
    '''
        1- select users from specific city that watched a specific team in the team's home match
    '''

    # evs = user_obj.find({'city':city},{'_id':1})
    # for ev in evs:
    #     pprint.pprint(ev)
    # return

    pipeline = [
        #1- find the match_ids with team_x as home
        {'$match': {'teams.home':team_obj.find_one(team_id)['team_name']}},
        {'$project': {'_id':0,'users_reserved.user_id':1} },
        {'$unwind':"$users_reserved"},
        #2- unwind and group fans
        {'$group':{'_id':'$users_reserved.user_id'}},
        #3- match fans with users
        {'$lookup':{
            'from':'users',
            'localField':'_id',
            'foreignField':'_id',
            'as':'users_info'
        }},
        #4- get fans at specific city
        {'$match': {'users_info.city':city}},
        #5- project results
        {'$project':{'_id':0,'fname':'$users_info.fname','lname':'$users_info.lname'}}
    ]

    match_docs = match_obj.aggregate(pipeline)
    print ("Printing Results..")
    count = 0
    for match_doc in match_docs:
        
        pprint.pprint(match_doc)
        count+=1
    print (f'Results Count: {count}')


def q_2(user_obj,match_obj,date_l='1999-07-02T07:57:33.000000',date_u='2000-07-02T07:57:33.000000'):
    '''
        (select users that attended matches in range of date).
    '''

    pipeline = [
        {'$match': {'date_time': {'$gt':date_l , '$lt': date_u}  }},

        {'$project': {'_id':0, 'users_reserved.user_id':1}},

        {'$unwind':"$users_reserved"},

        {'$lookup':{
            'from':'users',
            'localField':'users_reserved.user_id',
            'foreignField':'_id',
            'as':'users_info'
        }},
        {'$project':{'_id':0,'fname':'$users_info.fname','lname':'$users_info.lname'}}
       
                    
    ]
    match_docs = match_obj.aggregate(pipeline)
    print ("Printing Results..")
    count = 0
    for match_doc in match_docs:
        
        pprint.pprint(match_doc)
        count+=1
    print (f'Results Count: {count}')


def q_3(user_obj, match_obj):
    '''
    (select users that attended any match and sit on the first row i.e. y = 1).
    '''

    pipeline = [
        {'$project': {'_id':0, 'users_reserved.y_i':1, 'users_reserved.user_id':1}},
        {'$unwind': '$users_reserved'},
        {'$match': { 'users_reserved.y_i': 1}},

        {'$lookup':{
            'from':'users',
            'localField':'users_reserved.user_id',
            'foreignField':'_id',
            'as':'users_info'
        }},
        {'$project':{'_id':0,'fname':'$users_info.fname','lname':'$users_info.lname'}}
                    
    ]

    match_docs = match_obj.aggregate(pipeline)
    print ("Printing Results..")
    count = 0
    for match_doc in match_docs:
        
        pprint.pprint(match_doc)
        count+=1
    print (f'Results Count: {count}')



def q_4(user_obj, match_obj):
    '''
    2 -> 15
    far : x > 7 and y > 7
    (select users that attended any match and sit far i.e. x = 20 and y = 50).
    '''
    
    pipeline = [
        {'$project': {'_id':0, 'users_reserved.y_i':1,'users_reserved.x_i':1, 'users_reserved.user_id':1}},
        {'$unwind': '$users_reserved'},
        {'$match': {  '$and': [ {'users_reserved.y_i': {'$gt':7}} , 
                                {'users_reserved.x_i': {'$gt':7}}
                            ] 
                    }},

        {'$lookup':{
            'from':'users',
            'localField':'users_reserved.user_id',
            'foreignField':'_id',
            'as':'users_info'
        }},
        {'$project':{'_id':0,'fname':'$users_info.fname','lname':'$users_info.lname'}}
                    
    ]

    match_docs = match_obj.aggregate(pipeline)
    print ("Printing Results..")
    count = 0
    for match_doc in match_docs:
        
        pprint.pprint(match_doc)
        count+=1
    print (f'Results Count: {count}')




if __name__ == "__main__":
    mydb, myclient = create_client("adv_db_prj")
    users, matches, stadiums, teams = mydb['users'], mydb['matches'],mydb['stadiums'],mydb['teams']
    # view_one_doc([teams])
    
    # q_1(users,matches,teams)
    # q_2(users,matches)
    # q_3(users,matches)
    # q_4(users, matches)
    

    # first_five = users.find().limit(50)
    # for f in first_five:
        # print (f['_id'], f['city'])



    # when finished
    myclient.close()
