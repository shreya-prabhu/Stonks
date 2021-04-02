CREATE DATABASE if not exists stonks;
USE stonks;
DROP TABLE if exists admin_profile;
DROP TABLE if exists CompanyDB;
CREATE TABLE admin_profile(
id int(11) NOT NULL UNIQUE,
username VARCHAR(255)  NOT NULL,
password VARCHAR(25) NOT NULL ,
PRIMARY KEY(username));
INSERT INTO admin_profile(id,username,password)
VALUES
("1","A","password");
INSERT INTO admin_profile(id,username,password)
VALUES
("2","B@gmail.com","password");
CREATE TABLE CompanyDB(
CName VARCHAR(255)  NOT NULL UNIQUE,
SecurityNo VARCHAR(50) NOT NULL UNIQUE ,
Limited_Stock_Exchange  VARCHAR(255) NOT NULL,
Rate float(11) NOT NULL,
No_of_shares int(11) NOT NULL,
PRIMARY KEY(CName));
INSERT INTO CompanyDB(CName,SecurityNo,Limited_Stock_Exchange,Rate,No_of_shares)
VALUES
("Company1","9XGH12","1AAAAAA",56.7,178),
("Company2","9XGH13","ddddAAA",5,11),
("Company3","9XGH14","hhsjwj",6.9,10000),
("Company4","9XGH15","1AAAAAA",-8.7,500);
