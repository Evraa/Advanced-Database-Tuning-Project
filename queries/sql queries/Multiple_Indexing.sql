/*
Unoptimized
*/

SELECT fname, lname
FROM `users` AS U, `reservations` AS R
WHERE U.username = R.username AND R.x = 367 AND R.y = 400;


/*
After Query Optimization
*/

SELECT fname, lname 
FROM `users` AS U 
    INNER JOIN (SELECT username From `reservations` WHERE x = 367 AND y = 400) AS R ON U.username = R.username;

/*
Indexing Seat
*/

CREATE INDEX index_seat ON `reservations` (x, y);

/*
Dropping Index
*/

DROP INDEX index_seat ON `reservations`;




/*
Full SQL Queries:
    1- run the unoptimized and optimized queries and monitor the time of each
    2- create the index
    3- run the unoptimized and optimized queries with multiple indexing and monitor the time of each
    4- drop the index
*/


SELECT fname, lname
FROM `users` AS U, `reservations` AS R
WHERE U.username = R.username AND R.x = 367 AND R.y = 400;

SELECT fname, lname 
FROM `users` AS U 
    INNER JOIN (SELECT username From `reservations` WHERE x = 367 AND y = 400) AS R ON U.username = R.username;


CREATE INDEX index_seat ON `reservations` (x, y);


SELECT fname, lname
FROM `users` AS U, `reservations` AS R
WHERE U.username = R.username AND R.x = 367 AND R.y = 400;

SELECT fname, lname 
FROM `users` AS U 
    INNER JOIN (SELECT username From `reservations` WHERE x = 367 AND y = 400) AS R ON U.username = R.username;


DROP INDEX index_seat ON `reservations`;
