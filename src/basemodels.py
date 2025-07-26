from pydantic import BaseModel
from typing import Optional
from datetime import date

class Share_Price_Info(BaseModel):
    time            : Optional[date]
    stock_name      : Optional[str]
    close_price     : Optional[float]
    high_price      : Optional[float]
    low_price       : Optional[float]
    open_price      : Optional[float]
    volume          : Optional[int]
    volume_upg      : Optional[int]
    moving_avg_200  : Optional[float]
    moving_avg_100  : Optional[float]
    moving_avg_50   : Optional[float]
    moving_avg_25   : Optional[float]
    moving_avg_9    : Optional[float]