DELIMITER $$

DROP PROCEDURE IF EXISTS Get_movie_detail_sp;

DELIMITER $$
CREATE PROCEDURE `Get_movie_detail_sp`(In city_name varchar(255), In search_date date, 
                                       IN search_movie varchar(255),IN search_theater varchar(255), IN search_genre varchar(255))
BEGIN
	IF search_theater = '' and search_genre = '' then
		select mname, tname, address, city, state, tid, mid, show_date
		from initialMovieSearch
		where city = city_name and show_date = search_date and mname = search_movie ;
            
	ELSEIF search_movie = '' and search_genre = '' then
		select mname, tname, address, city, state, tid, mid, show_date
		from initialMovieSearch
		where city = city_name and show_date = search_date and tname = search_theater;
            
	ELSEIF search_movie = '' and search_theater = '' then
		select mname, tname, address, city, state, tid, mid, show_date
		from initialMovieSearch
		where city = city_name and show_date = search_date and genre = search_genre;

    ELSE 
		select mname, tname, address, city, state, tid, mid, show_date
		from initialMovieSearch
		where city = city_name and show_date = search_date and tname = search_theater 
						and mname = search_movie and genre = search_genre;
    	END if;    
END
