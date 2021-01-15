/*
Unoptimized
*/

SELECT fname, lname 
FROM `users` AS U, `reservations` AS R 
WHERE U.username = R.username AND R.y = 21;


/*
After Query Optimization
*/

SELECT fname, lname 
FROM `users` AS U
    INNER JOIN ( SELECT username FROM `reservations` WHERE y = 21 ) AS R ON U.username = R.username;
