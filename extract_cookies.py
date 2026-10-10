import sqlite3
import os
import json
import shutil
import base64
import win32crypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def main():
    local_state_path = r'C:\Users\Foysal\AppData\Local\Google\Chrome\User Data\Local State'
    with open(local_state_path, 'r', encoding='utf-8') as f:
        local_state = json.load(f)

    encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])[5:]
    decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

    db_path = r'C:\Users\Foysal\AppData\Local\Google\Chrome\User Data\Profile 2\Network\Cookies'
    temp_db = 'temp_cookies.db'
    shutil.copy2(db_path, temp_db)

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, encrypted_value, path, is_secure, expires_utc FROM cookies WHERE host_key LIKE '%facebook.com%'")

    cookies = []
    for host_key, name, encrypted_value, path, is_secure, expires_utc in cursor.fetchall():
        try:
            if encrypted_value[:3] == b'v10' or encrypted_value[:3] == b'v11':
                nonce = encrypted_value[3:15]
                ciphertext = encrypted_value[15:]
                cipher = AESGCM(decrypted_key)
                decrypted_value = cipher.decrypt(nonce, ciphertext, None).decode('utf-8')
            else:
                decrypted_value = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode('utf-8')
            
            cookies.append({
                'domain': host_key,
                'name': name,
                'value': decrypted_value,
                'path': path,
                'secure': bool(is_secure)
            })
        except Exception as e:
            print(f"Error decrypting {name}: {e}")

    conn.close()
    if os.path.exists(temp_db):
        os.remove(temp_db)

    print(f"Extracted {len(cookies)} Facebook cookies from Profile 2!")
    for c in cookies:
        if c['name'] in ['c_user', 'xs', 'datr', 'sb', 'fr', 'wd']:
            print(f"{c['name']}: {c['value'][:15]}... domain={c['domain']}")

    with open('fb_cookies.json', 'w', encoding='utf-8') as f:
        json.dump(cookies, f, indent=2)

if __name__ == '__main__':
    main()
