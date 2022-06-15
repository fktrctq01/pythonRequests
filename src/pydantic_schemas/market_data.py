import re

from pydantic import BaseModel, validator, StrictStr
from typing import List


class MarketDataOrder(BaseModel):
    price: StrictStr
    quantity: StrictStr

    @validator("price", "quantity")
    def check_length_attr(cls, v):
        reg_exs = r"^\d{1,4}$"
        if not re.search(reg_exs, v):
            raise ValueError("not match (integer/string, 10000 > id > 0)")
        return v


class MarketDataSchema(BaseModel):
    asks: List[MarketDataOrder]
    bids: List[MarketDataOrder]
