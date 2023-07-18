create table users(
  id integer primary key,
  fname varchar(255) not null,
  lname varchar(255),
  user_type character(20)
);

create table objects(
  id integer primary key autoincrement,
  name varchar(255) unique
);

create table time(
  id integer primary key autoincrement,
  day text, 
  hours numeric,
  object integer,
  user integer
);

create table actual_object(
  object integer,
  user integer primary key
);

insert into objects (id, name)
values 
  (1, "Новосмоленская набережная 2 кв. 145");
  
insert into users (id, fname, lname, user_type)
values
  (441293054, "Максим", "Машков", "root");
