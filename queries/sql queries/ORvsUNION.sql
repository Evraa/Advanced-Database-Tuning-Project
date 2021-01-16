/*
Unoptimized
*/

SELECT fname, lname 
FROM `users` AS U, `matches` AS M, `reservations` AS R, `teams` AS T 
WHERE R.match_id = M.id AND U.username = R.username AND M.home_team = T.id AND 
T.name = 'est' AND (U.city = 'Port Leathaside' or U.fname = 'Michael');


/*
After Query Optimization
*/

SELECT fname, lname 
FROM `matches` AS M 
    INNER JOIN (SELECT id FROM `teams` WHERE name = 'est') AS T ON M.home_team = T.id 
    INNER JOIN `reservations` AS R ON R.match_id = M.id 
    INNER JOIN (
        (SELECT fname, lname, username FROM `users` WHERE city = 'Port Leathaside') UNION
        (SELECT fname, lname, username FROM `users` WHERE fname = 'Michael')
    ) AS U ON R.username = U.username;

/*
Indexing City and fname
*/

CREATE INDEX index_city ON `users` (city);
CREATE INDEX index_fname ON `users` (fname);

/*
Dropping Indexes
*/

DROP INDEX index_city ON `users`;
DROP INDEX index_fname ON `users`;




/*
Full SQL Queries:
    1- run the unoptimized query and monitor its time
    2- create the indexes
    3- run the optimized query with indexing and monitor its time
    4- drop the indexes
*/

SELECT fname, lname 
FROM `users` AS U, `matches` AS M, `reservations` AS R, `teams` AS T 
WHERE R.match_id = M.id AND U.username = R.username AND M.home_team = T.id AND 
T.name = 'est' AND (U.city = 'Port Leathaside' or U.fname = 'Michael');



CREATE INDEX index_city ON `users` (city);
CREATE INDEX index_fname ON `users` (fname);



SELECT fname, lname 
FROM `matches` AS M 
    INNER JOIN (SELECT id FROM `teams` WHERE name = 'est') AS T ON M.home_team = T.id 
    INNER JOIN `reservations` AS R ON R.match_id = M.id 
    INNER JOIN (
        (SELECT fname, lname, username FROM `users` WHERE city = 'Port Leathaside') UNION
        (SELECT fname, lname, username FROM `users` WHERE fname = 'Michael')
    ) AS U ON R.username = U.username;




DROP INDEX index_city ON `users`;
DROP INDEX index_fname ON `users`;
