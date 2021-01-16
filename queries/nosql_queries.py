import pymongo
import json
from bson.objectid import ObjectId
import numpy as np
import pprint
import random

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


def q_1(user_obj, match_obj,team_obj, city, team_id):
    '''
        (select users (with specific fname or from specific city) that watched a specific team in the team's home match).
    '''

    pipeline = [
        #1- find the match_ids with team_x as home
        {'$match': {'teams.home': team_obj.find_one(team_id)['team_name']} },
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
        {'$match': {'users_info.city':city} },
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


def q_2(user_obj, match_obj):
    '''
    (select users that attended any match and sit at i.e. x = 10 and y = 12).
    '''
    pipeline = [
        {'$project': {'_id':0, 'users_reserved.y_i':1,'users_reserved.x_i':1, 'users_reserved.user_id':1}},
        {'$unwind': '$users_reserved'},
        {'$match': {  '$and': [ {'users_reserved.y_i': {'$eq':12}} , 
                                {'users_reserved.x_i': {'$eq':10}}
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

def q_3(user_obj, match_obj):
    '''
    (select users that attended any match and sit far i.e. x > 12 and y > 12).
    '''
    
    pipeline = [
        {'$project': {'_id':0, 'users_reserved.y_i':1,'users_reserved.x_i':1, 'users_reserved.user_id':1}},
        {'$unwind': '$users_reserved'},
        {'$match': {  '$and': [ {'users_reserved.y_i': {'$gt':10}} , 
                                {'users_reserved.x_i': {'$gt':10}}
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


def q_4(user_obj, match_obj,team_obj, fname, city, team_id):
    '''
        (select users (with specific fname or from specific city) that watched a specific team in the team's home match).
    '''

    pipeline = [
        #1- find the match_ids with team_x as home
        {'$match': {'teams.home': team_obj.find_one(team_id)['team_name']} },
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
        {'$match': {'users_info.city':city} },
        #4-2 specific fname
        {'$match': {'users_info.fname':fname} },
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


def q_5(user_obj, match_obj,team_obj, fname, city, team_id):
    q_4(user_obj, match_obj,team_obj, fname, city, team_id)
    

def q_6(user_obj, match_obj):
    '''
        (select users that sit on a seat where y = 10).
    '''
    
    pipeline = [
        {'$project': {'_id':0, 'users_reserved.y_i':1,'users_reserved.x_i':1, 'users_reserved.user_id':1}},
        {'$unwind': '$users_reserved'},
        {'$match': { 'users_reserved.y_i': 10 }},

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


def get_teams_fans(user_obj, match_obj,team_obj, team_id):
    '''
        print teams fans and cities.
    '''
    pipeline = [
        #1- find the match_ids with team_x as home
        {'$match': {'teams.home': team_obj.find_one(team_id)['team_name']} },
        {'$project': {'_id':0,'users_reserved.user_id':1} },
        #2- unwind and group fans
        {'$unwind':"$users_reserved"},
        {'$group':{'_id':'$users_reserved.user_id'}},
        #3- match fans with users
        {'$lookup':{
            'from':'users',
            'localField':'_id',
            'foreignField':'_id',
            'as':'users_info'
        }},
        #5- project results
        {'$project':{'_id':0,'fname':'$users_info.fname','city':'$users_info.city'}}
    ]

    match_docs = match_obj.aggregate(pipeline)
    print ("Preprocessing..")
    count = 0
    for match_doc in match_docs:
        count+=1
        if count % 100 == 0:
            return match_doc['fname'], match_doc['city']
    

def get_random_team_id(team_obj):
    random_team = list(team_obj.aggregate([{'$sample': {'size':1}}]))[0]
    team_id = random_team["_id"]
    return team_id

if __name__ == "__main__":
    mydb, myclient = create_client("adv_db_prj_3")
    users, matches, stadiums, teams = mydb['users'], mydb['matches'],mydb['stadiums'],mydb['teams']

    ## PREPROCESSING ##
    # view_one_doc([users,matches,stadiums,teams])
    rand_team_id = get_random_team_id(teams)
    fname,city = get_teams_fans(users, matches, teams, rand_team_id)
    
    # q_1(users, matches, teams,city=city[0], team_id = rand_team_id)
    # q_2(users,matches)
    # q_3(users,matches)
    # q_4(users, matches, teams, fname=fname[0], 
    #       city=city[0], team_id = rand_team_id)
    # q_5(users, matches, teams, fname=fname[0], 
    #       city=city[0], team_id = rand_team_id)
    
    # q_6(users,matches)
    


    # first_five = teams.find().limit(50)
    # for f in first_five:
    #     print (f['_id'], f['team_name'])



    # when finished
    myclient.close()

    #TODO: Add distinct and add mongo shell comands for these quereies.