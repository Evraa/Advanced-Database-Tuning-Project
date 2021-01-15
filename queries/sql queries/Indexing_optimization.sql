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