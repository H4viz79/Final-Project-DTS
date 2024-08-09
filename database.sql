CREATE DATABASE data_perpustakaan;
USE data_perpustakaan;

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    year_published YEAR,
    genre VARCHAR(255),
    date_added DATE
);