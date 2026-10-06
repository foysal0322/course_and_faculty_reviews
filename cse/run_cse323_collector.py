import json
import urllib.request

with open("raw/collector.js", encoding="utf-8") as f:
    js_content = f.read()

script = f"(function(arguments) {{\n{js_content}\n}})([\"q_cse323.json\", 60]);"

print("Script length:", len(script))

# We will execute this via call_mcp_tool
with open("raw/cse323_runner.js", "w", encoding="utf-8") as out:
    out.write(script)

print("Saved script to raw/cse323_runner.js")
