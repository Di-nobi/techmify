CREATE DATABASE IF NOT EXISTS techmify_db01;
CREATE USER IF NOT EXISTS 'first_usr'@'localhost' IDENTIFIED BY '123';
GRANT ALL PRIVILEGES ON techmify_db01 . * TO 'first_usr'@'localhost';
GRANT SELECT ON performance_schema . * TO 'first_usr'@'localhost';
FLUSH PRIVILEGES