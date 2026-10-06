import json

with open("raw/collector.js", encoding="utf-8") as f:
    js_content = f.read()

script = f"(function(arguments) {{\n{js_content}\n}})([\"business/q_bus251.json\", 60]);"

with open("raw/bus251_runner.js", "w", encoding="utf-8") as out:
    out.write(script)

print("Saved script to raw/bus251_runner.js")
