# secsoso

SECSOSO（安全搜搜）是一个面向网络安全场景的 AI 搜索引擎，核心思路是：

- 使用 SearXNG 聚合多源检索结果
- 结合安全垂直数据源（漏洞、工具、论文、导航等）
- 使用 LLM + RAG 对检索结果进行总结、归纳与追问建议

项目技术栈：

- 前端：Vue 3 + TailwindCSS
- 后端：FastAPI + SSE
- 搜索中台：SearXNG + App Search + 自定义引擎
- 容器化部署：Docker Compose

## 术语约定

为避免歧义，本文档统一使用以下术语：

- **搜索中台**：`App Search + SearXNG` 的组合服务
- **Engine**：App Search 中的索引单元（如 `sec-vuls`、`sec-tools`）
- **知识库**：写入各 Engine 的 documents 数据
- **初始化知识库快照**：仓库内 `kb/app_search/` 的导出数据

## 设计思路

项目的核心设计可参考：

- https://www.fooying.com/how-to-create-a-security-ai-search-engine/

代码中对应了文章提到的几个关键模块：

1. **检索聚合层**：`backend/src/routers/search.py` 调用 SearXNG
2. **意图路由层**：根据 query 关键词自动选择 `categories/engines`
3. **RAG 提示词层**：`backend/src/utils/prompts.py`
4. **LLM 调用层**：`backend/src/utils/llm.py`（OpenAI 兼容接口）
5. **流式输出层**：SSE 持续输出 `answer` 与 `more_question`

## 项目亮点（安全垂直封装）

- 自建 App Search Engine 知识库检索链路（`sec-vuls`/`sec-links`/`sec-mind`/`sec-wiki`/`sec-social`/`sec-tools`/`secsoso`）
- SearXNG 深度定制（`deploy/searxng/settings.yml`），融合 App Search 与外部安全数据源
- 针对漏洞、工具、论文、标准、导航、社群等场景做了意图路由与引擎优先级控制

完整引擎清单与扩展方法见：`docs/SEARCH_ENGINES.md`

## App Search 初始化知识库

仓库已包含可直接导入的 App Search 初始化快照（Engines/Schema/Relevance/Result/Documents）：

- `kb/app_search/`

导出与导入脚本：

- `scripts/export_app_search_kb.py`
- `scripts/import_app_search_kb.py`

使用方式见：`docs/APP_SEARCH_BOOTSTRAP.md`

新增 Engine 与知识库内容可参考：

- https://swiftype.com/documentation/app-search/getting-started

## 仓库结构

- `frontend/`：前端页面与交互
- `backend/`：API、流式问答、检索编排
- `deploy/`：部署脚本与容器编排
- `imgs/`：项目截图

## 快速开始（本地开发）

### 1) 后端

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .envs/test.env .envs/local.env
echo "APP_ENV=test" > .envs/.env
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2) 前端

```bash
cd frontend
npm install
npm run dev
```

默认前端会请求 `http://127.0.0.1:8000`。

## 后端环境变量

`backend/.envs/prod.env` / `backend/.envs/test.env` 中可配置：

- 基础：`DEBUG` `ALLOWED_HOSTS` `SITE_URL`
- 搜索：`SEAR_XNG_URL` `SEAR_XNG_SAFE` `CONTEXTS_LIMIT`
- 代理鉴权：`PROXY_AUTH`（格式 `user:pass`，可留空）
- LLM：
  - `LLM_PROVIDER`（如 `moonshot` / `openai` / `ollama`）
  - `LLM_MODEL`
  - `LLM_BASE_URL`
  - `LLM_API_KEY`

> 所有密钥默认留空，按你的实际环境填写。

## API 说明

### `GET /search/query`

SSE 流式接口，返回事件：

- `search_results`：完整检索结果
- `contexts`：送入 LLM 的上下文（截断后）
- `answer`：LLM 流式回答片段
- `end_answer`：回答完成标记
- `more_question`：延伸问题流
- `error`：错误事件

### `POST /search/search_query`

普通查询接口（非流式），Body 参考：

```json
{
  "q": "最新高危漏洞",
  "pageno": 1,
  "categories": ["general", "science"],
  "language": "zh-CN",
  "engines": ""
}
```

当 `categories/engines` 为空时，后端会按 query 自动匹配安全搜索意图。

## 部署

请按 `DEPLOY.md` 的顺序执行：先部署搜索中台并导入知识库，再部署 UI + Backend。

## 截图

以下为对比截图（时间：2024-09-12）：

#### 查询最新漏洞
##### SECSOSO
![最新漏洞_secsoso](imgs/最新漏洞_secsoso.jpg)
##### chatgpt
![最新漏洞_chatgpt](imgs/最新漏洞_chatgpt.jpg)
##### metaso
![最新漏洞_metaso](imgs/最新漏洞_metaso.jpg)

#### wordpress漏洞
##### SECSOSO
![wordpress漏洞_secsoso](imgs/wordpress漏洞_secsoso.jpg)
##### chatgpt
![wordpress漏洞_chatgpt](imgs/wordpress漏洞_chatgpt.jpg)
##### metaso
![wordpress漏洞_metaso](imgs/wordpress漏洞_metaso.jpg)

#### 专有知识库查询AI安全应用
##### SECSOSO
![AI安全应用_secsoso](imgs/AI安全应用_secsoso.jpg)
##### chatgpt
![AI安全应用_chatgpt](imgs/AI安全应用_chatgpt.jpg)
##### metaso
![AI安全应用_metaso](imgs/AI安全应用_metaso.jpg)

#### 渗透测试工具
##### SECSOSO
![渗透测试工具_secsoso](imgs/渗透测试工具_secsoso.jpg)
##### chatgpt
![渗透测试工具_chatgpt](imgs/渗透测试工具_chatgpt.jpg)
##### metaso
![渗透测试工具_metaso](imgs/渗透测试工具_metaso.jpg)

#### ctf工具
##### SECSOSO
![ctf工具_secsoso](imgs/ctf工具_secsoso.jpg)
##### chatgpt
![ctf工具_chatgpt](imgs/ctf工具_chatgpt.jpg)
##### metaso
![ctf工具_metaso](imgs/ctf工具_metaso.jpg)
