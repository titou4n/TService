import sqlite3
import os
from flask import abort
import datetime

class DatabaseHandler():
  def get_db_connection():
    conn = sqlite3.connect('Data\database.db')
    conn.row_factory = sqlite3.Row
    return conn

  def number_account(self):
    conn = sqlite3.connect('Data\database.db')
    conn.row_factory = sqlite3.Row
    query = f"SELECT * FROM account"
    number_account = len(conn.execute(query).fetchall())
    conn.close()
    return number_account

  def date_connected(self, id:str, date_connected:datetime, ipv4:int ):
    conn = sqlite3.connect('Data\database.db')
    query = f"INSERT INTO metadata (date_connected, id, ipv4) VALUES (?,?,?);"
    conn.execute(query, (date_connected, id, ipv4))
    conn.commit()
    conn.close()

  def create_account(self, username, password, name):
    conn = sqlite3.connect('Data\database.db')
    conn.execute('INSERT INTO account (username, password, name) VALUES (?, ?, ?)',(username, password, name))
    conn.commit()
    conn.close()

  def delete_account(self, id):
    conn = sqlite3.connect('Data\database.db')
    conn.execute('DELETE FROM account WHERE id = ?', (id,))
    conn.commit()
    conn.close()
  
  def change_password(self, id, new_password):
    conn = sqlite3.connect('Data\database.db')
    query = f"UPDATE account SET password=?, nbpasswordchange=nbpasswordchange+1 WHERE id=?;"
    conn.execute(query, (new_password,id))
    conn.commit()
    conn.close()
  
  def change_name(self, id, new_name):
    conn = sqlite3.connect('Data\database.db')
    query = f"UPDATE account SET name=?, nbnamechange=nbnamechange+1 WHERE id=?;"
    conn.execute(query, (new_name,id))
    conn.commit()
    conn.close()

  def change_name_in_post(self, id, new_name):
    conn = sqlite3.connect('Data\database.db')
    conn.execute('UPDATE posts SET name = ?'' WHERE id = ?', (new_name, id))
    conn.commit()
    conn.close()
    
  def id_db(self, username:str) -> bool:
    conn = sqlite3.connect('Data\database.db')
    conn.row_factory = sqlite3.Row
    query = f"SELECT id FROM account WHERE username=?;"
    result = conn.execute(query, (username,))
    result = result.fetchall()
    conn.close()
    return dict(result[0])["id"]

  def password_db(self, id:int) -> bool:
    conn = sqlite3.connect('Data\database.db')
    conn.row_factory = sqlite3.Row
    query = f"SELECT password FROM account WHERE id=?;"
    result = conn.execute(query, (id,))
    result = result.fetchall()
    conn.close()
    return dict(result[0])["password"]

  def name_db(self, id:int) -> bool:
    conn = sqlite3.connect('Data\database.db')
    conn.row_factory = sqlite3.Row
    query = f"SELECT name FROM account WHERE id=?;"
    result = conn.execute(query, (id,))
    result = result.fetchall()
    conn.close()
    return dict(result[0])["name"]

  def user_exists_with(self, username:str) -> bool:
    conn = sqlite3.connect('Data\database.db')
    conn.row_factory = sqlite3.Row
    query = f"SELECT * FROM account WHERE username=?;"
    result = conn.execute(query, (username,)).fetchall()
    conn.close()
    return len(result)==1

  def name_exists_with(self, name:str) -> bool:
    conn = sqlite3.connect('Data\database.db')
    conn.row_factory = sqlite3.Row
    query = f"SELECT * FROM account WHERE name=?;"
    result = conn.execute(query, (name,)).fetchall()
    conn.close()
    return len(result)==1

  def pay_db(self, id:str) -> bool:
    conn = sqlite3.connect('Data\database.db')
    conn.row_factory = sqlite3.Row
    query = f"SELECT pay FROM account WHERE id=?;"
    result = conn.execute(query, (id,)).fetchall()
    conn.close()
    return dict(result[0])["pay"]

  def new_pay_db(self, id:str, new_pay:str):
    conn = sqlite3.connect('Data\database.db')
    conn.row_factory = sqlite3.Row
    query = f"UPDATE account SET pay=? WHERE id=?;"
    conn.execute(query, (new_pay,id))
    conn.commit()
    conn.close()
    

  def post_in_chatroom(self):
    conn = sqlite3.connect('Data\database.db')
    conn.row_factory = sqlite3.Row
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return posts
  
  def get_post(self, id_post):
      conn = sqlite3.connect('Data\database.db')
      conn.row_factory = sqlite3.Row
      post = conn.execute('SELECT * FROM posts WHERE id_post = ?',(id_post,)).fetchone()
      conn.close()
      if post is None:
          abort(404)
      return post

  def create_post(self, id, name, title, content):
    conn = sqlite3.connect('Data\database.db')
    conn.execute('INSERT INTO posts (id, name, title, content) VALUES (?, ?, ?, ?)',(id, name, title, content))
    conn.commit()
    conn.close()

  def edit_post(self, id_post, name, title, content):
    conn = sqlite3.connect('Data\database.db')
    conn.execute('UPDATE posts SET name = ?, title = ?, content = ?'' WHERE id_post = ?', (name, title, content, id_post))
    conn.commit()
    conn.close()

  def delete_post(self, id_post):
    conn = sqlite3.connect('Data\database.db')
    conn.execute('DELETE FROM posts WHERE id_post = ?', (id_post,))
    conn.commit()
    conn.close()

  def insert_movie_search(self, id, movie_title, date_movie_search:datetime):
    conn = sqlite3.connect('Data\database.db')
    query = f"INSERT INTO movie_search (id, movie_title, date_movie_search) VALUES (?,?,?);"
    conn.execute(query, (id, movie_title, date_movie_search))
    conn.commit()
    conn.close()

  def all_movie_search(self, id):
    conn = sqlite3.connect('Data\database.db')
    conn.row_factory = sqlite3.Row
    movie_search = conn.execute('SELECT * FROM movie_search WHERE id=id').fetchall()
    conn.close()
    return movie_search

  


