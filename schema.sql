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
	    
INSERT INTO CompanyDB(CName,SecurityNo,Limited_Stock_Exchange,Rate,No_of_shares)
VALUES
("Company1","9XGH12","NSE",56.7,10000),
("Company2","9XGH13","BSE",5,10000),
("Company3","9XGH14","BSE",6.9,10000),
("Company4","9XGH15","NSE",-8.7,10000);

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

Create table if not exists stock_customer(
SCode varchar(10) Not Null Unique,
CName VARCHAR(255)  NOT NULL,
quantity integer not null,
primary key(SCode, CName),
foreign key(SCode) references stocks(SCode),
FOREIGN KEY(CName) REFERENCES client_profile(username)
ON UPDATE CASCADE ON DELETE CASCADE);

Create table if not exists transactions(
T_ID varchar(5),
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
