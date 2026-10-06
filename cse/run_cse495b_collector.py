import json

with open("raw/collector.js", encoding="utf-8") as f:
    js_content = f.read()

script = f"(function(arguments) {{\n{js_content}\n}})([\"q_cse495b.json\", 60]);"

with open("raw/cse495b_runner.js", "w", encoding="utf-8") as out:
    out.write(script)

print("Saved script to raw/cse495b_runner.js")
