from faker import Faker
import random
from random import randint


USERS_NUM = 20000
TEAMS_NUM = 20
STADIUMS_NUM = 30
MATCHES_NUM = 400
DATES_COUNT = 400//2
RESERVATIONS_NUM = 1000000
MIN_STAD_SIZE = 100
MAX_STAD_SIZE = 500
CITY_NUM = 500

fake = Faker('en_US')

#get list of cities
_cities = []
for _ in range(CITY_NUM):
    city = fake.city()
    while city in _cities:
        city = fake.city()
    _cities.append(city)

managers = []
fans = []
usernames = set()
with open("users.csv", "w") as write_file:
    write_file.write('username,email,password,fname,lname,role,bdate,gender,city\n')
    for i in range(USERS_NUM):
        if i % 1000 == 0: 
            print (f"user:  Iteration: {i}")
        ev = random.randint(0, 2)

        role = 'manager' if (ev==0 or i==0) else 'fan'

        username = fake.user_name()
        while username in usernames:
            username = fake.user_name()
        usernames.add(username)

        if role == 'manager':
            managers.append(username)
        else:
            fans.append(username)
        
        data = [
            username,
            fake.profile()['mail'],
            fake.password(length=8),
            fake.first_name(),
            fake.last_name(),
            role,
            fake.date_time().strftime('%Y-%m-%d'),
            fake.profile()['sex'],
            random.choice(_cities)
        ]
        data = [str(d) for d in data]
        write_file.write(','.join(data)+'\n')

with open("teams.csv", "w") as write_file:
    write_file.write('id,name\n')
    for i in range(TEAMS_NUM):
        if i % 100 == 0:
            print (f"Team:  Iteration: {i}")

        data = [
            i+1,
            '"'+fake.profile()['company']+'"'
        ]
        data = [str(d) for d in data]
        write_file.write(','.join(data)+'\n')


stad_x_y = []
with open("stadiums.csv", "w") as write_file:
    write_file.write('id,width,height,name\n')
    for i in range(STADIUMS_NUM):
        stad_x_y.append((
            randint(MIN_STAD_SIZE, MAX_STAD_SIZE),
            randint(MIN_STAD_SIZE, MAX_STAD_SIZE)
        ))
        if i % 10 == 0:
            print (f"stadium:  Iteration: {i}")
        data = [
            i+1,
            stad_x_y[i][0],
            stad_x_y[i][1],
            fake.city()
        ]
        data = [str(d) for d in data]
        write_file.write(','.join(data)+'\n')
    
match_stadium = []
#unique dates but specific
_dates = []
for i in range (DATES_COUNT):
    date = fake.date_time().strftime('%Y-%m-%dT%H:%M')
    _dates.append(date)

with open("matches.csv", "w") as write_file:
    write_file.write('id,referee,match_time,first_lineman,second_lineman,stadium_id,home_team,away_team,manager_scheduled\n')
    for i in range(MATCHES_NUM):
        if i % 1000 == 0: 
            print (f"Match:  Iteration: {i}")

        #pick one random manager
        manager_user = random.choice(managers)

        #home team
        team_x = randint(1, TEAMS_NUM)
        team_y = randint(1, TEAMS_NUM)
        while team_x == team_y:
            team_y = randint(1, TEAMS_NUM)

        stad_id = randint(1, STADIUMS_NUM)
        match_stadium.append(stad_id)
        
        data = [
            i+1,
            fake.profile()['name'],
            random.choice(_dates),
            fake.profile()['name'],
            fake.profile()['name'],
            stad_id,
            team_x,
            team_y,
            manager_user
        ]
        data = [str(d) for d in data]
        write_file.write(','.join(data))
        write_file.write('\n')

reserve_info = set()

with open("reservations.csv", "w") as write_file:
    write_file.write('x,y,username,match_id\n')
    for i in range(RESERVATIONS_NUM):
        if i % 1000 == 0:
            print(f"Reservation: Iteration: {i}")

        fan = random.choice(fans)
        while True:
            match_id = randint(1, MATCHES_NUM)
            x = randint(0, stad_x_y[match_stadium[match_id-1]-1][0])
            y = randint(0, stad_x_y[match_stadium[match_id-1]-1][1])
            if (match_id, x, y) not in reserve_info:
                break
        reserve_info.add((match_id, x, y))

        data = [
            x,
            y,
            fan,
            match_id
        ]
        data = [str(d) for d in data]
        write_file.write(','.join(data)+'\n')
