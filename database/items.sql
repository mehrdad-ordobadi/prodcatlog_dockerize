CREATE DATABASE IF NOT EXISTS db;
USE db;

CREATE TABLE IF NOT EXISTS item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    UNIQUE KEY unique_name (name)
);

-- Replace 'newuser' and 'userpassword' with your desired username and password
CREATE USER IF NOT EXISTS 'newuser'@'%' IDENTIFIED BY 'userpassword';
GRANT ALL PRIVILEGES ON db.* TO 'newuser'@'%';
FLUSH PRIVILEGES;