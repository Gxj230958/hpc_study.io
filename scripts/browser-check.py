"""Inspect actual browser rendering at desktop and mobile sizes."""
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

base = "http://127.0.0.1:8008/hpc_study.io/"
out = Path("build/browser")
out.mkdir(parents=True, exist_ok=True)
failures = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=p.chromium.executable_path, args=["--no-sandbox"])
    for name, size in [("desktop", {"width":1440,"height":1000}), ("mobile", {"width":390,"height":844})]:
        page = browser.new_page(viewport=size, device_scale_factor=1)
        page.on("pageerror", lambda error: failures.append(str(error)))
        for slug in ("", "hardware/hardware-intro/", "gpu/arch/", "gpu/cuda-advanced/", "benchmark/intro/", "sci-mlsys/intro/", "performance-analysis/intro/"):
            response = page.goto(base + slug, wait_until="load")
            if not response or response.status != 200:
                failures.append(f"{name} {slug}: HTTP failure")
            page.wait_for_timeout(800)
            if page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1"):
                failures.append(f"{name} {slug}: horizontal page overflow")
            broken = page.locator(".md-content img").evaluate_all("xs => xs.filter(x => !x.complete || x.naturalWidth === 0).map(x => x.src)")
            failures.extend(broken)
            if slug in ("hardware/hardware-intro/", "sci-mlsys/intro/"):
                # CDP can inspect Material's closed shadow root without changing it.
                cdp = page.context.new_cdp_session(page)
                pending = [cdp.send("DOM.getDocument", {"depth":-1,"pierce":True})["root"]]
                rendered = False
                while pending:
                    node = pending.pop()
                    pending.extend(node.get("children", []) + node.get("shadowRoots", []))
                    attributes = dict(zip(node.get("attributes", [])[::2], node.get("attributes", [])[1::2]))
                    if node["nodeName"].lower() == "svg" and attributes.get("id", "").startswith("__mermaid_"):
                        box = cdp.send("DOM.getBoxModel", {"backendNodeId":node["backendNodeId"]})["model"]
                        rendered = box["width"] > 30 and box["height"] > 30
                cdp.detach()
                if not rendered:
                    failures.append(f"{name} {slug}: missing rendered diagram")
            if slug == "performance-analysis/intro/" and page.locator("mjx-container").count() == 0:
                failures.append(f"{name}: formula did not render")
            page.screenshot(path=str(out / f"{name}-{slug.replace('/', '-') or 'home'}.png"), full_page=False)
        page.goto(base, wait_until="load")
        page.wait_for_timeout(1000)
        if name == "mobile":
            page.locator('.md-header__button[for="__search"]').click()
        page.locator(".md-search__input").click()
        page.locator(".md-search__input").fill("量化")
        # Material observes keyup; fill() alone only dispatches input events.
        page.locator(".md-search__input").press("End")
        try:
            page.locator(".md-search-result__item").first.wait_for(state="visible", timeout=15000)
        except Exception:
            pass
        count = page.locator(".md-search-result__item").count()
        if count == 0:
            failures.append(f"{name}: Chinese search produced no results: " + page.locator(".md-search-result__meta").inner_text())
        page.keyboard.press("Escape")
        page.locator(".md-header__option label:visible").click()
        page.wait_for_function("document.body.dataset.mdColorScheme === 'slate'")
        page.screenshot(path=str(out / f"{name}-dark.png"))
        page.locator(".md-header__option label:visible").click()
        if name == "mobile":
            page.locator('.md-header__button[for="__drawer"]').click()
            if not page.locator("#__drawer").is_checked():
                failures.append("mobile: navigation drawer did not open")
            page.locator(".md-overlay").click(position={"x":380,"y":400})
        response = page.request.get(base + "downloads/hpc-study-examples.zip")
        if response.status != 200 or response.body()[:2] != b"PK":
            failures.append(f"{name}: example download invalid")
        page.close()
    browser.close()
(out / "summary.json").write_text(json.dumps({
    "timestamp_utc":datetime.now(timezone.utc).isoformat(),
    "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "viewports":[[1440,1000],[390,844]], "pages_per_viewport":7,
    "checks":["HTTP status", "overflow", "images", "diagrams", "formula", "Chinese search", "download", "theme", "mobile navigation"],
    "failures":failures,"passed":not failures}, indent=2))
print(json.dumps({"failures":failures,"passed":not failures}, indent=2))
raise SystemExit(bool(failures))
