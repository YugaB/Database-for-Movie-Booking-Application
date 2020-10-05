DROP DATABASE IF EXISTS cmpe226;
CREATE DATABASE cmpe226;
USE cmpe226;

CREATE TABLE IF NOT EXISTS user(
uid INT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(60) NOT NULL,
email VARCHAR(100) NOT NULL UNIQUE,
password CHAR(100) NOT NULL,
role VARCHAR(60) NOT NULL,
discount INT(60) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS theater(
tid INT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
tname VARCHAR(60) NOT NULL UNIQUE,
address VARCHAR(60) NOT NULL,
state VARCHAR(60) NOT NULL,
city VARCHAR(60) NOT NULL,
phone VARCHAR(60) NOT NULL,
admin_id int(60) NOT NULL REFERENCES user(uid)
);

CREATE TABLE IF NOT EXISTS screen(
show_id INT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
tid INT(20) NOT NULL REFERENCES theater(tid),
scid INT(20) NOT NULL,
mid INT(20) NOT NULL,
show_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS screenSeats(
tid INT(20) NOT NULL REFERENCES theater(tid),
scid INT(20) NOT NULL REFERENCES screen(scid),
total_seats INT(20) NOT NULL,
PRIMARY KEY (tid, scid)
);

CREATE TABLE IF NOT EXISTS movie(
mid INT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
mname VARCHAR(60) NOT NULL,
genre VARCHAR(60) NOT NULL,
price FLOAT NOT NULL,
duration INT(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS show_time(
show_id int(20) NOT NULL REFERENCES screen(show_id),
show_time TIME NOT NULL,
primary key(show_id, show_time)
);

CREATE TABLE IF NOT EXISTS seat(
seat_id VARCHAR(60) NOT NULL,
status VARCHAR(60),
show_time TIME,
show_id INT(20) REFERENCES screen(show_id),
uid INT(20) REFERENCES user(uid),
primary key(seat_id, show_id, uid, show_time)
);

DELIMITER $$
CREATE TRIGGER checkPrice BEFORE INSERT ON movie
FOR EACH ROW
BEGIN
IF NEW.price < 12.0 THEN
SET NEW.price = 12.0;
END IF;
END $$
DELIMITER ;

CREATE VIEW initialMovieSearch AS
SELECT movie.mname, movie.genre, movie.mid, theater.tname, theater.address, theater.state, theater.city, theater.tid, screen.show_date
FROM movie JOIN screen ON movie.mid=screen.mid JOIN theater ON theater.tid=screen.tid;


DELIMITER $$

DROP PROCEDURE IF EXISTS show_times_sp$$
CREATE PROCEDURE show_times_sp(IN theaterID INT, IN movieID INT, IN showDate VARCHAR(60), OUT show_id INT, OUT show_time TIME)
BEGIN
    SELECT show_time.show_id, show_time.show_time
    FROM show_time JOIN screen ON screen.show_id=show_time.show_id
    WHERE tid=theaterID AND mid=movieID AND show_date=showDate;
END$$

DELIMITER ;



DELIMITER $$

DROP PROCEDURE IF EXISTS Get_movie_detail_sp$$
CREATE PROCEDURE Get_movie_detail_sp(IN city_name varchar(255), IN search_date varchar(255), 
                                     IN search_movie varchar(255), IN search_theater varchar(255), 
                                     IN search_genre varchar(255))
BEGIN
    IF search_theater = '' AND search_genre = '' THEN
        SELECT mname, genre, mid, tname, address, state, city, tid
        FROM initialMovieSearch
        WHERE city=city_name AND show_date=search_date AND mname=search_movie ;
                                                             
    ELSEIF search_movie = '' AND search_genre = '' THEN
        SELECT mname, genre, mid, tname, address, state, city, tid
        FROM initialMovieSearch
        WHERE city=city_name AND show_date=search_date AND tname=search_theater;
                                                             
    ELSEIF search_movie = '' AND search_theater = '' THEN
        SELECT mname, genre, mid, tname, address, state, city, tid
        FROM initialMovieSearch
        WHERE city=city_name AND show_date=search_date AND genre=search_genre;
                                                             
    ELSE
        SELECT mname, genre, mid, tname, address, state, city, tid
        FROM initialMovieSearch
        WHERE city=city_name AND show_date=search_date AND tname=search_theater 
                                 AND mname=search_movie AND genre=search_genre;
    END IF;
                                                             
END$$

DELIMITER ;

ALTER TABLE seat ADD INDEX (show_id);
ALTER TABLE seat ADD INDEX (show_time);
