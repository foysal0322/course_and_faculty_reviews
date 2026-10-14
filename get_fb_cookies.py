import sqlite3, os, shutil, json, base64, win32crypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

base_dir = r'C:\Users\SMFoysalAhmed\AppData\Local\Google\Chrome\User Data'
local_state_path = os.path.join(base_dir, 'Local State')
with open(local_state_path, 'r', encoding='utf-8') as f:
    local_state = json.load(f)
key = base64.b64decode(local_state['os_crypt']['encrypted_key'])[5:]
decrypted_key = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

best_prof = None
max_cookies = 0

for prof in ['Default', 'Profile 1', 'Profile 4']:
    cookie_db = os.path.join(base_dir, prof, 'Network', 'Cookies')
    if not os.path.exists(cookie_db):
        print(f'{prof}: no Cookies db')
        continue
    temp_db = f'temp_cookie_check.db'
    if os.path.exists(temp_db):
        os.remove(temp_db)
    shutil.copy2(cookie_db, temp_db)
    conn = sqlite3.connect(temp_db)
    c = conn.cursor()
    c.execute("SELECT host_key, name, encrypted_value, path, is_secure, expires_utc FROM cookies WHERE host_key LIKE '%facebook.com%'")
    rows = c.fetchall()
    print(f'{prof}: {len(rows)} facebook cookies found')
    
    cookies = []
    for host_key, name, encrypted_value, path, is_secure, expires_utc in rows:
        try:
            if encrypted_value[:3] in (b'v10', b'v11'):
                nonce = encrypted_value[3:15]
                ciphertext = encrypted_value[15:]
                cipher = AESGCM(decrypted_key)
                val = cipher.decrypt(nonce, ciphertext, None).decode('utf-8')
            else:
                val = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode('utf-8')
            cookies.append({
                'domain': host_key,
                'name': name,
                'value': val,
                'path': path,
                'secure': bool(is_secure)
            })
        except Exception as e:
            pass
    conn.close()
    if os.path.exists(temp_db):
        os.remove(temp_db)
        
    names = [c['name'] for c in cookies]
    print(f'{prof} extracted {len(cookies)} cookies: {names[:10]}')
    if 'c_user' in names:
        print(f'*** LOGGED IN IN {prof}! *** c_user found')
        best_prof = prof
        with open('fb_cookies.json', 'w', encoding='utf-8') as out:
            json.dump(cookies, out, indent=2)
        break

if not best_prof:
    print("Could not find c_user in standard profiles.")
