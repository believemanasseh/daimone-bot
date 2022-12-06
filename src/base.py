from typing import Union
from pydantic import BaseModel


class Request(BaseModel):
    update_id: str
    message: Union[dict, None] = None
