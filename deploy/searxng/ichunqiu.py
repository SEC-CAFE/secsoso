import json
import time
import hashlib
import random
import base64
from urllib.parse import urlencode
from searx.utils import to_string, html_to_text
from searx.engines.json import query as json_query, identity


search_url = None
url_query = None
url_prefix = ""
content_query = None
title_query = None
content_html_to_text = False
title_html_to_text = False
paging = False
thumbnail_query = ''
suggestion_query = ''
results_query = ''
method = 'GET'
word_segment = False
need_base64 = False

data = {}
cookies = {}
headers = {}
'''Some engines might offer different result based on cookies or headers.
Possible use-case: To set safesearch cookie or header to moderate.'''

# parameters for engines with paging support
#
# number of results on each page
# (only needed if the site requires not a page number, but an offset)
page_size = 1
# number of the first page (usually 0 or 1)
first_page_num = 1


def json_request(query, params):  # pylint: disable=redefined-outer-name
    if word_segment:
        query = query.split("<|>", 1)[0]

    if need_base64:
        query = base64.b64encode(query.encode(encoding="utf-8"))

    if query == "null":
        query = ""

    o_query = query
    query = urlencode({'q': query})[2:]

    fp = {'query': query}  # pylint: disable=invalid-name
    if paging:
        fp['pageno'] = (params['pageno'] - 1) * page_size + first_page_num

    new_data = {}
    for _k, _v in data.items():
        if isinstance(_v, str):
            if '{query}' in _v:
                new_data[_k] = _v.replace('{query}', o_query)
            else:
                new_data[_k] = _v.format(**fp)
        else:
            new_data[_k] = _v

    params['cookies'].update(cookies)
    params['headers'].update(headers)
    params['data'].update(new_data)
    params['data'] = json.dumps(params['data'])

    params['url'] = search_url.format(**fp)
    params['query'] = query
    params['method'] = 'POST' if method == 'POST' else 'GET'

    return params, query


def request(query, params):  # pylint: disable=redefined-outer-name
    params, new_query = json_request(query, params)

    random_str = int(time.time()) + random.random()
    _str = f'{random_str}icq'
    rs = hashlib.md5(_str.encode('utf-8')).hexdigest()
    sign_str = f'key_word={new_query}&rs={rs}&type=0&9ebced8552d853232fb766ec3aed153a24578999'
    sign = hashlib.sha1(sign_str.encode("utf-8")).hexdigest()
    params['headers'].update({'SIGN': sign})

    data['key_word'] = new_query
    data['type'] = 0
    data['rs'] = rs
    params['data'] = data
    print(params)

    return params


def response(resp):
    results = []
    json_data = json.loads(resp.text)

    title_filter = html_to_text if title_html_to_text else identity
    content_filter = html_to_text if content_html_to_text else identity

    if results_query:
        rs = json_query(json_data, results_query)  # pylint: disable=invalid-name
        if not rs:
            return results
        for result in rs[0]:
            try:
                url = json_query(result, url_query)[0]
                title = json_query(result, title_query)[0]
            except:  # pylint: disable=bare-except
                continue
            try:
                content = json_query(result, content_query)[0]
            except:  # pylint: disable=bare-except
                content = ""

            try:
                thumbnail = json_query(result, thumbnail_query)[0]
            except:
                thumbnail = ""
            results.append(
                {
                    'url': url_prefix + to_string(url),
                    'title': title_filter(to_string(title)),
                    'content': content_filter(to_string(content)),
                    'thumbnail': to_string(thumbnail),
                }
            )
    else:
        for url, title, content in zip(json_query(json_data, url_query), json_query(json_data, title_query), json_query(json_data, content_query)):
            results.append(
                {
                    'url': url_prefix + to_string(url),
                    'title': title_filter(to_string(title)),
                    'content': content_filter(to_string(content)),
                }
            )

    if not suggestion_query:
        return results
    for suggestion in json_query(json_data, suggestion_query):
        results.append({'suggestion': suggestion})
    return results

