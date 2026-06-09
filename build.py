#!/usr/bin/env python3
"""Transform lp-body.v2.html / mobile-body.v2.html into GitHub Pages preview pc.html / sp.html.

Transforms:
  1. Swap viewport-switcher script (query-param based -> file-based, with ?view= bypass)
  2. Rewrite /wp-content/uploads/lp-assets/ -> lp-assets/
  3. Inject sessionStorage auth guard so direct page access bounces back to index.html
"""
import re
from pathlib import Path

SRC = Path("/Users/mycareer/projects/work-talk-lp-source/wp-deploy")
DST = Path("/tmp/wt-pages")

VP_PC_PREVIEW = '<script data-wt-vp="pc-preview">(function(){if(/[?&]view=/.test(location.search))return;if(!window.matchMedia)return;if(matchMedia("(max-width:767px)").matches){location.replace("./sp.html");}})();</script>'
VP_SP_PREVIEW = '<script data-wt-vp="sp-preview">(function(){if(/[?&]view=/.test(location.search))return;if(!window.matchMedia)return;if(matchMedia("(min-width:768px)").matches){location.replace("./pc.html");}})();</script>'
AUTH_GUARD = '<script>(function(){if(sessionStorage.getItem("wt_lp_auth_v1")!=="1"){location.replace("./");}})();</script>'

VP_SRC_RE = re.compile(r'<script data-wt-vp="(pc|sp)">.*?</script>', re.DOTALL)


def transform(src_path: Path, dst_path: Path, vp_replacement: str) -> None:
    html = src_path.read_text(encoding="utf-8")
    html = VP_SRC_RE.sub(vp_replacement, html, count=1)
    html = html.replace("/wp-content/uploads/lp-assets/", "lp-assets/")
    html = html.replace("<head>", "<head>\n" + AUTH_GUARD, 1)
    dst_path.write_text(html, encoding="utf-8")
    print(f"wrote {dst_path}")


transform(SRC / "lp-body.v2.html", DST / "pc.html", VP_PC_PREVIEW)
transform(SRC / "mobile-body.v2.html", DST / "sp.html", VP_SP_PREVIEW)
