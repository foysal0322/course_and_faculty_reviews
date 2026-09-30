import json, time, urllib.request

ports = [49673, 49670, 49668, 49667, 49666, 49665, 49664, 49312, 42050, 62764, 58872, 58871, 58870, 58869, 58281, 58270, 58269, 58265, 49683, 49682, 49680, 49676, 49320]

found = []
for p in range(49000, 50000):
    try:
        url = f"http://127.0.0.1:{p}/json/version"
        res = urllib.request.urlopen(url, timeout=0.1).read().decode()
        print(f"Found Chrome DevTools on port {p}:", res[:80])
        found.append(p)
    except Exception:
        pass
