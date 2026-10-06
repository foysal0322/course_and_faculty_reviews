import json

with open("raw/collector.js", encoding="utf-8") as f:
    js_content = f.read()

script = f"(function(arguments) {{\n{js_content}\n}})([\"q_cse425.json\", 60]);"

with open("raw/cse425_runner.js", "w", encoding="utf-8") as out:
    out.write(script)

print("Saved script to raw/cse425_runner.js")
