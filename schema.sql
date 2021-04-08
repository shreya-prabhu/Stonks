DROP DATABASE if exists stonks;
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
No_of_shares int(11) NOT NULL,
PRIMARY KEY(CName));

INSERT INTO CompanyDB(CName,SecurityNo,Limited_Stock_Exchange,No_of_shares)
VALUES
("Company1","9XGH12","NSE",10000),
("Company2","9XGH13","BSE",10000),
("Company3","9XGH14","BSE",10000),
("Company4","9XGH15","NSE",10000);

CREATE TABLE if not exists client_profile(
FName VARCHAR(255)  NOT NULL,
DOB date,
email_id varchar(40) unique not null,
phone_no varchar(10) unique not null,
username varchar(15) unique NOT NULL,
password varchar(20) not null,
aadhar_no varchar(12) unique not null,
pan_no varchar(10) unique not null,
security_code varchar(20) not null,
DP_ID varchar(10) not null,
Bank_acc_no varchar(10) not null unique,
PRIMARY KEY(username));

INSERT INTO client_profile(FName,email_id,phone_no,username,password,aadhar_no,pan_no,security_code,
DP_ID,Bank_acc_no)
VALUES('moo','m@gmail.com',12,'moo','moo','1','1','1','1','1');

INSERT INTO client_profile(FName,email_id,phone_no,username,password,aadhar_no,pan_no,security_code,
DP_ID,Bank_acc_no)
VALUES('boo','b@gmail.com',112,'boo','boo','2','2','2','2','2');


Create table if not exists bank_details(
BName Varchar(255) Not NULL,
Bank_acc_no varchar(10) not null unique,
bank_ifsc_no varchar(12) not null,
account_type varchar(20) not null,
PRIMARY KEY(Bank_acc_no),
FOREIGN KEY (Bank_acc_no) REFERENCES client_profile(Bank_acc_no)
ON UPDATE CASCADE ON DELETE CASCADE);

Create table if not exists stocks(
SCode varchar(10) Not Null Unique,
CName VARCHAR(255)  NOT NULL UNIQUE,
SDescription Varchar(255),
Price float(2)  not null,
Primary Key(SCode),
FOREIGN KEY (CName) REFERENCES CompanyDB(CName)
ON UPDATE CASCADE ON DELETE CASCADE);

INSERT INTO stocks(SCode,CName,SDescription,Price) VALUES ('CT1','Company1','NULL',12.3);
INSERT INTO stocks(SCode,CName,SDescription,Price) VALUES ('CT2','Company2','Market Rate',82.43);
INSERT INTO stocks(SCode,CName,SDescription,Price) VALUES ('CT3','Company3','Market Rate',312.53);
INSERT INTO stocks(SCode,CName,SDescription,Price) VALUES ('CT4','Company4','Market Rate',212.3);

-- -- Create table if not exists transactions(
-- -- T_ID varchar(5),
-- -- CName VARCHAR(255)  NOT NULL,
-- -- T_Time time,
-- -- T_Date date,
-- -- T_type varchar(10),
-- -- SCode varchar(10) Not Null,
-- -- Quantity integer,
-- -- primary key(T_ID),
-- -- foreign key(SCode) references stocks(SCode),
-- -- FOREIGN KEY(CName) REFERENCES client_profile(username)
-- -- ON UPDATE CASCADE ON DELETE CASCADE);

-- -- INSERT INTO transactions(T_ID,CName,T_Time,T_Date,T_Type,SCode,Quantity) VALUES ('0','moo','12:12:12','2000-01-01','Buy','CT1',4);
-- -- INSERT INTO transactions(T_ID,CName,T_Time,T_Date,T_Type,SCode,Quantity) VALUES ('1','moo','12:12:12','2000-01-01','Sell','CT1',4);
-- -- INSERT INTO transactions(T_ID,CName,T_Time,T_Date,T_Type,SCode,Quantity) VALUES ('2','moo','12:12:12','2000-01-01','Buy','CT1',4);
-- -- INSERT INTO transactions(T_ID,CName,T_Time,T_Date,T_Type,SCode,Quantity) VALUES ('3','boo','12:12:12','2000-01-01','Buy','CT2',4);
-- -- INSERT INTO transactions(T_ID,CName,T_Time,T_Date,T_Type,SCode,Quantity) VALUES ('4','moo','12:12:12','2000-01-01','Buy','CT3',4);
-- Create table if not exists stock_customer(
-- SCode varchar(10) Not Null,
-- CName VARCHAR(255)  NOT NULL,
-- quantity integer not null,
-- primary key(SCode, CName),
-- foreign key(SCode) references stocks(SCode),
-- FOREIGN KEY(CName) REFERENCES client_profile(username)
-- ON UPDATE CASCADE ON DELETE CASCADE);

-- Create table if not exists transactions(
-- T_ID integer not null auto_increment,
-- CName VARCHAR(255)  NOT NULL,
-- T_Time time,
-- T_Date date,
-- T_type varchar(10),
-- SCode varchar(10) Not Null,
-- Quantity integer,
-- primary key(T_ID),
-- foreign key(SCode) references stocks(SCode),
-- FOREIGN KEY(CName) REFERENCES client_profile(username)
-- ON UPDATE CASCADE ON DELETE CASCADE);

-- DELIMITER //
-- CREATE TRIGGER display_stock_changes 
-- BEFORE UPDATE ON CompanyDB FOR EACH ROW 
-- BEGIN  
-- 	IF OLD.No_of_shares <= 200 THEN 
--     SIGNAL SQLSTATE '45000'
-- 	SET MESSAGE_TEXT = 'Share not available';
--     END IF;
-- END;//
-- DELIMITER ;

Create table if not exists stock_customer(
SCode varchar(10) Not Null,
CName VARCHAR(255)  NOT NULL,
quantity integer not null,
primary key(SCode, CName),
foreign key(SCode) references stocks(SCode),
FOREIGN KEY(CName) REFERENCES client_profile(username)
ON UPDATE CASCADE ON DELETE CASCADE);

Create table if not exists transactions(
T_ID integer not null auto_increment,
CName VARCHAR(255)  NOT NULL,
T_Time time,
T_Date date,
T_type varchar(10),
SCode varchar(10) Not Null,
Quantity integer,
primary key(T_ID),
foreign key(SCode) references stocks(SCode),
FOREIGN KEY(CName) REFERENCES client_profile(username)
ON UPDATE CASCADE ON DELETE CASCADE);

DELIMITER //
CREATE TRIGGER display_stock_changes 
BEFORE UPDATE ON CompanyDB FOR EACH ROW 
BEGIN  
	IF OLD.No_of_shares <= 200 THEN 
    SIGNAL SQLSTATE '45000'
	SET MESSAGE_TEXT = 'Share not available';
    END IF;
END;//
DELIMITER ;