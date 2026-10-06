import json

with open("raw/collector.js", encoding="utf-8") as f:
    js_content = f.read()

script = f"(function(arguments) {{\n{js_content}\n}})([\"accounting/q_act310.json\", 60]);"

with open("raw/act310_runner.js", "w", encoding="utf-8") as out:
    out.write(script)

print("Saved script to raw/act310_runner.js")
