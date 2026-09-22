from abc import ABC, abstractmethod
from typing import Dict, Callable
from pydantic import BaseModel


class RequesterMiddle(ABC):
    def __init__(self, request_speck_middle: Dict[str,str], response_speck_middle: Callable):
        self.headers = request_speck_middle['headers']
        self.base_url = request_speck_middle['base_url']
        self.response_speck_middle = response_speck_middle

    @abstractmethod
    def post(self, model: BaseModel):...



