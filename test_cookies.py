import sqlite3, os, shutil
base_dir = r'C:\Users\SMFoysalAhmed\AppData\Local\Google\Chrome\User Data'
cookie_db = os.path.join(base_dir, 'Default', 'Network', 'Cookies')
temp_db = 'temp_c.db'
if os.path.exists(temp_db):
    os.remove(temp_db)
shutil.copy2(cookie_db, temp_db)
conn = sqlite3.connect(temp_db)
c = conn.cursor()
c.execute("SELECT host_key, name, length(encrypted_value), encrypted_value FROM cookies WHERE host_key LIKE '%facebook%'")
for row in c.fetchall():
    print(row[0], row[1], row[2], repr(row[3][:20]))
conn.close()
if os.path.exists(temp_db):
    os.remove(temp_db)
