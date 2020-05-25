CREATE VIEW initialMovieSearch AS
SELECT movie.mname, movie.genre, movie.mid, theater.tname, theater.address, theater.state, theater.city, theater.tid, screen.show_date
FROM movie JOIN screen ON movie.mid=screen.mid JOIN theater ON theater.tid=screen.tid;

