import sys
import time
import json
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    opts = Options()
    opts.add_argument('--user-data-dir=C:\\Users\\Foysal\\OneDrive\\Desktop\\course_and_faculty_reviews\\selenium_data')
    opts.add_argument('--disable-notifications')
    opts.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=opts)
    driver.get('https://www.facebook.com')
    time.sleep(2)

    with open('fb_cookies.json', 'r', encoding='utf-8') as f:
        cookies = json.load(f)

    for c in cookies:
        val = urllib.parse.unquote(c['value'])
        cookie_dict = {
            'name': c['name'],
            'value': val,
            'domain': '.facebook.com',
            'path': '/'
        }
        try:
            driver.add_cookie(cookie_dict)
            print(f"Added cookie: {c['name']}")
        except Exception as e:
            print(f"Error adding {c['name']}: {e}")

    driver.get('https://www.facebook.com/groups/241165482653333/search/?q=mkt202')
    time.sleep(5)

    print('Current URL:', driver.current_url)
    print('Title:', driver.title)
    snippet = driver.find_element('tag name', 'body').text[:400].encode('ascii', 'ignore').decode('ascii')
    print('Snippet:', snippet)

    info = driver.execute_script('''
        const main = document.querySelector('[role=main]');
        const feed = document.querySelector('[role=feed]');
        const articles = document.querySelectorAll('[role=article]');
        const dirAuto = document.querySelectorAll('div[dir=auto]');
        const msgElements = document.querySelectorAll('[data-ad-rendering-role=story_message],[data-ad-comet-preview=message]');
        
        return {
            hasMain: !!main,
            mainChildrenCount: main ? main.children.length : 0,
            hasFeed: !!feed,
            feedChildrenCount: feed ? feed.children.length : 0,
            articlesCount: articles.length,
            msgElementsCount: msgElements.length,
            dirAutoCount: dirAuto.length
        };
    ''')
    print(json.dumps(info, indent=2))
    driver.quit()

if __name__ == '__main__':
    main()
