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
        {'$project':{'_id':0,'fname':'users_info.fname','lname':'users_info.lname'}}
    ]

    match_docs = match_obj.aggregate(pipeline)
    print ("Printing Results..")
    count = 0
    for match_doc in match_docs:
        
        pprint.pprint(match_doc)
        count+=1
    print (f'Results Count: {count}')


def q_2(user_obj,match_obj,date='1981-07-02T07:57:33.000000'):
    '''
        2- Get set of attendence of matches in specific day.
        Note: faker is so good, that each match is played at exactly one day!
        but the code is fine to be applcable with multiple matches within the same day.
    '''

    pipeline = [
        {'$match': {'date_time':date}},
        
        {'$project': {'_id':0,'indexes':'$users_reserved',
                        'team_home':'$teams.home','team_away':'$teams.away',
                        'stad_name':'$stadium.name',}},
        {'$unwind':"$indexes"},

        {'$lookup':{
            'from':'users',
            'localField':'indexes.user_id',
            'foreignField':'_id',
            'as':'users_info'
        }},

        {'$project': { 'index_x': '$indexes.x_i','index_y': '$indexes.y_i',
                        'team_home':1,'team_away':1,
                        'stad_name':1,'fname':'$users_info.fname','lname':'$users_info.lname'
        }},
                    
    ]
    match_docs = match_obj.aggregate(pipeline)

    for match_doc in match_docs:
        pprint.pprint(match_doc)


def q_3(user_obj, match_obj, user_id=ObjectId('5ca3958688a8c7d732c0526f')):
    '''
    3- For a user get history of all his matches // ATTENDED
    '''

    pipeline = [
        {'$match': {'_id':user_id}},
        
        {'$project': {'_id':1}},

        {'$lookup':{
            'from':'matches',
            'localField':'_id',
            'foreignField':'users_reserved.user_id',
            'as':'matches_info'
        }},

        {'$project': { 'matches_info.teams':1, 'matches_info.date_time':1,
                        'matches_info.stadium':1, 
        }},

        # {'$group':{'_id':'$matches_info.users_reserved.user_id'}}
        # {'$match':{'matches_info.users_reserved.user_id':user_id}}
                    
    ]


    user_docs = user_obj.aggregate(pipeline)

    for user_doc in user_docs:
        pprint.pprint(user_doc)

    #NOTE: Can't get seats for THAT user.



def q_4(team_obj, match_obj, team_id=ObjectId('2f884164f21ba9602d8263db')):
    '''
    4- Set of Matches for specific team.
    '''
    
    #get matches
    matches = match_obj.find({
        '$or':[
            {'teams.home':team_obj.find_one({'_id':team_id})['team_name']},
            {'teams.away':team_obj.find_one({'_id':team_id})['team_name']}
        ]
        },{
            '_id':0, 'team_home':'$teams.home','team_away':'$teams.away', 'referee':1,
            'stad_name':'$stadium.name', 'date_time':1,

            'audience_count': { '$cond': { 'if': { '$isArray': "$users_reserved" }, 
            'then': { '$size': "$users_reserved" }, 'else': "NA"}}
        })

    for match in matches:
        pprint.pprint(match)




if __name__ == "__main__":
    mydb, myclient = create_client("adv_db_prj")
    users, matches, stadiums, teams = mydb['users'], mydb['matches'],mydb['stadiums'],mydb['teams']
    # view_one_doc([teams])
    
    q_1(users,matches,teams)
    # q_2(users,matches)
    # q__3(users,matches)
    # q_4(teams, matches)
    

    # first_five = users.find().limit(50)
    # for f in first_five:
        # print (f['_id'], f['city'])


    # when finished
    myclient.close()
