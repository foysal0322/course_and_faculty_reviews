"""Scrape one NSU course from both Facebook groups using an existing Chrome browser.

Group 1 is scraped first. If it yields fewer than MAX_POSTS posts, group 2 is scraped
as well and the collector keeps going until "End of results". Results are written to
``raw/q_<course>.json`` (same shape the rest of the pipeline already consumes).

Run through ``Scrapper\\run.bat`` or directly::

    python Scrapper\\scrape_course.py bbt203
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT = Path(__file__).resolve().parent.parent
COLLECTOR = ROOT / "raw" / "collector.js"
SINK_SCRIPT = ROOT / "raw" / "sink.py"
PROFILE_DIR = ROOT / "Scrapper" / "chrome-profile"
LOG_FILE = ROOT / "Scrapper" / "scrape.log"
SINK_URL = "http://127.0.0.1:8085"
DEBUG_PORT = 9222
DEBUG_URL = f"http://127.0.0.1:{DEBUG_PORT}"
GROUPS = ("241165482653333", "171372522341869")
MAX_POSTS = 60
POLL_SECONDS = 15
LOGIN_TIMEOUT = 900
ATTEMPTS = 3


def log(message: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {message}"
    print(f"[scraper] {message}", flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    except OSError:
        pass


def port_is_up(url: str, timeout: float = 2.0) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=timeout):
            return True
    except (urllib.error.URLError, TimeoutError, ConnectionError):
        return False


def ensure_sink() -> None:
    """Start ``raw/sink.py`` in the background unless it is already listening."""
    if port_is_up(SINK_URL + "/"):
        log("sink already running on 8085")
        return
    log("starting local sink (raw/sink.py)")
    subprocess.Popen(
        [sys.executable, str(SINK_SCRIPT)],
        cwd=str(ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(40):
        if port_is_up(SINK_URL + "/", timeout=1.0):
            log("sink is up")
            return
        time.sleep(0.25)
    raise RuntimeError("Could not start the local sink on 127.0.0.1:8085.")


def devtools_ready() -> bool:
    """Chrome exposes a DevTools WebSocket only when started with the debug port."""
    try:
        with urllib.request.urlopen(DEBUG_URL + "/json/version", timeout=3) as response:
            return bool(json.loads(response.read().decode("utf-8")).get("webSocketDebuggerUrl"))
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError):
        return False


def find_chrome() -> Path:
    candidates = (
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        Path.home() / "AppData/Local/Google/Chrome/Application/chrome.exe",
    )
    for path in candidates:
        if path.is_file():
            return path
    raise RuntimeError("Google Chrome was not found in the standard install locations.")


def import_existing_session() -> bool:
    """Seed the scraper profile from the user's real Chrome profile.

    Chrome refuses to expose DevTools for the default profile directory, but it
    does for a copy. Copying ``Local State`` plus the cookie database keeps the
    Facebook login without asking the user to sign in again.
    """
    source = Path.home() / "AppData/Local/Google/Chrome/User Data"
    if not source.is_dir():
        return False

    destination_network = PROFILE_DIR / "Default" / "Network"
    if (destination_network / "Cookies").exists():
        return False

    source_network = source / "Default" / "Network"
    try:
        destination_network.mkdir(parents=True, exist_ok=True)
        local_state = source / "Local State"
        if local_state.is_file():
            shutil.copy2(local_state, PROFILE_DIR / "Local State")
        copied = False
        for name in ("Cookies", "Cookies-journal"):
            candidate = source_network / name
            if candidate.is_file():
                shutil.copy2(candidate, destination_network / name)
                copied = True
    except OSError as exc:
        log(f"could not import the existing Chrome session: {exc}")
        return False

    if copied:
        log("imported the existing Chrome session into the scraper profile")
    return copied


def open_chrome() -> None:
    """Open Chrome with its own profile so the DevTools port is actually exposed.

    Chrome 136+ ignores ``--remote-debugging-port`` when the default profile
    directory is used, so this uses a dedicated profile that is kept on disk
    between runs (which also keeps the Facebook login).
    """
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    log(f"opening Chrome (profile: {PROFILE_DIR})")
    subprocess.Popen(
        [
            str(find_chrome()),
            f"--remote-debugging-port={DEBUG_PORT}",
            f"--user-data-dir={PROFILE_DIR}",
            "--no-first-run",
            "--no-default-browser-check",
            "https://www.facebook.com/",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(40):
        if devtools_ready():
            log("Chrome is ready for automation")
            return
        time.sleep(1)
    raise RuntimeError(
        "Chrome did not expose its DevTools port on 9222. Close the scraper "
        f"Chrome window, delete '{PROFILE_DIR}', and try again."
    )


def attach_chrome() -> webdriver.Chrome:
    if not devtools_ready():
        import_existing_session()
        open_chrome()
    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{DEBUG_PORT}")
    try:
        return webdriver.Chrome(options=options)
    except Exception as exc:  # noqa: BLE001 - surfaced as a clear message below
        raise RuntimeError(
            "Chrome is listening on 9222 but Selenium could not attach. "
            "Make sure ChromeDriver matches the installed Chrome version."
        ) from exc


def is_logged_in(driver: webdriver.Chrome) -> bool:
    """Facebook sets a ``c_user`` cookie only for signed-in accounts."""
    try:
        if "/login" in (driver.current_url or ""):
            return False
        return any(cookie.get("name") == "c_user" for cookie in driver.get_cookies())
    except Exception:  # noqa: BLE001 - transient page states are not fatal
        return False


def wait_for_login(driver: webdriver.Chrome, timeout: int = LOGIN_TIMEOUT) -> None:
    """Facebook needs a one-time login in the scraper profile."""
    if is_logged_in(driver):
        log("Facebook session found in the scraper profile")
        return
    log("=" * 64)
    log("  ACTION NEEDED: sign in to Facebook")
    log("  A Chrome window is open on the Facebook login page.")
    log("  Log in there once - scraping starts automatically afterwards,")
    log("  and this profile stays signed in for future runs.")
    log("=" * 64)
    deadline = time.time() + timeout
    waited = 0
    while time.time() < deadline:
        time.sleep(5)
        waited += 5
        if is_logged_in(driver):
            log("signed in - starting the scrape")
            return
        if waited % 60 == 0:
            log(f"still waiting for the Facebook login ({waited}s)")
            if not driver.window_handles:
                raise RuntimeError(
                    "The scraper Chrome window was closed while waiting for login."
                )
    raise RuntimeError(
        "Timed out waiting for the Facebook login. Sign in and run the scraper again."
    )


def find_sink_handle(driver: webdriver.Chrome) -> str | None:
    for handle in driver.window_handles:
        try:
            driver.switch_to.window(handle)
            if driver.execute_script("return window.name || '';") == "fbsink":
                return handle
            if SINK_URL in (driver.current_url or ""):
                return handle
        except Exception:  # noqa: BLE001 - skip tabs that cannot be inspected
            continue
    return None


def open_sink_tab(driver: webdriver.Chrome) -> None:
    """The collector posts data to a tab named ``fbsink``; make sure it exists."""
    current = driver.current_window_handle
    if find_sink_handle(driver):
        driver.switch_to.window(current)
        log("sink tab already open")
        return

    driver.switch_to.window(current)
    driver.execute_script("window.open(arguments[0], 'fbsink'); window.focus();", SINK_URL + "/")
    time.sleep(2)
    if not find_sink_handle(driver):
        log("popup blocked by Chrome; opening the sink tab through DevTools")
        driver.switch_to.window(current)
        driver.switch_to.new_window("tab")
        driver.get(SINK_URL + "/")
        driver.execute_script("window.name = 'fbsink';")
        time.sleep(1)
    driver.switch_to.window(current)
    if find_sink_handle(driver):
        driver.switch_to.window(current)
        log("sink tab is ready")
    else:
        log("WARNING: could not confirm the sink tab; saves may fail")
    driver.switch_to.window(current)


def collector_status(driver: webdriver.Chrome) -> dict | None:
    return driver.execute_script(
        "const s = window.__fb; return s ? {posts: s.posts.length, running: s.running,"
        " done: s.done, saves: s.saves, log: s.log} : null;"
    )


def wait_for_collector(driver: webdriver.Chrome, group_id: str) -> dict:
    last = -1
    while True:
        time.sleep(POLL_SECONDS)
        try:
            status = collector_status(driver)
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(
                f"Lost the Facebook page while scraping group {group_id}."
            ) from exc
        if status is None:
            raise RuntimeError(
                f"The collector stopped responding in group {group_id} "
                "(the page probably reloaded)."
            )
        if status["posts"] != last:
            log(
                f"group {group_id}: {status['posts']} posts, {status['saves']} saves, "
                f"log: {status['log'][-1:]}"
            )
            last = status["posts"]
        if status["done"] or not status["running"]:
            return status


def load_posts(output_path: Path) -> list:
    if not output_path.exists():
        return []
    try:
        data = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Existing file is not valid JSON: {output_path}") from exc
    if not isinstance(data, list):
        raise RuntimeError(f"Existing file is not a post list: {output_path}")
    return data


def scrape_group(driver: webdriver.Chrome, group_id: str, course: str, output_name: str) -> None:
    url = f"https://www.facebook.com/groups/{group_id}/search/?q={quote(course)}"
    collector = COLLECTOR.read_text(encoding="utf-8")

    for attempt in range(1, ATTEMPTS + 1):
        suffix = "" if attempt == 1 else f" (attempt {attempt}/{ATTEMPTS})"
        log(f"group {group_id}: navigating to {url}{suffix}")
        driver.get(url)
        time.sleep(5)

        landed = driver.current_url or ""
        log(f"group {group_id}: landed on {landed}")
        if "/login" in landed:
            raise RuntimeError(
                "Facebook redirected to the login page. Sign in and run the scraper again."
            )
        has_feed = bool(
            driver.execute_script(
                "return !!document.querySelector('[role=feed], [role=main]');"
            )
        )
        log(f"group {group_id}: feed present = {has_feed}")
        open_sink_tab(driver)

        result = driver.execute_script(collector, output_name, MAX_POSTS)
        log(f"group {group_id}: collector said {result!r}")
        if result != "started " + output_name:
            if attempt < ATTEMPTS:
                log(f"group {group_id}: collector did not start; retrying")
                time.sleep(10)
                continue
            raise RuntimeError(
                f"Collector did not start in group {group_id} (returned {result!r})."
            )

        try:
            status = wait_for_collector(driver, group_id)
        except RuntimeError as exc:
            # Facebook often reloads the tab mid-scrape. The collector resumes from
            # the posts already written to disk, so reload and carry on.
            if attempt < ATTEMPTS:
                log(f"group {group_id}: {exc} - reloading and resuming")
                time.sleep(15)
                continue
            raise

        log(f"group {group_id}: finished with {status['posts']} posts")
        return


def normalize_course(raw: str) -> str:
    course = re.sub(r"[\s_-]+", "", raw.strip().lower())
    if not re.fullmatch(r"[a-z]{2,8}\d{2,4}[a-z]?", course):
        raise ValueError(f"{raw!r} is not a valid course code (for example CSE215).")
    return course


def scrape_one(driver: webdriver.Chrome, course: str, outdir: str) -> int:
    """Scrape a single course, falling back to the second group when needed."""
    output_name = f"{outdir}/q_{course}.json"
    output_path = ROOT / output_name
    output_path.parent.mkdir(parents=True, exist_ok=True)

    for index, group_id in enumerate(GROUPS):
        posts = load_posts(output_path)
        if len(posts) >= MAX_POSTS:
            log(f"{course}: already has {len(posts)} posts; skipping group {group_id}")
            break
        scrape_group(driver, group_id, course, output_name)
        posts = load_posts(output_path)
        log(f"{course}: {len(posts)} unique posts saved to {output_path}")
        if len(posts) >= MAX_POSTS:
            break
        if index == len(GROUPS) - 1:
            log(f"{course}: second group finished below 60 posts (end of results)")
    return len(load_posts(output_path))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scrape courses from both Facebook groups using an existing Chrome."
    )
    parser.add_argument(
        "course_code",
        nargs="+",
        help="One or more course codes, for example BBT221 BBT230",
    )
    parser.add_argument(
        "--outdir",
        default="raw",
        help="Folder for the scraped JSON files, relative to the repo (default: raw).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only verify the sink, Chrome and output paths, then exit.",
    )
    args = parser.parse_args()

    try:
        courses = [normalize_course(code) for code in args.course_code]
    except ValueError as exc:
        parser.error(str(exc))
        return 2  # unreachable, parser.error exits

    ensure_sink()
    if args.check:
        if not devtools_ready():
            log("Chrome is not exposing DevTools on 9222 (it will be started on run).")
        else:
            log("Chrome DevTools is available on 9222.")
        log(f"collector found: {COLLECTOR.is_file()}")
        log(f"output folder: {ROOT / args.outdir}")
        log(f"courses: {', '.join(courses)}")
        log("check complete")
        return 0

    driver = attach_chrome()

    try:
        wait_for_login(driver)
        for position, course in enumerate(courses, start=1):
            log(f"===== [{position}/{len(courses)}] {course} =====")
            try:
                count = scrape_one(driver, course, args.outdir)
                log(f"[{position}/{len(courses)}] {course}: done with {count} posts")
            except Exception as exc:  # noqa: BLE001 - one bad course must not stop the batch
                log(f"[{position}/{len(courses)}] {course}: FAILED - {exc}")
    finally:
        # Detach ChromeDriver but leave the user's browser open.
        driver.service.stop()

    log(f"finished {len(courses)} course(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
