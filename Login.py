# Made by GraddZero 
# Created on: 29/06/2021
# Updated 01/07/2020

#imports required modules
import hashlib
import sqlite3

# conn = sqlite3.connect('auth.db')
# cursor = conn.cursor()
# cursor.execute("""CREATE TABLE users (
# 	username text,	
# 	password text,
# 	privileged integer,
# 	id integer not null primary key autoincrement
# )""")
# cursor.execute("INSERT into users VALUES ('admin','SHA256HASH',1,NULL)")
# conn.commit()
# conn.close()

def admin_authenticate():
	username = input("Input privileged user's username: ")
	password = bytes(input("Enter Privileged User's Password: "), encoding='utf8')
	hash = password.hexdigest()
	conn = sqlite3.connect('auth.db')
	c = conn.cursor()
	c.execute(f"SELECT * FROM users WHERE username='{username}' AND privileged=1")
	entries = c.fetchone()
	if entries is None:
		conn.commit()
		conn.close()
		return 0
	elif entries[1] == hash:	
		conn.commit()
		conn.close()
		print("Authorised.")
		return 1
	else:
		print("Incorrect Password.")
		return 0

def new_prived_user(username, hash):
	isPriv = admin_authenticate()
	if isPriv == 1:
		hash = hash.hexdigest()
		conn = sqlite3.connect('auth.db')
		c = conn.cursor()
		c.execute(f"SELECT * FROM users WHERE username='{username}'")
		entries = c.fetchone()
		if entries is None:
			c.execute(f"INSERT into users VALUES ('{username}','{hash}',1,NULL)")
			conn.commit()
			conn.close()
			return "Account created."
		if entries[0] == username:
			conn.commit()
			conn.close()
			return "Username already in use"
	elif isPriv == 0:
		print("Username Incorrect or User isn't privileged.")

def new_user(username, hash):
	hash = hash.hexdigest()
	conn = sqlite3.connect('auth.db')
	c = conn.cursor()
	c.execute(f"SELECT * FROM users WHERE username='{username}'")
	entries = c.fetchone()
	if entries is None:
		c.execute(f"INSERT INTO users VALUES ('{username}','{hash}',0,NULL)")
		conn.commit()
		conn.close()
		return "Account created."
	if entries[0] == username:
		conn.commit()
		conn.close()
		return "Username already in use"
	
def login(username, hash):
	hash = hash.hexdigest()
	conn = sqlite3.connect('auth.db')
	c = conn.cursor()
	c.execute(f"SELECT * FROM users WHERE username='{username}'")
	entries = c.fetchone()
	if entries is None:
		conn.commit()
		conn.close()
		return 0
	elif entries[1] == hash:	
		conn.commit()
		conn.close()
		return 1
	else:
		return 0

def get_creds():
	username = input("Enter username: ")
	conn = sqlite3.connect('auth.db')
	c = conn.cursor()
	c.execute(f"SELECT * FROM users WHERE username='{username}'")
	entries = c.fetchone()
	conn.commit()
	conn.close()
	return f"""Username: {entries[0]}\nHash: {entries[1]}\nUnique Identifier: {entries[2]}"""
	
def delete_user_by_id(id):
	isPriv = admin_authenticate()
	if isPriv == 1:
		conn = sqlite3.connect('auth.db')
		c = conn.cursor()
		c.execute(f"DELETE FROM users WHERE id='{id}'")
		conn.commit()
		conn.close()
	elif isPriv == 0:
		print("Username Incorrect or User isn't privileged.")

def delete_user_by_name(username):
	isPriv = admin_authenticate()
	if isPriv == 1:
		conn = sqlite3.connect('auth.db')
		c = conn.cursor()
		c.execute(f"DELETE FROM users WHERE username='{username}'")
		conn.commit()
		conn.close()
	elif isPriv == 0:
		print("Username Incorrect or User isn't privileged.")

def sha256hash(text):
	text = str(text)
	password = hashlib.sha256(bytes(text, encoding='utf8'))
	hash = password.hexdigest()
	print(hash)

#password = hashlib.sha256(bytes(input("Enter Password: "), encoding='utf8'))
