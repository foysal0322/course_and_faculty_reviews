import json
import time

def inject_cookies_to_mcp(mcp_client, session_id):
    with open("fb_cookies.json", encoding="utf-8") as f:
        cookies = json.load(f)
    for c in cookies:
        try:
            mcp_client.add_cookie(
                session_id=session_id,
                name=c["name"],
                value=c["value"],
                domain=c.get("domain", ".facebook.com"),
                path=c.get("path", "/"),
                secure=c.get("secure", True),
                http_only=c.get("httpOnly", True)
            )
        except Exception as e:
            print(f"Cookie {c['name']} load warning:", e)

if __name__ == "__main__":
    print("Loaded fb_cookies.json helper.")
