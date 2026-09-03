#!/usr/bin/env python3
"""Generate the offline/installable build in app/ from index.html.

index.html is the Artifact source: it deliberately has no <!doctype>/<head>/<body>,
because the Artifact host supplies those. The phone app needs a complete document,
so this wraps the same content and adds the PWA plumbing. Run after editing
index.html so the two never drift apart.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).parent
src = (ROOT / "index.html").read_text()

title = re.search(r"<title>(.*?)</title>", src).group(1)

HEAD = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<link rel="manifest" href="./manifest.webmanifest">
<link rel="apple-touch-icon" href="./icon-180.png">
<link rel="icon" type="image/png" href="./icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Dope Card">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#EAEBE5">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#1A201D">
<meta name="description" content="Holdover and point-of-impact chart for 7mm Rem Mag and .30-06 Springfield.">
<style>
  html{{color-scheme:light dark}}
  body{{margin:0}}
  img{{max-width:100%}}
  [hidden]{{display:none!important}}
  /* keep content clear of the notch when installed full screen */
  .topbar{{padding-top:calc(13px + env(safe-area-inset-top))}}
  .wrap{{padding-bottom:calc(52px + env(safe-area-inset-bottom))}}
</style>
</head>
<body>
"""

FOOT = """
<script>
/* Register the offline worker. isSecureContext covers https and localhost;
   on file:// or where the host forbids it this silently does nothing, and the
   page is fully self-contained either way. */
if ("serviceWorker" in navigator && window.isSecureContext) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("./sw.js").catch(function () {});
  });
}
</script>
</body>
</html>
"""

(ROOT / "app").mkdir(exist_ok=True)
(ROOT / "app" / "index.html").write_text(HEAD + src + FOOT)
print("app/index.html written:", (ROOT / "app" / "index.html").stat().st_size // 1024, "KB")
