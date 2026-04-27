#!/usr/bin/env python3
"""Import App Search knowledge base exported by export_app_search_kb.py.

Usage:
  APP_SEARCH_BASE_URL=http://127.0.0.1:3012 \
  APP_SEARCH_PRIVATE_KEY=private-xxx \
  python3 scripts/import_app_search_kb.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List

BATCH_SIZE = 100


def _normalize_base_url(url: str) -> str:
    return url.rstrip("/")


def _request(
    base_url: str,
    api_key: str,
    method: str,
    path: str,
    body: Any | None = None,
    allow_404: bool = False,
) -> Any:
    url = f"{base_url}/api/as/v1{path}"
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = resp.read().decode("utf-8")
            return json.loads(payload) if payload else None
    except urllib.error.HTTPError as exc:
        if allow_404 and exc.code == 404:
            return None
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"{method} {path} failed: {exc.code} {detail}") from exc


def _chunks(items: List[Dict[str, Any]], size: int) -> Iterable[List[Dict[str, Any]]]:
    for i in range(0, len(items), size):
        yield items[i : i + size]


def _load_ndjson(path: Path) -> List[Dict[str, Any]]:
    docs: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            docs.append(json.loads(line))
    return docs


def _list_document_ids(base_url: str, key: str, engine: str) -> List[str]:
    ids: List[str] = []
    current = 1
    total_pages = 1
    while current <= total_pages:
        q = urllib.parse.urlencode({"page[current]": current, "page[size]": 100})
        resp = _request(base_url, key, "GET", f"/engines/{engine}/documents/list?{q}")
        meta = resp.get("meta", {}).get("page", {})
        total_pages = int(meta.get("total_pages", 1))
        for doc in resp.get("results", []):
            doc_id = doc.get("id")
            if doc_id:
                ids.append(doc_id)
        current += 1
    return ids


def _ensure_engine(base_url: str, key: str, name: str, language: str | None) -> None:
    exists = _request(base_url, key, "GET", f"/engines/{name}", allow_404=True)
    if exists:
        print(f"Engine exists: {name}")
        return

    body: Dict[str, Any] = {"name": name}
    if language:
        body["language"] = language
    _request(base_url, key, "POST", "/engines", body=body)
    print(f"Engine created: {name}")


def import_engine(base_url: str, key: str, engine_dir: Path, reset_documents: bool) -> None:
    engine_meta = json.loads((engine_dir / "engine.json").read_text(encoding="utf-8"))
    schema = json.loads((engine_dir / "schema.json").read_text(encoding="utf-8"))
    search_settings = json.loads((engine_dir / "search_settings.json").read_text(encoding="utf-8"))
    docs = _load_ndjson(engine_dir / "documents.ndjson")

    name = engine_meta["name"]
    language = engine_meta.get("language")

    print(f"Importing engine: {name}")
    _ensure_engine(base_url, key, name, language)

    _request(base_url, key, "POST", f"/engines/{name}/schema", body=schema)
    _request(base_url, key, "PUT", f"/engines/{name}/search_settings", body=search_settings)

    # reset mode: cleanup existing documents to keep deterministic bootstrap state
    if reset_documents:
        existing_ids = _list_document_ids(base_url, key, name)
        for id_batch in _chunks([{"id": i} for i in existing_ids], BATCH_SIZE):
            _request(
                base_url,
                key,
                "DELETE",
                f"/engines/{name}/documents",
                body=[v["id"] for v in id_batch],
            )

    inserted = 0
    for batch in _chunks(docs, BATCH_SIZE):
        _request(base_url, key, "POST", f"/engines/{name}/documents", body=batch)
        inserted += len(batch)
    print(f"  imported documents: {inserted}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import App Search KB snapshot")
    parser.add_argument(
        "--base-url",
        default=os.getenv("APP_SEARCH_BASE_URL", "").strip(),
        help="App Search base URL, e.g. http://127.0.0.1:3012",
    )
    parser.add_argument(
        "--private-key",
        default=os.getenv("APP_SEARCH_PRIVATE_KEY", "").strip(),
        help="App Search private key",
    )
    parser.add_argument(
        "--source-dir",
        default=os.getenv("APP_SEARCH_EXPORT_DIR", "kb/app_search").strip(),
        help="Export snapshot directory",
    )
    parser.add_argument(
        "--engines",
        default="",
        help="Comma-separated engine names to import, default imports all",
    )
    parser.add_argument(
        "--merge",
        action="store_true",
        help="Merge mode: keep existing documents and append imported documents",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_url = args.base_url
    api_key = args.private_key
    src = args.source_dir

    if not base_url or not api_key:
        print("APP_SEARCH_BASE_URL and APP_SEARCH_PRIVATE_KEY are required", file=sys.stderr)
        return 1

    src_dir = Path(src)
    manifest_path = src_dir / "manifest.json"
    if not manifest_path.exists():
        print(f"manifest not found: {manifest_path}", file=sys.stderr)
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    engines = manifest.get("engines", [])
    selected = {e.strip() for e in args.engines.split(",") if e.strip()}

    for engine in engines:
        if selected and engine["name"] not in selected:
            continue
        engine_dir = src_dir / engine["path"]
        import_engine(
            _normalize_base_url(base_url),
            api_key,
            engine_dir,
            reset_documents=not args.merge,
        )

    print("Import completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
