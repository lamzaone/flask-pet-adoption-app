CREATE TABLE user (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT NOT NULL
);


CREATE TABLE animals (
  id TEXT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  name TEXT NOT NULL,
  user_id TEXT,
  kind TEXT NOT NULL,
  breed TEXT,
  sex TEXT,
  age TEXT,
  description TEXT,
  img_url TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id)
);