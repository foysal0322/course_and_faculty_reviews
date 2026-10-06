import sys
import json
import time
import urllib.request

course = sys.argv[1] if len(sys.argv) > 1 else "cse417"
output_file = f"q_{course.lower()}.json"

with open("raw/collector.js", encoding="utf-8") as f:
    js_content = f.read()

script = f'(function(arguments) {{\n{js_content}\n}})(["{output_file}", 60]);'
runner_path = f"raw/{course.lower()}_runner.js"

with open(runner_path, "w", encoding="utf-8") as out:
    out.write(script)

print(f"Saved runner script to {runner_path}")
