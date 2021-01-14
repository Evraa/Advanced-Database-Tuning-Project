CREATE SCHEMA match_reservation;

CREATE TABLE stadiums ( 
	id                   int  NOT NULL    PRIMARY KEY,
	width                int  NOT NULL    ,
	height               int  NOT NULL    ,
	name                 varchar(100)  NOT NULL    
 );

CREATE TABLE teams ( 
	id                   int  NOT NULL    PRIMARY KEY,
	name                 varchar(100)  NOT NULL    
 );

CREATE TABLE users ( 
	username             varchar(50)  NOT NULL    PRIMARY KEY,
	email                varchar(50)  NOT NULL    ,
	password             varchar(50)  NOT NULL    ,
	fname                varchar(50)  NOT NULL    ,
	lname                varchar(50)  NOT NULL    ,
	role                 varchar(10)  NOT NULL    ,
	bdate                date      ,
	gender               char(6)      ,
	city                 varchar(50)      
 );

CREATE TABLE matches ( 
	id                   int  NOT NULL    PRIMARY KEY,
	referee              varchar(50)      ,
	match_time           date  NOT NULL    ,
	first_lineman        varchar(50)      ,
	second_lineman       varchar(50)      ,
	stadium_id           int  NOT NULL    ,
	home_team            int  NOT NULL    ,
	away_team            int  NOT NULL    ,
	manager_scheduled    varchar(50)  NOT NULL    ,
	CONSTRAINT fk_matches_stadiums FOREIGN KEY ( stadium_id ) REFERENCES stadiums( id ) ON DELETE RESTRICT ON UPDATE RESTRICT,
	CONSTRAINT fk_matches_teams FOREIGN KEY ( away_team ) REFERENCES teams( id ) ON DELETE RESTRICT ON UPDATE RESTRICT,
	CONSTRAINT fk_matches_teams_0 FOREIGN KEY ( home_team ) REFERENCES teams( id ) ON DELETE RESTRICT ON UPDATE RESTRICT,
	CONSTRAINT fk_matches_users FOREIGN KEY ( manager_scheduled ) REFERENCES users( username ) ON DELETE RESTRICT ON UPDATE RESTRICT
 );

CREATE INDEX fk_matches_stadiums ON matches ( stadium_id );

CREATE INDEX fk_matches_teams ON matches ( away_team );

CREATE INDEX fk_matches_teams_0 ON matches ( home_team );

CREATE INDEX fk_matches_users ON matches ( manager_scheduled );

CREATE TABLE reservations ( 
	x                    int  NOT NULL    ,
	y                    int  NOT NULL    ,
	username             varchar(100)  NOT NULL    ,
	match_id             int  NOT NULL    ,
	CONSTRAINT fk_reservations_matches FOREIGN KEY ( match_id ) REFERENCES matches( id ) ON DELETE RESTRICT ON UPDATE RESTRICT,
	CONSTRAINT fk_reservations_users FOREIGN KEY ( username ) REFERENCES users( username ) ON DELETE RESTRICT ON UPDATE RESTRICT
 );

CREATE INDEX fk_reservations_matches ON reservations ( match_id );

CREATE INDEX fk_reservations_users ON reservations ( username );
