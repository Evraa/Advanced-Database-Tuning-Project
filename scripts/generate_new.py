import json
from faker import Faker
import random
from random import randint
import datetime



itrs = 1000000*5
fake = Faker('en_US')

#unique match ids
match_ids = []
for i in range (itrs):
    match_id = fake.msisdn()
    while match_id in match_ids:
        match_id = fake.msisdn()
    match_ids.append(match_id)

data = []
usernames = []

with open("player.json", "w") as write_file:
    for i in range(itrs):
        if i % 1000 == 0: print (f"Player:  Iteration: {i}")
        ev = random.randint(0, 2)

        role = 'manage' if ev==0 else 'fan'
        #unique
        username = fake.profile()['name']
        while username in usernames:
            username = fake.profile()['name']
        usernames.append(username)
        
        ev = randint(0, 10)
        
        reserve_info = {}
        for l in range (ev):
            match_id = random.choice(match_ids)
            reserve_info['reserve_info_'+str(l)] = {'x_i':randint(0,ev*ev),'y_i':randint(0,ev*ev),'match_id':match_id}

        my_dict = {
                    'role':role,
                    'email':fake.profile()['mail'],
                    'pass':fake.password(length=8),
                    'username':username,
                    'fname':fake.first_name(),
                    'lname':fake.last_name(),
                    'bdate':fake.date_time().strftime('%Y-%m-%dT%H:%M:%S.%f'),
                    'gender':fake.profile()['sex'],
                    'city':fake.city(),
                    'reservations': reserve_info
                }
        data.append(my_dict)
    json.dump(data, write_file)

matches_picked = []
data_y = []
with open("match.json", "w") as write_file:
    for i in range(itrs):
        if i % 1000 == 0: print (f"Match:  Iteration: {i}")
        m_id = random.choice(match_ids)
        match_ids.remove(m_id)

        users_dict = {}
        users_taken = []
        j = 0
        for dic in data:
            for recv in dic['reservations']:
                if m_id == dic['reservations'][recv]['match_id'] and dic['username'] not in users_taken:
                    users_dict['user_'+str(j)] = dic['username']
                    j += 1
                    users_taken.append(dic['username'])

            
        my_dict = {
                    'match_id':m_id,
                    'referee':fake.profile()['name'],
                    'date_time':fake.date_time().strftime('%Y-%m-%dT%H:%M:%S.%f'),
                    'teams':{
                        'home':fake.profile()['company'],
                        'away':fake.profile()['company']
                    },
                    'stadium':{
                        'name':fake.city(),
                        'x':randint(2, 15),
                        'y':randint(2, 15)
                    },
                    'line_men':{
                        'first':fake.profile()['name'],
                        'second':fake.profile()['name']
                    },
                    'users':users_dict
                }
        data_y.append(my_dict)
    json.dump(data_y, write_file)


    
        

    
