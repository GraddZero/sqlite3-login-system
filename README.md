# sqlite3-login-system
Login system made with SQLite3. Features SHA256 hashing for passwords and some base functions. Made to be used in a website in the backend, but more uses can probably be found.

First time init
Username is the username field
Password is a hashed sha256 password in this instance though variations can be made
privileged in an integer that should either be a 1 or a 0. Alterations can be made to have different levels of privilege across system.
id is a unique number associated with each entry.
in the cursor.execute(username, password, privileged, null) entry, change password to a hashed sha256 pass. Keep rest the same.

Run it once then afterwards just remove the code or comment it out otherwise you'll get errors.
