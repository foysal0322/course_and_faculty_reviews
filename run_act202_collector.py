import json

with open("raw/collector.js", encoding="utf-8") as f:
    js_content = f.read()

script = f"(function(arguments) {{\n{js_content}\n}})([\"accounting/q_act202.json\", 60]);"

with open("raw/act202_runner.js", "w", encoding="utf-8") as out:
    out.write(script)

print("Saved script to raw/act202_runner.js")
