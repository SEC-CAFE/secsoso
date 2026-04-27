# SECSOSO 部署说明

本文档提供一条可直接落地的部署路径：

1. 部署搜索中台（App Search + SearXNG）
2. 导入初始化知识库
3. 部署应用层（UI + Backend）
4. 验证服务

执行前可先做快速核对：

- `deploy/.env` 已设置 `APP_SEARCH_DEFAULT_PASSWORD`
- `deploy/appsearch/app-search.yml` 已设置 `elasticsearch.password`
- `backend/.envs/prod.env` 已设置 `LLM_BASE_URL` / `LLM_API_KEY` / `LLM_MODEL`

## 1) 环境准备

- 已安装 Docker / Docker Compose
- 已安装 Python 3（用于导入知识库）
- 已安装 Node.js 20.x（用于构建前端）

在仓库根目录准备配置：

- 后端配置：`backend/.envs/prod.env`
- 中台配置：
  - 复制 `deploy/.env.example` 为 `deploy/.env`
  - 修改 `deploy/.env` 中 `APP_SEARCH_DEFAULT_PASSWORD`
  - 修改 `deploy/appsearch/app-search.yml` 中 `elasticsearch.password`
  - 修改 `deploy/searxng/settings.yml` 中 App Search Search Key（`Authorization: Bearer ...`）

App Search 后台默认登录：

- 用户名：`app-search`
- 密码：`deploy/.env` 中 `APP_SEARCH_DEFAULT_PASSWORD`

## 2) 部署搜索中台（必须）

```bash
cd deploy
docker-compose -f docker-compose.engine.yml up -d
```

等待容器就绪后，确认 App Search 可访问：

- `http://127.0.0.1:3012`

此时登录 App Search 后台并创建 Search Key（用于查询 Engine）：

1. 打开 `http://127.0.0.1:3012`
2. 使用账号 `app-search` 和 `APP_SEARCH_DEFAULT_PASSWORD` 登录
3. 在 App Search 后台创建 Search Key（形如 `search-xxxxxxxx`）

然后把 `deploy/searxng/settings.yml` 中所有占位符：

- `Authorization: Bearer CHANGE_ME_APPSEARCH_SEARCH_KEY`

替换为你的真实 Search Key，例如：

- `Authorization: Bearer search-xxxxxxxxxxxxxxxx`

## 3) 导入初始化知识库（必须）

回到仓库根目录执行：

```bash
APP_SEARCH_BASE_URL=http://127.0.0.1:3012 \
APP_SEARCH_PRIVATE_KEY=private-xxxx \
python3 scripts/import_app_search_kb.py
```

更多导入参数见：`docs/APP_SEARCH_BOOTSTRAP.md`

## 4) 构建并部署 UI + Backend（必须）

先构建前端：

```bash
cd frontend
npm install
npm run build
```

执行部署脚本：

```bash
cd ../deploy
chmod +x deploy.sh
./deploy.sh -s ui -e prod -t /data/www/secsoso.com --clean
```

参数说明：

- `-s ui`：部署 UI + Backend
- `-e prod|test`：选择后端环境
- `-t`：目标部署目录
- `--clean`：清空目标目录后部署

## 5) 验证

- 打开前端页面并发起搜索
- 检查 `search_results` 和 `answer` 是否正常返回
- 检查后端日志是否存在 `llm_error`

## 6) Nginx（按需）

如需对外代理：

- 站点配置：`deploy/nginx/ui_nginx.conf`
- 搜索代理：`deploy/nginx/proxy_nginx.conf`

如启用 basic auth，请先生成 htpasswd：

```bash
htpasswd -nb <user> <password>
```

将结果写入 `.proxy_htpasswd` 并挂载到 nginx。

## 7) 扩展知识库与引擎

- 引擎清单与扩展方法：`docs/SEARCH_ENGINES.md`
- App Search 初始化/导入导出：`docs/APP_SEARCH_BOOTSTRAP.md`
- App Search 官方入门：
  - https://swiftype.com/documentation/app-search/getting-started
