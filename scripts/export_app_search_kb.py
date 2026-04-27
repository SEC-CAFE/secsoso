#!/usr/bin/env python3
"""Export App Search engines, schema, search settings and documents.

Usage:
  APP_SEARCH_BASE_URL=http://127.0.0.1:3012 \
  APP_SEARCH_PRIVATE_KEY=private-xxx \
  python3 scripts/export_app_search_kb.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

PAGE_SIZE = 100


def _normalize_base_url(url: str) -> str:
    return url.rstrip("/")


def _request_json(base_url: str, api_key: str, path: str) -> Any:
    url = f"{base_url}/api/as/v1{path}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def export(base_url: str, api_key: str, out_dir: Path) -> None:
    engines_resp = _request_json(base_url, api_key, "/engines")
    engines = engines_resp.get("results", [])

    (out_dir / "engines").mkdir(parents=True, exist_ok=True)

    manifest: Dict[str, Any] = {
        "source": base_url,
        "engine_count": len(engines),
        "engines": [],
    }

    for engine in engines:
        name = engine["name"]
        print(f"Exporting engine: {name}")

        engine_dir = out_dir / "engines" / name
        engine_dir.mkdir(parents=True, exist_ok=True)

        schema = _request_json(base_url, api_key, f"/engines/{name}/schema")
        search_settings = _request_json(base_url, api_key, f"/engines/{name}/search_settings")

        (engine_dir / "engine.json").write_text(
            json.dumps(engine, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (engine_dir / "schema.json").write_text(
            json.dumps(schema, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (engine_dir / "search_settings.json").write_text(
            json.dumps(search_settings, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        # App Search exposes relevance tuning and result settings via search_settings.
        relevance_tuning = {
            "search_fields": search_settings.get("search_fields", {}),
            "boosts": search_settings.get("boosts", {}),
        }
        result_settings = {"result_fields": search_settings.get("result_fields", {})}
        (engine_dir / "relevance_tuning.json").write_text(
            json.dumps(relevance_tuning, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (engine_dir / "result_settings.json").write_text(
            json.dumps(result_settings, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        documents_path = engine_dir / "documents.ndjson"
        total_docs = 0
        current = 1
        total_pages = 1

        with documents_path.open("w", encoding="utf-8") as f:
            while current <= total_pages:
                query = urllib.parse.urlencode(
                    {
                        "page[current]": current,
                        "page[size]": PAGE_SIZE,
                    }
                )
                page_data = _request_json(
                    base_url,
                    api_key,
                    f"/engines/{name}/documents/list?{query}",
                )
                meta = page_data.get("meta", {}).get("page", {})
                total_pages = int(meta.get("total_pages", 1))
                results: List[Dict[str, Any]] = page_data.get("results", [])

                for doc in results:
                    f.write(json.dumps(doc, ensure_ascii=False) + "\n")
                total_docs += len(results)
                print(f"  page {current}/{total_pages} -> {len(results)} docs")
                current += 1

        info = {
            "name": name,
            "language": engine.get("language"),
            "type": engine.get("type", "default"),
            "documents": total_docs,
            "path": str(Path("engines") / name),
        }
        (engine_dir / "meta.json").write_text(
            json.dumps(info, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        manifest["engines"].append(info)

    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    base_url = os.getenv("APP_SEARCH_BASE_URL", "").strip()
    api_key = os.getenv("APP_SEARCH_PRIVATE_KEY", "").strip()
    out = os.getenv("APP_SEARCH_EXPORT_DIR", "kb/app_search").strip()

    if not base_url or not api_key:
        print("APP_SEARCH_BASE_URL and APP_SEARCH_PRIVATE_KEY are required", file=sys.stderr)
        return 1

    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    export(_normalize_base_url(base_url), api_key, out_dir)
    print(f"Export completed: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
