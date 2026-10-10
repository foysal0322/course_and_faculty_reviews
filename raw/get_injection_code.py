import sys
import json

def get_code(course, folder="History", max_posts=60):
    with open("raw/collector.js", "r", encoding="utf-8") as f:
        collector_code = f.read()
    
    target_name = f"{folder}/q_{course.lower()}.json"
    header = f"window.__fbTargetName = {json.dumps(target_name)};\nwindow.__fbTargetMax = {max_posts};\n"
    return header + collector_code

if __name__ == "__main__":
    course = sys.argv[1] if len(sys.argv) > 1 else "his101"
    code = get_code(course)
    with open("raw/current_injection.js", "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Generated raw/current_injection.js for {course} (length: {len(code)})")
