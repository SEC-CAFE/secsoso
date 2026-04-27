import enum
import json
import asyncio
import re
from typing import List

from pydantic import BaseModel, Field
from fastapi import APIRouter, Body, Request
from sse_starlette import EventSourceResponse

from src.utils.req import HttpReq
from src.utils.llm import LLM
from src.utils.prompts import format_answer_prompt, format_more_question_prompt
from src.routers.response import Response
from src.conf.config import get_app_settings


router = APIRouter()
settings = get_app_settings()
httpreq = HttpReq()
llm_client = LLM()


class searXNGCategory(str, enum.Enum):
    SCIENCE = "science",
    IT = "it",
    GENERAL = "general",
    IMAGES = "images",
    VIDEOS = "videos",
    NEWS = "news",
    MUSIC = "music"
    VUL = "vul"
    POC = "poc"
    PROJECT = "project"
    PAPER = "paper"
    TECHNICAL = "technical"
    STANDARDS = "standards"
    COURSE = "course"
    JOB = "job"
    EVENT = "event"
    NAVIGATION = "navigation"
    SOCIAL = "social"
    MIND = "mind"
    BOOK = "book"


class searchIteam(BaseModel):
    q: str = Field(default="", max_length=256)
    pageno: int = 1
    categories: List[searXNGCategory] = [searXNGCategory.GENERAL, searXNGCategory.SCIENCE]
    language: str = "zh-CN"
    engines: str = ""


def _parse_engine_names(raw: str) -> List[str]:
    if not raw:
        return []
    return [e.strip() for e in raw.split(",") if e and e.strip()]


def _choose_strategy(question: str):
    q = (question or "").lower()

    strategy = {
        "categories": [searXNGCategory.GENERAL, searXNGCategory.SCIENCE],
        "engines": [],
    }

    if re.search(r"cve|漏洞|vuln|exploit|0day|情报", q):
        strategy["categories"] = [searXNGCategory.VUL, searXNGCategory.POC, searXNGCategory.NEWS]
        strategy["engines"] = ["sec vuls", "sec.cafe vuls", "seebug", "snyk", "vulmon", "bing news"]
    elif re.search(r"工具|tool|github|gitlab|项目|project|poc", q):
        strategy["categories"] = [searXNGCategory.PROJECT, searXNGCategory.POC]
        strategy["engines"] = ["sec tools", "freebuf tools", "github", "gitlab"]
    elif re.search(r"论文|paper|研究|research|白皮书", q):
        strategy["categories"] = [searXNGCategory.PAPER, searXNGCategory.TECHNICAL]
        strategy["engines"] = ["sec wiki", "freebuf paper", "vipread", "seebug paper", "hackinn"]
    elif re.search(r"标准|合规|compliance|iso|等保", q):
        strategy["categories"] = [searXNGCategory.STANDARDS, searXNGCategory.TECHNICAL]
        strategy["engines"] = ["cssn standards", "freebuf standards", "bing"]
    elif re.search(r"导航|网站|link|links|资源", q):
        strategy["categories"] = [searXNGCategory.NAVIGATION, searXNGCategory.PROJECT]
        strategy["engines"] = ["sec links", "sec.cafe links", "bing"]
    elif re.search(r"社群|社区|twitter|telegram|公众号|social", q):
        strategy["categories"] = [searXNGCategory.SOCIAL, searXNGCategory.GENERAL]
        strategy["engines"] = ["sec social", "secsoso", "bing"]
    else:
        strategy["engines"] = ["secsoso", "sec mind", "sec tools", "bing"]

    return strategy


def _normalize_item(item: searchIteam) -> searchIteam:
    item.q = (item.q or "").strip()
    if not item.q:
        return item

    strategy = _choose_strategy(item.q)
    default_categories = [searXNGCategory.GENERAL, searXNGCategory.SCIENCE]

    if (not item.categories) or (item.categories == default_categories):
        item.categories = strategy["categories"]

    if not item.engines:
        item.engines = ",".join(strategy["engines"])

    return item


async def get_search_result(item):
    item = _normalize_item(item)
    url = f"{settings.sear_xng_url}/search"
    params = {
        "q": item.q,
        "pageno": item.pageno,
        "categories": ",".join([c.value for c in item.categories]),
        "safesearch": settings.sear_xng_safe,
        "language": item.language,
        "engines": item.engines,
        "format": "json"
    }
    # headers = {
    #     "Cookie": 'disabled_engines=qwant__general; enabled_engines="bing__general\054ddg definitions__general"'
    # }

    content, res = await httpreq.request(
        url,
        method="post",
        params=params,
        # custom_headers=headers,
        auth=settings.proxy_auth,
        retry_limit=0
    )
    data = []
    if content:
        try:
            json_data = json.loads(content)
        except json.JSONDecodeError:
            return data
        results = json_data.get("results", [])
        n = 0
        for _ in results:
            n += 1
            parsed_url = _.get("parsed_url", [])
            data.append({
                "id": n,
                "title": _.get("title"),
                "url": _.get("url"),
                "content": _.get("content"),
                "engines": _.get("engines", []),
                "site": parsed_url[1] if parsed_url else '',
            })
    return data


@router.get("/query", response_model=Response, include_in_schema=False)
async def query(req: Request, q: str = "", pageno: int = 1, ):
    async def event_generator(request: Request):
        item = searchIteam(q=q, pageno=pageno)
        item = _normalize_item(item)
        if not item.q:
            yield {
                "event": "error",
                "retry": 15000,
                "data": "empty query",
            }
            return

        data = await get_search_result(item)
        contexts = data[:settings.contexts_limit]

        yield {
            "event": "search_results",
            "retry": 15000,
            "data": json.dumps(data)
        }
        yield {
            "event": "contexts",
            "retry": 15000,
            "data": json.dumps(contexts)
        }
        await asyncio.sleep(0.1)

        try:
            answer_response = llm_client.chat_stream(format_answer_prompt(contexts), item.q)
            for chunk in answer_response:
                if await request.is_disconnected():
                    break
                choices = chunk.choices  # type: ignore
                if choices:
                    message = choices[0].delta.content
                    if not message:
                        continue
                    yield {
                        "event": "answer",
                        "retry": 15000,
                        "data": message
                    }
                    await asyncio.sleep(0.05)
        except Exception as ex:  # pragma: no cover - runtime protection
            yield {
                "event": "error",
                "retry": 15000,
                "data": f"llm_error: {str(ex)}",
            }
            return
        yield {
            "event": "end_answer",
            "retry": 15000,
            "data": 1
        }

        try:
            more_question_response = llm_client.chat_stream(format_more_question_prompt(contexts), item.q)
            for chunk in more_question_response:
                if await request.is_disconnected():
                    break
                choices = chunk.choices  # type: ignore
                if choices:
                    message = choices[0].delta.content
                    if not message:
                        continue
                    yield {
                        "event": "more_question",
                        "retry": 15000,
                        "data": message
                    }
                    await asyncio.sleep(0.05)
        except Exception:
            # related-question stage should not break main answer flow
            return

    return EventSourceResponse(event_generator(req))


@router.post("/search_query", response_model=Response, include_in_schema=False)
async def search_query(item: searchIteam = Body(...)):
    resp = Response()
    item = _normalize_item(item)
    if not item.q:
        resp.code = 400
        resp.message = "empty query"
        resp.data = []
        return resp

    data = await get_search_result(item)

    resp.data = data
    return resp
