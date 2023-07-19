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
  user integer,
  FOREIGN KEY(user) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY(object) REFERENCES objects(id) ON DELETE CASCADE 
);

create table actual_object(
  id integer primary key autoincrement,
  object integer,
  user integer,
  FOREIGN KEY(user) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY(object) REFERENCES objects(id) ON DELETE CASCADE 
);

