SELECT fname, lname
FROM `users` AS U, `reservations` AS R
WHERE U.username = R.username and R.x > 400 AND R.y > 400;

CREATE INDEX index_seat ON `reservations` (x, y);

SELECT fname, lname
FROM `users` AS U, `reservations` AS R
WHERE U.username = R.username and R.x > 400 AND R.y > 400;