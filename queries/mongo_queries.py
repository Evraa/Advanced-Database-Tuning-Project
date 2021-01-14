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

def q_1(match_obj,match_id=ObjectId('84eb185ed16d7a6b818d2389')):
    '''
        1- Given a matchid get set of free seats in the stadium.
    '''

    #first get the match we are taking about
    pipeline = [
        {'$match': {'_id':match_id}},
        {'$project': {'users_reserved.x_i':1,'users_reserved.y_i':1}}
    ]

    match_docs = match_obj.aggregate(pipeline)

    for match_doc in match_docs:
        pprint.pprint(match_doc)

    #NOTE: Can't get the FREE Seats


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


def q_3_fan(user_obj, match_obj, user_id=ObjectId('5ca3958688a8c7d732c0526f')):
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



def q_3_man(user_obj, match_obj, user_id=ObjectId('e536d09303e53afe634eb0b4')):
    '''
        3_2: list all managers with their matches scheduled info.
    '''
    #get managers

    pipeline = [
        {'$match': {'_id':user_id}},
        
        {'$project': {'_id':1, 'username':1,'role':1}},

        {'$lookup':{
            'from':'matches',
            'localField':'_id',
            'foreignField':'manager_scheduled',
            'as':'matches_info'
        }},

        {'$project': { 'username':1, 'matches_info.teams':1, 'matches_info.date_time':1,
                        'matches_info.stadium':1, 
        }},
    ]


    user_docs = user_obj.aggregate(pipeline)

    for user_doc in user_docs:
        pprint.pprint(user_doc)


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
        },{
            '_id':0, 'team_home':'$teams.home','team_away':'$teams.away', 'referee':1,
            'stad_name':'$stadium.name', 'date_time':1,
            'audience_count': { '$cond': { 'if': { '$isArray': "$users_reserved" }, 
            'then': { '$size': "$users_reserved" }, 'else': "NA"}}
        })

    for match in matches:
        input("e")
        pprint.pprint(match)
    # results = []
    # for match in matches:
    #     result = [
    #         match['teams']['home'],
    #         match['teams']['away'],
    #         match['referee'],
    #         len(match['users_reserved']),
    #         match['stadium']['name'],
    #         match['date_time']            
    #     ]
    #     results.append(result)
    # return results

def q_5(team_obj, match_obj, team_id=ObjectId('2f884164f21ba9602d8263db')):
    #get team name
    team_name = team_obj.find_one({'_id':team_id})
    
    #get matches
    matches = match_obj.find({'teams.home':team_name['team_name']}, {'users_reserved':1})
    results = []
    for match in matches:
        results.append(len(match['users_reserved']))
    
    stat= (min(results),max(results),sum(results)/len(results),sum(results))
    return (stat)

def q_6(stad_obj, user_obj, match_obj, stad_id = ObjectId('1539a9451eb51a34df87c3bc')):
    '''
    6- History of reservations for specific stadium. //Lake Stephanieberg
    '''
    #get stad name
    stad_name = stad_obj.find_one({'_id':stad_id})['stad_name']
    #get matches
    matches = match_obj.find({'stadium.name':stad_name}, {'teams':1,'date_time':1,'users_reserved':1})
    results = []
    for match in matches:
        reservations = match['users_reserved']
        for reservation in reservations:
            user_id = reservation['user_id']
            x_i = reservation['x_i']
            y_i = reservation['y_i']

            user = user_obj.find_one({'_id':user_id},{'fname':1,'lname':1})
            result = [
                stad_name,
                user['fname'],
                user['lname'],
                x_i, y_i,
                match['teams']['home'],
                match['teams']['away'],
                match['date_time']
            ]
            results.append(result)
    # print (len(results))
    return results

def q_8(team_obj, match_obj, user_obj, team_id=ObjectId('2f884164f21ba9602d8263db')):
    '''
    8- Get all audience of a specific team that are females. //team: Navarro Inc

    fname           lname           countOfMatches
    '''
    #get team name
    team_name = team_obj.find_one({'_id':team_id},{'team_name':1})
    #get matches
    matches = match_obj.find({
        '$or':[
            {'teams.home':team_name['team_name']},
            {'teams.away':team_name['team_name']}
        ]
        }, {'users_reserved':1})
    results = []
    for match in matches:
        reservations = match['users_reserved']
        for reservation in reservations:
            user_id = reservation['user_id']
            user = user_obj.find_one({'_id':user_id,'gender':'F'},{'fname':1,'lname':1})
            if user is not None:
                result = [user['fname'],user['lname']]
                results.append(result)
    print (len(results))
    return results


if __name__ == "__main__":
    mydb, myclient = create_client("adv_db_prj")
    users, matches, stadiums, teams = mydb['users'], mydb['matches'],mydb['stadiums'],mydb['teams']
    # view_one_doc([matches])
    
    # q_1(matches)
    # q_2(users,matches)
    # q_3_fan(users,matches)
    # q_3_man(users, matches)
    q_4(teams, matches)
    # q_5(teams, matches)
    # q_6(stadiums, users, matches)
    # q_8(teams, matches, users)


    # first_five = users.find().limit(50)
    # for f in first_five:
    #     print (f['_id'], f['role'])


    # when finished
    myclient.close()
