import json
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

with open('course_faculty.json', 'r', encoding='utf-8') as f:
    course_data = json.load(f)

cse115_faculties = set()
for item in course_data:
    for course, faculties in item.items():
        if course.lower().replace('-', '').replace(' ', '') == 'cse115':
            fac_list = [fac.strip().upper() for fac in faculties.split(',')]
            cse115_faculties.update(fac_list)

chrome_options = Options()
chrome_options.debugger_address = "127.0.0.1:57543"

try:
    driver = webdriver.Chrome(options=chrome_options)
except Exception as e:
    print("Could not connect:", e)
    exit(1)

for handle in driver.window_handles:
    driver.switch_to.window(handle)
    if 'facebook.com' in driver.current_url:
        break

print(f"Attached to page: {driver.current_url}")

# Ensure we are on the search page at the top
if 'search' not in driver.current_url:
    driver.get("https://www.facebook.com/groups/Nsu.faculty.course.grade/search/?q=cse115")
    time.sleep(8)
else:
    # Scroll to top to restart cleanly
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)

seen_posts = set()
all_data = []

def save_data():
    with open('final_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

def extract_modal_text(post_author):
    time.sleep(3.5)
    try:
        dialogs = driver.find_elements(By.CSS_SELECTOR, 'div[role="dialog"]')
        post_dialog = None
        # Find the correct dialog containing the post
        for d in dialogs:
            try:
                t = d.text
                if ("Like" in t and "Comment" in t) or post_author in t:
                    post_dialog = d
                    break
            except:
                pass
                
        if not post_dialog:
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(1)
            return ""
            
        # Try to expand comments by clicking "View more comments"
        for _ in range(5):
            try:
                clickables = post_dialog.find_elements(By.XPATH, ".//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'view more comments') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'replies') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'see more')]")
                clicked = False
                for btn in clickables:
                    if btn.is_displayed():
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                        time.sleep(0.5)
                        driver.execute_script("arguments[0].click();", btn)
                        clicked = True
                        time.sleep(2)
                if not clicked:
                    break
            except:
                pass
                
        text = post_dialog.text
        
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(2)
        return text
    except Exception as e:
        print("Modal error:", e)
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(2)
        return ""

stop_scraping = False
consecutive_no_new = 0

while not stop_scraping:
    try:
        posts = driver.find_elements(By.CSS_SELECTOR, 'div[role="feed"] > div')
        valid_unprocessed = []
        
        for p in posts:
            try:
                text = p.text
                if not text or len(text) < 10: continue
                post_hash = hash(text[:100])
                if post_hash not in seen_posts:
                    valid_unprocessed.append((p, post_hash, text))
            except StaleElementReferenceException:
                continue
                
        # Process 2 posts at a time
        batch = valid_unprocessed[:2]
        if not batch:
            consecutive_no_new += 1
            if consecutive_no_new > 5:
                print("No new posts found after multiple scrolls. Stopping.")
                break
        else:
            consecutive_no_new = 0
            for p, p_hash, p_text in batch:
                try:
                    date_context = p_text[:200]
                    if "2020" in date_context or "2019" in date_context or "6y" in date_context or "7y" in date_context:
                        print("Hit post from 2020 or earlier. Stopping.")
                        stop_scraping = True
                        break
                        
                    seen_posts.add(p_hash)
                    lines = [l.strip() for l in p_text.split('\n') if l.strip()]
                    author = lines[0] if lines else "Unknown"
                    
                    btns = p.find_elements(By.XPATH, ".//div[@role='button']")
                    numeric_btns = [b for b in btns if b.text.strip().isdigit()]
                    
                    num_comments = 0
                    btn_to_click = None
                    if len(numeric_btns) >= 2:
                        num_comments = int(numeric_btns[1].text.strip())
                        btn_to_click = numeric_btns[1]
                    elif len(numeric_btns) == 1:
                        val = int(numeric_btns[0].text.strip())
                        if val > 3:
                            num_comments = val
                            btn_to_click = numeric_btns[0]
                    
                    extracted_text = p_text
                    if num_comments > 0 and btn_to_click:
                        print(f"Opening post by {author} with {num_comments} comments...")
                        try:
                            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn_to_click)
                            time.sleep(1)
                            driver.execute_script("arguments[0].click();", btn_to_click)
                            modal_text = extract_modal_text(author)
                            if modal_text and len(modal_text) > len(extracted_text):
                                extracted_text = modal_text
                        except Exception as e:
                            print(f"Failed to open/extract modal: {e}")
                    
                    # Extract faculties mapped to CSE115, and any other general words that look like faculty initials
                    faculties_mentioned = [f for f in cse115_faculties if re.search(rf'\b{f}\b', extracted_text, re.IGNORECASE)]
                    # Extract unmatched 3-4 letter uppercase words as potential unmapped faculties
                    potential_unmatched = list(set(re.findall(r'\b[A-Z]{3,4}\b', extracted_text)))
                    unmatched_faculties = [f for f in potential_unmatched if f not in faculties_mentioned and f not in ['CSE', 'EEE', 'NSU', 'ENG', 'MAT']]
                    
                    all_data.append({
                        "post_id": f"P_{int(time.time()*1000)}",
                        "author": author,
                        "extracted_text": extracted_text,
                        "matched_cse115_faculties": faculties_mentioned,
                        "unmatched_faculties_found": unmatched_faculties
                    })
                    save_data()
                    print(f"Saved post. Total saved: {len(all_data)}")
                except StaleElementReferenceException:
                    print("Stale element during post processing, skipping.")
                    continue
                
                if stop_scraping:
                    break
                    
        if stop_scraping:
            break
            
        print("Processed batch. Scrolling down and waiting 5 seconds...")
        driver.execute_script("window.scrollBy(0, 1200);")
        time.sleep(5)
        
    except StaleElementReferenceException:
        print("Stale DOM encountered. Retrying feed lookup.")
        time.sleep(2)
        continue

print("Scraping completed.")
