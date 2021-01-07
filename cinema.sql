CREATE DATABASE cinema;

CREATE TABLE users (
    userid INT NOT NULL PRIMARY KEY,
    name varchar(50),
    gender varchar(10),
    age INT,
    phn_no varchar(15),
    ticketid INT
);

CREATE TABLE ticketsinfo(
    ticketid INT NOT NULL PRIMARY KEY,
    rowno INT,
    columnno INT,
    price INT
);