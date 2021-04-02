CREATE DATABASE if not exists stonks;
USE stonks;

CREATE TABLE admin_profile(
id int(11) NOT NULL,
username VARCHAR(255)  NOT NULL,
password VARCHAR(25) NOT NULL ,
PRIMARY KEY(username));
INSERT INTO admin_profile(id,username,password)
VALUES
("1","A","password");
