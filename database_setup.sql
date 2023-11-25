CREATE DATABASE IF NOT EXISTS techmify_db01;
CREATE USER IF NOT EXISTS 'techyman02'@'localhost' IDENTIFIED BY 'Techy_200200';
GRANT ALL PRIVILEGES ON `techmify_db01`.* TO 'techyman02'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'techyman02'@'localhost';
FLUSH PRIVILEGES;