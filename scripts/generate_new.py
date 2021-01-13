import json
from faker import Faker
import random
from random import randint
import datetime



itrs = 1*5
fake = Faker('en_US')

#unique match ids
match_ids = []
for i in range (itrs):
    match_id = fake.md5(raw_output=False),
    while match_id in match_ids:
        match_id = fake.md5(raw_output=False),
    match_ids.append(match_id)

data = []
usernames = []
user_ids = []
managers = []
with open("user.json", "w") as write_file:
    for i in range(itrs):
        if i % 1000 == 0: print (f"user:  Iteration: {i}")
        ev = random.randint(0, 2)

        role = 'manage' if ev==0 else 'fan'

        #unique
        username = fake.profile()['name']
        while username in usernames:
            username = fake.profile()['name']
        usernames.append(username)

        #unique
        user_id = fake.md5(raw_output=False)
        while user_id in user_ids:
            user_id = fake.md5(raw_output=False)
        user_ids.append(user_id)
        
        ev = randint(0, 10)
        if role == 'fan':
            reserve_info = {}
            for l in range (ev):
                match_id = random.choice(match_ids)
                reserve_info['reserve_info_'+str(l)] = {'x_i':randint(0,ev*ev),'y_i':randint(0,ev*ev),'match_id':match_id}
        else:
            #manage
            managers.append(user_id)

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
                    'city':fake.city(),
                    'reservations': reserve_info
                }
        data.append(my_dict)
    json.dump(data, write_file)

matches_picked = []
managers_taken = []
data_y = []
with open("match.json", "w") as write_file:
    for i in range(itrs):
        if i % 1000 == 0: print (f"Match:  Iteration: {i}")
        #pick random match id
        m_id = random.choice(match_ids)
        match_ids.remove(m_id)

        #pick users reservations
        users_ids = []
        j = 0
        for dic in data:
            if dic['role'] == 'fan':
                for recv in dic['reservations']:
                    if m_id == dic['reservations'][recv]['match_id'] and dic['username'] not in users_ids:
                        users_ids.append(dic['_id'])
        
        #pick one random manager
        manager_user = random.choice(managers)

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
                        'width':randint(2, 15),
                        'height':randint(2, 15)
                    },
                    'line_men':{
                        'first':fake.profile()['name'],
                        'second':fake.profile()['name']
                    },
                    'manager_scheduled':manager_user,
                    'users_reserved':users_ids
                }
        data_y.append(my_dict)
    json.dump(data_y, write_file)


    
        

    
