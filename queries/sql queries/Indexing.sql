/*
Unoptimized
*/

SELECT fname, lname 
FROM `users` AS U, `matches` AS M, `reservations` AS R, `teams` AS T 
WHERE R.match_id = M.id AND U.username = R.username AND M.home_team = T.id AND 
T.name = 'est' AND U.city = 'Port Leathaside';


/*
After Query Optimization
*/

SELECT fname, lname 
FROM `matches` AS M 
    INNER JOIN (SELECT id FROM `teams` WHERE name = 'est') AS T ON M.home_team = T.id 
    INNER JOIN `reservations` AS R ON R.match_id = M.id 
    INNER JOIN (SELECT fname, lname, username FROM `users` WHERE city = 'Port Leathaside') AS U ON R.username = U.username;

/*
Indexing City
*/

CREATE INDEX index_city ON `users` (city);

/*
Dropping Index
*/

DROP INDEX index_city ON `users`;




/*
Full SQL Queries:
    1- run the unoptimized and optimized queries and monitor the time of each
    2- create the index
    3- run the unoptimized and optimized queries with indexing and monitor the time of each
    4- drop the index
*/

SELECT fname, lname 
FROM `users` AS U, `matches` AS M, `reservations` AS R, `teams` AS T 
WHERE R.match_id = M.id AND U.username = R.username AND M.home_team = T.id AND 
T.name = 'est' AND U.city = 'Port Leathaside';

SELECT fname, lname 
FROM `matches` AS M 
    INNER JOIN (SELECT id FROM `teams` WHERE name = 'est') AS T ON M.home_team = T.id 
    INNER JOIN `reservations` AS R ON R.match_id = M.id 
    INNER JOIN (SELECT fname, lname, username FROM `users` WHERE city = 'Port Leathaside') AS U ON R.username = U.username;



CREATE INDEX index_city ON `users` (city);



SELECT fname, lname 
FROM `users` AS U, `matches` AS M, `reservations` AS R, `teams` AS T 
WHERE R.match_id = M.id AND U.username = R.username AND M.home_team = T.id AND 
T.name = 'est' AND U.city = 'Port Leathaside';

SELECT fname, lname 
FROM `matches` AS M 
    INNER JOIN (SELECT id FROM `teams` WHERE name = 'est') AS T ON M.home_team = T.id 
    INNER JOIN `reservations` AS R ON R.match_id = M.id 
    INNER JOIN (SELECT fname, lname, username FROM `users` WHERE city = 'Port Leathaside') AS U ON R.username = U.username;



DROP INDEX index_city ON `users`;
