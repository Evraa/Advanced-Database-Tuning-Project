import json
from faker import Faker
import random
from random import randint

#matcehs and users count
itrs = 500000

TEAMS_NUM = 1000
STADIUMS_NUM = 200
CITY_NUM = 500
DATES_COUNT = itrs / 10
fake = Faker('en_US')

#get list of cities
_cities = []
city = fake.city()
while city in _cities:
    city = fake.city()
_cities.append(city)


data = []
user_ids = []
managers = []
fans = []
with open("users.json", "w") as write_file:
    for i in range(itrs):
        if i % 1000 == 0: print (f"user:  Iteration: {i}")
        ev = random.randint(0, 2)

        role = 'manager' if (ev==0 or i==0) else 'fan'

        #unique
        username = fake.profile()['name']

        #unique
        user_id = {"$oid": fake.hexify('^^^^^^^^^^^^^^^^^^^^^^^^')}
        user_ids.append(user_id)
        
        ev = randint(0, 10)
        reserve_info = {}
        if role == 'manager':
            managers.append(user_id)
        else:
            fans.append(user_id)
        

        my_dict = {
                    '_id':user_id,
                    'username':username,
                    'role':role,
                    'email':fake.profile()['mail'],
                    'pass':fake.password(length=8),
                    'fname':fake.first_name(),
                    'lname':fake.last_name(),
                    'bdate':fake.date_time().strftime('%Y-%m-%dT%H:%M:%S.%f'),
                    'gender':fake.profile()['sex'],
                    'city':random.choice(_cities)
                }
        data.append(my_dict)
    json.dump(data, write_file)


#unique match ids
match_ids = []
for i in range (itrs):
    match_id = {"$oid": fake.hexify('^^^^^^^^^^^^^^^^^^^^^^^^')}
    match_ids.append(match_id)

#unique teams
teams_names = []
teams_ids = []
for i in range (TEAMS_NUM):
    team = fake.profile()['company']
    teams_names.append(team)

    team_id = {"$oid": fake.hexify('^^^^^^^^^^^^^^^^^^^^^^^^')}
    teams_ids.append(team_id)

#unique stads
stads_names = []
stads_ids = []
stad_x_y = []
for i in range (STADIUMS_NUM):
    stad = fake.city()
    stads_names.append(stad)
    stad_x_y.append([randint(2,15),randint(2,15)])

    stads_id = {"$oid": fake.hexify('^^^^^^^^^^^^^^^^^^^^^^^^')}
    stads_ids.append(stads_id)

#unique dates but specific
_dates = []
for i in range (DATES_COUNT):
    date = fake.date_time().strftime('%Y-%m-%dT%H:%M:%S.%f')
    _dates.append(date)


matches_picked = []
managers_taken = []
data_y = []
data = []
with open("matches.json", "w") as write_file:
    for i in range(itrs):
        if i % 1000 == 0: print (f"Match:  Iteration: {i}")

        m_id = match_ids[i]

        #pick one random manager
        manager_user = random.choice(managers)

        #home team
        team_x = random.choice(teams_names)
        team_y = random.choice(teams_names)
        while team_x == team_y:
            team_y = random.choice(teams_names)

        stad_i = randint(0, len(stads_ids)-1)
        stad_name = stads_names[stad_i]

        width, height = stad_x_y[stad_i]
        k = 0
        users_picked = []
        for ii in range (width):
            for jj in range (height):
                ev = randint(0,2)
                if ev == 1 and len (users_picked) != len(fans):
                    #assign
                    fan = random.choice(fans)
                    users_picked.append({'user_id':fan, 'x_i':ii, 'y_i':jj})
                    k += 1

        
        my_dict = {
                    '_id':m_id,
                    'referee':fake.profile()['name'],
                    'date_time':random.choice(_dates),
                    'teams':{
                        'home':team_x,
                        'away':team_y
                    },
                    'stadium':{
                        'name':stad_name,
                        'width':stad_x_y[stad_i][0],
                        'height':stad_x_y[stad_i][1]
                    },
                    'line_men':{
                        'first':fake.profile()['name'],
                        'second':fake.profile()['name']
                    },
                    'manager_scheduled':manager_user,
                    'users_reserved':users_picked
                    
                }
        data_y.append(my_dict)
    json.dump(data_y, write_file)


data = []
with open("teams.json", "w") as write_file:
    for i in range(TEAMS_NUM):
        if i % 100 == 0: 
            print (f"Team:  Iteration: {i}")
        team_id = teams_ids[i]
        team_name = teams_names[i]

        my_dict={
            '_id':team_id,
            'team_name':team_name
        }
        data.append(my_dict)
    json.dump(data, write_file)



data = []
with open("stadiums.json", "w") as write_file:
    for i in range(STADIUMS_NUM):
        if i % 10 == 0: 
            print (f"stadium:  Iteration: {i}")
        stad_id = stads_ids[i]
        stads_name = stads_names[i]

        my_dict={
            '_id':stad_id,
            'stad_name':stads_name,
            'width':stad_x_y[i][0],
            'height':stad_x_y[i][1]
        }
        data.append(my_dict)
    json.dump(data, write_file)

    