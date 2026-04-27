# 搜索引擎与知识库说明

SECSOSO 的核心价值在于“安全垂直知识库 + 自定义检索引擎”。

## 1. 整体链路

1. App Search 承载预填充知识库（多个 Engine）
2. SearXNG 统一编排检索（App Search Engine + 外部平台 Engine）
3. FastAPI 从 SearXNG 拉取结果并做 RAG
4. 前端通过 SSE 获取流式回答

## 2. App Search 预置 Engine（标准）

项目默认使用以下 Engine，并写入 documents：

- `sec-vuls`：漏洞与情报
- `sec-links`：安全导航与站点
- `sec-mind`：方法论/心智内容
- `sec-wiki`：术语与知识条目
- `sec-social`：社区与社媒来源
- `sec-tools`：工具与项目
- `secsoso`：综合知识库（通用补充）

示例查询接口（需 search key）：

`POST /api/as/v1/engines/<engine_name>/search.json`

例如：

`http://<appsearch-host>:3002/api/as/v1/engines/sec-mind/search.json`

若希望直接复用现成初始化内容，可使用仓库内快照导入流程：

- `docs/APP_SEARCH_BOOTSTRAP.md`

## 3. SearXNG 已封装的核心安全引擎

配置文件：`deploy/searxng/settings.yml`

### 3.1 App Search 引擎映射

- `sec mind` -> `sec-mind`
- `sec tools` -> `sec-tools`
- `sec social` -> `sec-social`
- `sec links` -> `sec-links`
- `sec vuls` -> `sec-vuls`
- `sec wiki` -> `sec-wiki`
- `secsoso` -> `secsoso`

这些引擎统一使用 App Search Search Key（`Authorization: Bearer ...`）。

`deploy/searxng/settings.yml` 中默认占位符为：

- `Authorization: Bearer CHANGE_ME_APPSEARCH_SEARCH_KEY`

请在 App Search 后台创建 Search Key 后替换为真实值（`search-...`）。

### 3.2 外部平台引擎（示例）

- `cssn standards`
- `sec.cafe vuls`
- `sec.cafe links`
- `sploitus exps`
- `expku`
- `vulmon`
- `seebug`
- `snyk`
- `freebuf *`（tools/vul/course/event/technical/standards/job/paper）
- `vipread` / `seebug paper` / `hackinn`

## 4. 如何新增 App Search 知识库

建议先阅读官方入门文档：

- https://swiftype.com/documentation/app-search/getting-started

1. 在 App Search 新建 Engine（如 `sec-new`）
2. 准备 documents（建议字段）：
   - `title`（text）
   - `content`（text）
   - `url`（text）
   - `file`（text，可选缩略图）
3. 通过 Documents API 导入
4. 在 `deploy/searxng/settings.yml` 新增对应 engine

新增 engine 模板：

```yaml
- name : sec new
  engine : json
  engine_type: online
  search_url : http://appsearch:3002/api/as/v1/engines/sec-new/search.json
  enable_http: true
  method: POST
  data:
    query: "{query}"
  headers:
    Authorization: Bearer CHANGE_ME_APPSEARCH_SEARCH_KEY
    Content-Type: application/json
  results_query: results
  title_query: title/raw
  content_query: content/raw
  url_query: url/raw
  categories: [technical]
  word_segment: true
  timeout: 6.0
  shortcut: scnw
  weight: 120
  disabled: false
```

## 5. 如何新增外部平台引擎

按目标网站返回类型选 `json` / `xpath`：

1. 确认 query 参数、分页参数、鉴权、反爬策略
2. 在 `settings.yml` 新增 engine 并设置：
   - `search_url`
   - `results_query` 或 `results_xpath`
   - `title/content/url` 映射
   - `categories`、`weight`、`timeout`
3. 在 SearXNG 容器内验证
4. 再在后端意图路由（`backend/src/routers/search.py`）中纳入优先引擎

## 6. 配置建议

- 将 App Search Search Key 以环境变量或部署平台 Secret 管理
- 定期检查外部引擎字段是否变更，避免 XPath/JSON 路径失效
