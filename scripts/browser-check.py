"""Browser-level English/archive checks with screenshots at desktop and mobile sizes."""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import zipfile
from playwright.sync_api import sync_playwright

p = argparse.ArgumentParser()
p.add_argument("--base", default="http://127.0.0.1:8008/hpc_study.io/")
p.add_argument("--output", default="build/browser-english")
args = p.parse_args()
base = args.base.rstrip("/") + "/"
out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)
failures = []
checks = []
modules = ["hardware/hardware-intro/", "parallel-programming/parallel-programming-intro/",
           "parallel-programming/mpi/", "gpu/intro/", "performance-analysis/intro/",
           "sci-mlsys/intro/", "clusters/platform-intro/", "datacenter/intro/"]


def diagram_visible(page):
    cdp = page.context.new_cdp_session(page)
    pending = [cdp.send("DOM.getDocument", {"depth": -1, "pierce": True})["root"]]
    rendered = False
    while pending:
        node = pending.pop()
        pending.extend(node.get("children", []) + node.get("shadowRoots", []))
        attrs = dict(zip(node.get("attributes", [])[::2], node.get("attributes", [])[1::2]))
        if node["nodeName"].lower() == "svg" and attrs.get("id", "").startswith("__mermaid_"):
            box = cdp.send("DOM.getBoxModel", {"backendNodeId": node["backendNodeId"]})["model"]
            rendered = rendered or (box["width"] > 30 and box["height"] > 30)
    cdp.detach()
    return rendered


with sync_playwright() as playwright:
    options = {"args": ["--no-sandbox"]}
    if os.environ.get("BROWSER_EXECUTABLE"):
        options["executable_path"] = os.environ["BROWSER_EXECUTABLE"]
    browser = playwright.chromium.launch(**options)
    browser_version = browser.version
    for name, width, height in (("desktop", 1440, 1000), ("mobile", 390, 844)):
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        page.on("pageerror", lambda error: failures.append(str(error)))
        for slug in ["", *modules, "gpu/arch/", "gpu/cuda-advanced/", "learning/labs/",
                     "datacenter/architectures/", "archive/zh/"]:
            response = page.goto(base + slug, wait_until="load")
            if not response or response.status != 200:
                failures.append(f"{name} {slug}: HTTP failure")
            page.wait_for_timeout(600)
            if page.evaluate("document.documentElement.scrollWidth > innerWidth + 1"):
                failures.append(f"{name} {slug}: horizontal page overflow")
            broken = page.locator(".md-content img").evaluate_all(
                "xs => xs.filter(x => !x.complete || x.naturalWidth === 0).map(x => x.src)")
            failures.extend(f"{name}: broken image {src}" for src in broken)
            if slug in modules:
                answers = page.locator('.md-content details:has(> summary:text-is("Answer"))')
                if answers.count() != 3:
                    failures.append(f"{name} {slug}: expected three answers")
                elif answers.evaluate_all("xs => xs.some(x => x.open)"):
                    failures.append(f"{name} {slug}: answer open by default")
                else:
                    first = answers.first
                    first.locator("summary").click()
                    if not first.evaluate("x => x.open"):
                        failures.append(f"{name} {slug}: answer did not open")
                    first.locator("summary").click()
                    if first.evaluate("x => x.open"):
                        failures.append(f"{name} {slug}: answer did not close")
            if slug in ("hardware/hardware-intro/", "sci-mlsys/intro/"):
                if not diagram_visible(page):
                    failures.append(f"{name} {slug}: missing rendered diagram")
            if slug == "performance-analysis/intro/" and not page.locator("mjx-container").count():
                failures.append(f"{name}: formula did not render")
            if slug in ("gpu/intro/", "clusters/platform-intro/"):
                if not page.locator(".md-content pre code").count():
                    failures.append(f"{name} {slug}: no code blocks")
                if not page.locator(".md-content .md-clipboard").count():
                    failures.append(f"{name} {slug}: no code copy controls")
            page.screenshot(path=str(out / f"{name}-{slug.replace('/', '-') or 'home'}.png"))
            checks.append({"viewport": name, "page": slug, "status": response.status if response else None})

        if name == "mobile":
            for root in ("", "archive/zh/"):
                page.goto(base + root, wait_until="load")
                page.add_style_tag(content=":root { --md-text-font: monospace !important; }")
                page.locator(".md-select").hover()
                page.wait_for_timeout(300)
                box = page.locator(".md-select__inner").bounding_box()
                if not box or box["x"] < 0 or box["x"] + box["width"] > width + 1:
                    failures.append(f"{name} {root}: language menu exceeds viewport under wider font metrics")
                if page.evaluate("document.documentElement.scrollWidth > innerWidth + 1"):
                    failures.append(f"{name} {root}: horizontal overflow under wider font metrics")
                page.screenshot(path=str(out / f"mobile-language-{'archive' if root else 'english'}.png"))

        for root, query in (("", "quantization"), ("archive/zh/", "量化")):
            page.goto(base + root, wait_until="load")
            page.wait_for_timeout(1000)
            if name == "mobile":
                page.locator('.md-header__button[for="__search"]').click()
            search = page.locator(".md-search__input")
            search.fill(query)
            search.press("End")
            try:
                page.locator(".md-search-result__item").first.wait_for(state="visible", timeout=15000)
            except Exception:
                failures.append(f"{name} {root}: search returned no result for {query}")
            page.screenshot(path=str(out / f"{name}-search-{'archive' if root else 'english'}.png"))
            page.keyboard.press("Escape")

        page.goto(base, wait_until="load")
        groups = ["Start Here", "CPU and Memory", "GPU Programming", "Performance and Applications",
                  "Clusters", "Datacenter GPUs", "Reference"]
        for group in groups:
            if not page.get_by_text(group, exact=True).count():
                failures.append(f"{name}: navigation group missing: {group}")
        if name == "mobile":
            page.locator('.md-header__button[for="__drawer"]').click()
            if not page.locator("#__drawer").is_checked():
                failures.append("mobile: drawer did not open")
            page.screenshot(path=str(out / "mobile-navigation.png"))
            page.locator(".md-overlay").click(position={"x": 380, "y": 400})
        page.locator(".md-header__option label:visible").click()
        page.wait_for_function("document.body.dataset.mdColorScheme === 'slate'")
        page.screenshot(path=str(out / f"{name}-dark.png"))

        response = page.request.get(base + "downloads/hpc-study-examples.zip")
        try:
            with zipfile.ZipFile(io.BytesIO(response.body())) as archive:
                for source in ("pyproject.toml", "uv.lock", ".python-version", "README-course.md",
                               "scripts/activate-study.sh", "scripts/run-labs.py",
                               "examples/distributed/collectives.py"):
                    if source not in archive.namelist():
                        failures.append(f"{name}: bundle missing {source}")
        except zipfile.BadZipFile:
            failures.append(f"{name}: invalid example download")
        if response.status != 200:
            failures.append(f"{name}: download HTTP {response.status}")
        for old, new in (("platform/cluster/", "clusters/cluster/"),
                         ("hpc-intro/what-is-hpc/", "foundations/what-is-hpc/"),
                         ("gpu/opencl/", "reference/programming-models/opencl/"),
                         ("hardware/gpu/", "gpu/arch/"),
                         ("performance-analysis/nsys/", "gpu/nsys/")):
            page.goto(base + old)
            page.wait_for_url(base + new)
        page.close()
    browser.close()
summary = {"timestamp_utc": datetime.now(timezone.utc).isoformat(),
           "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           "browser_version": browser_version, "base": base, "viewports": [[1440, 1000], [390, 844]],
           "pages": checks, "failures": failures, "passed": not failures}
(out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({"failures": failures, "passed": not failures}, indent=2))
raise SystemExit(bool(failures))
