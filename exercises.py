import sys
import sqlite3
dbconnect = sqlite3.connect("db.sqlite3");
cursor = dbconnect.cursor();

username = sys.argv[1];

print(username)

cursor.execute("SELECT * FROM auth_user WHERE username = '%s'" % (username,))
print(cursor.fetchone())