import json
import time
import random
import re
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

sys.stdout.reconfigure(line_buffering=True)

REPLY_TEXT = """Tutor needed !!

We’ve launched nsuOne.com, built dedicatedly for NSUers.
On nsuOne, you can find a tutor and teach at the same time — and yes, you can earn from it too.
Just sign up, add the courses you want to teach, and that’s it. Students can find you when they need help.
Start teaching. Start earning. Follow the page: https://www.facebook.com/nsuOne

www.nsuone.com"""

INCLUDE_PATTERNS = [
    r'\bneed\s+(a\s+)?tutor\b',
    r'\blooking\s+for\s+(a\s+)?(female\s+|male\s+)?tutor\b',
    r'\btutor\s+needed\b',
    r'\btutor\s+wanted\b',
    r'\bneed\s+tutor\b',
    r'\blooking\s+for\s+tutor\b',
    r'\btuition\b'
]

EXCLUDE_PATTERNS = [
    r'\b9th\s*grader\b',
    r'\b9th\s*grade\b',
    r'\balgebra\b',
    r'\bgeometry\b',
    r'\bparents\s+to\s+refer\b',
    r'\bson\b',
    r'\bdaughter\b',
    r'\bclass\s*\d+\b',
    r'\bmohammadpur\b',
    r'\bmirpur\b',
    r'\biso\b',
    r'\bschool\b',
    r'\bhsc\b',
    r'\bssc\b',
    r'\bo\s*level\b',
    r'\ba\s*level\b'
]

COURSE_CODE_PATTERN = r'\b([a-zA-Z]{2,4}\s*[-_]?\s*\d{3})\b'

def is_matching_post(text):
    if not text:
        return False
    text_lower = text.lower()

    for exc in EXCLUDE_PATTERNS:
        if re.search(exc, text_lower):
            return False

    has_tutor_request = any(re.search(inc, text_lower) for inc in INCLUDE_PATTERNS)
    has_course_code = bool(re.search(COURSE_CODE_PATTERN, text_lower)) or "physics" in text_lower or "engineering" in text_lower

    if has_tutor_request and has_course_code:
        return True
    
    if ("tutor" in text_lower or "tuition" in text_lower) and ("faculty" in text_lower or "under" in text_lower or "course" in text_lower or "nsu" in text_lower):
        return True

    return False
