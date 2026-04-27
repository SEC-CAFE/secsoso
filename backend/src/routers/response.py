from typing import List, Dict, Union
import orjson
from pydantic import BaseModel, Field


class Response(BaseModel):
    code: int = 0
    data: Union[List, Dict] = Field(default_factory=list)
    message: str = 'success'


class ResponseModel(BaseModel):
    code: int = 0
    data: Dict = Field(default_factory=dict)
    message: str = 'success'


# orjson https://pydantic-docs.helpmanual.io/usage/exporting_models/
# https://yanbin.blog/python-json-choose-ujson-if-necessary/
class CustomModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps


# https://fastapi.tiangolo.com/tutorial/handling-errors/
class CustomException(Exception):
    def __init__(self, code: int, message: str, data: Union[List, Dict] = None):
        if data is None:
            data = []
        self.response = Response(code=code, message=message, data=data)
