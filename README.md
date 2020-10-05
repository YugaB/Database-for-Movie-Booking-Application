## Movie Booking Application

### To Run Application 

```
cd cmpe226
pip install -r requirements.txt
python server.py
```

---

### Technologies:

#### Front-end:
```
- Jinja
- HTML
```

#### Back-end:
```
- Python
- Flask
```

#### Database:
```
- MySQL (AWS RDS)
- MongoDB (Atlas)
```

---

### Login Details

###### User Login

| Name          | Email                     | Password   |
|---------------| ------------------------- | -----------|
| User1         | user1@gmail.com           | User1      |

###### Owner Login

| Name          | Email                | Password        |
|---------------| ---------------------| ----------------|
| Admin1        | admin1@gmail.com     | Admin1          |
| Admin2        | admin2@gmail.com     | Admin2          |
| TestAdmin     | testadmin@gmail.com  | TestAdmin       |

---

### Data Details

1. Currently the database contains data for San Francisco and San Jose city.
2. With in following date range: 2019-06-01 to 2019-06-11

Examples:

![example1](static/images/example1.png)

![example2](static/images/example2.png)
=======
# Database-for-Movie-Booking-Application
Designed and developed relational and non-relational databases for Movie Booking Application
## Databases Used:
1. MySQL (AWS RDS)
2. Mongodb Atlas

## Steps followed for designing database:
1. Used MySQL database to store relational data such as users, admin, movies, theaters, screens, seats.
2. Created ERD and performed entity relational mapping
3. Designed and developed MySQL database schema. 
4. Wrote SQL queries to create database objects such as tables with Primary keys, foreign keys, indexes.
5. Created stored procedure, view and triggers.
6. Maintained tables in 3NF.
7. Stored data such as ratings and reviews for moviews and theaters in MongoDB using Atlas.

