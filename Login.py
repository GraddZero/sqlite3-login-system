# Made by GraddZero 
# Created on: 29/06/2021

#imports required modules
import hashlib
import sqlite3

# First time init
# Username is the username field
# Password is a hashed sha256 password in this instance though variations can be made
# privileged in an integer that should either be a 1 or a 0. Alterations can be made to have different levels of privilege across system.
# id is a unique number associated with each entry.
# in the cursor.execute(username, password, privileged, null) entry below, change password to a hashed sha256 pass. Keep rest the same.

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
	c.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}' AND privileged=1")
	entries = c.fetchone()
	if entries is None:
		conn.commit()
		conn.close()
		return 0
	else:	
		conn.commit()
		conn.close()
		print("Authorised.")
		return 1

def new_user(username, hash):
	hash = hash.hexdigest()
	conn = sqlite3.connect('auth.db')
	c = conn.cursor()
	c.execute(f"SELECT * FROM users WHERE username='{username}'")
	entries = c.fetchone()
	if entries is None:
		c.execute(f"INSERT into users VALUES ('{username}','{hash}',0,NULL)")
		conn.commit()
		conn.close()
		return "Account created."
	if entries[0] == username:
		conn.commit()
		conn.close()
		return "Username already in use"
	
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
		print("Credentials incorrect or User isn't privileged.")


def login(username, hash):
	hash = hash.hexdigest()
	conn = sqlite3.connect('auth.db')
	c = conn.cursor()
	c.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{hash}'")
	entries = c.fetchone()
	if entries is None:
		conn.commit()
		conn.close()
		return "Username or Password is incorrect."
	else:	
		conn.commit()
		conn.close()
		return "Login Authorised."

def get_creds():
	username = input("Enter username: ")
	conn = sqlite3.connect('auth.db')
	c = conn.cursor()
	c.execute(f"SELECT * FROM users WHERE username='{username}'")
	entries = c.fetchone()
	conn.commit()
	conn.close()
	return f"Username: {entries[0]}\nHash: {entries[1]}\nUnique Identifier: {entries[2]}"
	
def delete_user_by_id(id):
	isPriv = admin_authenticate()
	if isPriv == 1:
		conn = sqlite3.connect('auth.db')
		c = conn.cursor()
		c.execute(f"DELETE FROM users WHERE id='{id}'")
		conn.commit()
		conn.close()
	elif isPriv == 0:
		print("Credentials Incorrect or User isn't privileged.")

def delete_user_by_name(username):
	isPriv = admin_authenticate()
	if isPriv == 1:
		conn = sqlite3.connect('auth.db')
		c = conn.cursor()
		c.execute(f"DELETE FROM users WHERE username='{username}'")
		conn.commit()
		conn.close()
	elif isPriv == 0:
		print("Credentials Incorrect or User isn't privileged.")

username = input("Enter Username: ")
password = bytes(input("Enter Password: "), encoding='utf8')


# Formatting of how to use each of the functions.

print(login(username, hashlib.sha256(password)))
print(new_user(username, hashlib.sha256(password)))
print(new_prived_user(username, hashlib.sha256(password)))
print(get_creds(username))
delete_user_by_id(id)
delete_user_by_name(username)
