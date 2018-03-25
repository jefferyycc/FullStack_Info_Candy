"""
need to update
"""

drop table if exists users;
create table users(
  """
  user_id integer primary key,
  first_name text not null,
  last_name text not null,
  username text not null,
  password text not null
  """
);
