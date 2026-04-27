# SPDX-License-Identifier: AGPL-3.0-or-later
"""The JSON engine is a *generic* engine with which it is possible to configure
engines in the settings.

.. todo::

   - The JSON engine needs documentation!!

   - The parameters of the JSON engine should be adapted to those of the XPath
     engine.

"""
import json
import base64
from collections.abc import Iterable
from json import loads
from urllib.parse import urlencode
from searx.utils import to_string, html_to_text


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


def iterate(iterable):
    if isinstance(iterable, dict):
        items = iterable.items()

    else:
        items = enumerate(iterable)
    for index, value in items:
        yield str(index), value


def is_iterable(obj):
    if isinstance(obj, str):
        return False
    return isinstance(obj, Iterable)


def parse(query):  # pylint: disable=redefined-outer-name
    q = []  # pylint: disable=invalid-name
    for part in query.split('/'):
        if part == '':
            continue
        q.append(part)
    return q


def do_query(data, q):  # pylint: disable=invalid-name
    ret = []
    if not q:
        return ret

    qkey = q[0]

    for key, value in iterate(data):

        if len(q) == 1:
            if key == qkey:
                ret.append(value)
            elif is_iterable(value):
                ret.extend(do_query(value, q))
        else:
            if not is_iterable(value):
                continue
            if key == qkey:
                ret.extend(do_query(value, q[1:]))
            else:
                ret.extend(do_query(value, q))
    return ret


def query(data, query_string):
    if '|' in query_string:
        contents = []
        for _qs in query_string.split('|'):
            if '=' in _qs:
                _title, _child_query_str = _qs.split('=', 1)
            else:
                _title = ''
                _child_query_str = _qs
            q = parse(_child_query_str)
            _content = do_query(data, q)
            _content = _title + ':' + _content[0]
            contents.append(_content)
        return ['\n'.join(contents)]
    else:
        if '=' in query_string:
            _title, query_string = query_string.split('=', 1)
            q = parse(query_string)
            _content = do_query(data, q)
            _content = _title + ':' + _content[0]
        else:
            q = parse(query_string)
            _content = do_query(data, q)
        return _content


def request(query, params):  # pylint: disable=redefined-outer-name
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
    if params['data']:
        params['data'] = json.dumps(params['data'])
    else:
        params['data'] = {}

    params['url'] = search_url.format(**fp)
    params['query'] = query
    params['method'] = 'POST' if method == 'POST' else 'GET'

    return params


def identity(arg):
    return arg


def response(resp):
    results = []
    json = loads(resp.text)

    title_filter = html_to_text if title_html_to_text else identity
    content_filter = html_to_text if content_html_to_text else identity

    if results_query:
        rs = query(json, results_query)  # pylint: disable=invalid-name
        if not rs:
            return results
        for result in rs[0]:
            try:
                url = query(result, url_query)[0]
                title = query(result, title_query)[0]
            except:  # pylint: disable=bare-except
                continue
            try:
                content = query(result, content_query)[0]
            except:  # pylint: disable=bare-except
                content = ""

            try:
                thumbnail = query(result, thumbnail_query)[0]
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
        for url, title, content in zip(query(json, url_query), query(json, title_query), query(json, content_query)):
            results.append(
                {
                    'url': url_prefix + to_string(url),
                    'title': title_filter(to_string(title)),
                    'content': content_filter(to_string(content)),
                }
            )

    if not suggestion_query:
        return results
    for suggestion in query(json, suggestion_query):
        results.append({'suggestion': suggestion})
    return results

