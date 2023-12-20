CREATE DATABASE IF NOT EXISTS weatherApp;

USE weatherApp;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    APIkey VARCHAR(100) NOT NULL
);