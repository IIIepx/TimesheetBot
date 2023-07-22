create table users(
  id integer primary key,
  name varchar(255) not null,
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

CREATE VIEW summary 
AS           
SELECT users.id AS id,                        
users.name AS name,    
objects.name AS object,                       
time.day AS day,                              
time.hours AS hours                           
FROM time                                     
INNER JOIN users ON time.user = users.id      
INNER JOIN objects ON time.object = objects.id
;
