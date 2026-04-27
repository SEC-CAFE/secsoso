# App Search 初始化知识库

本目录用于保存项目部署时可直接导入的 App Search 初始化知识库快照：

- Engine 元数据
- Schema
- Relevance Tuning（由 `search_settings` 拆分）
- Result Settings（由 `search_settings` 拆分）
- Documents

数据目录：`kb/app_search/`

## 1. 当前快照内容

已导出 Engines：

- `sec-vuls`
- `sec-links`
- `sec-mind`
- `sec-wiki`
- `sec-social`
- `sec-tools`
- `secsoso`

详情见：`kb/app_search/manifest.json`

## 2. 导出（维护者）

```bash
cd secsoso
APP_SEARCH_BASE_URL=http://<host>:3012 \
APP_SEARCH_PRIVATE_KEY=private-xxxx \
python3 scripts/export_app_search_kb.py
```

导出脚本会写入：

- `kb/app_search/manifest.json`
- `kb/app_search/engines/<engine>/engine.json`
- `kb/app_search/engines/<engine>/schema.json`
- `kb/app_search/engines/<engine>/search_settings.json`
- `kb/app_search/engines/<engine>/relevance_tuning.json`
- `kb/app_search/engines/<engine>/result_settings.json`
- `kb/app_search/engines/<engine>/documents.ndjson`

## 3. 导入（部署初始化）

```bash
cd secsoso
APP_SEARCH_BASE_URL=http://<host>:3012 \
APP_SEARCH_PRIVATE_KEY=private-xxxx \
python3 scripts/import_app_search_kb.py
```

可选参数：

- `--merge`：保留现有 documents，只追加导入
- `--engines sec-vuls,sec-wiki`：仅导入指定 engines
- `--source-dir kb/app_search`：指定导入目录

导入行为：

1. 若 Engine 不存在则自动创建
2. 写入 Schema
3. 写入 Search Settings（包含 Relevance/Result 配置）
4. 默认清空现有 documents（`--merge` 时跳过）
5. 批量导入 `documents.ndjson`

## 4. 安全建议

- `APP_SEARCH_PRIVATE_KEY` 不要写入代码仓库
- 建议在 CI/CD Secret 或本地环境变量中注入
- 若知识库存在受限内容，发布开源前请检查 `documents.ndjson`

## 5. 扩展知识库

若你需要新增 Engine、Schema 或文档，可先参考：

- https://swiftype.com/documentation/app-search/getting-started
