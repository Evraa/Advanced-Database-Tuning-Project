/*
Unoptimized
*/

SELECT fname, lname 
FROM `users` AS U, `reservations` AS R 
WHERE U.username = R.username AND R.y = 21;


/*
After Schema Optimization
*/

SELECT fname, lname 
FROM `users` AS U, `reservations` AS R 
WHERE U.id = R.user_id AND R.y = 21;

