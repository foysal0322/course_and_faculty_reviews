import os
import shutil

src_user_data = r'C:\Users\Foysal\AppData\Local\Google\Chrome\User Data'
dst_user_data = r'C:\Users\Foysal\OneDrive\Desktop\course_and_faculty_reviews\selenium_data'

# Copy Local State
local_state_src = os.path.join(src_user_data, 'Local State')
local_state_dst = os.path.join(dst_user_data, 'Local State')
if os.path.exists(local_state_src):
    shutil.copy2(local_state_src, local_state_dst)
    print("Copied Local State")

# Copy Profile 2 into Default inside selenium_data
profile2_src = os.path.join(src_user_data, 'Profile 2')
profile2_dst = os.path.join(dst_user_data, 'Default')

print("Copying Profile 2 to selenium_data/Default...")
# Copy essential subdirectories/files, ignoring locked ones if any
items = ['Network', 'Local Storage', 'Session Storage', 'Cookies', 'Preferences', 'Web Data', 'Login Data']
for item in items:
    s = os.path.join(profile2_src, item)
    d = os.path.join(profile2_dst, item)
    if os.path.exists(s):
        try:
            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d, ignore_errors=True)
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
            print(f"Copied {item}")
        except Exception as e:
            print(f"Error copying {item}: {e}")

print("Profile copy setup complete.")
