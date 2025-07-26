import json
from typing import Dict
from datetime import datetime
import pandas as pd
with open('config.json','r') as files:
    users = json.load(files)

with open('artifacts\stock_names.json','r') as stock_files:
     stock_info = json.load(stock_files)

def get_home_dropdwon_info()->Dict:

    return {
            'start_date' : '2024-01-01',
            'end_date'   : str(datetime.now()).split(" ")[0],
            'stock_names': stock_info.get("stock_names"),
            'volume_plot_type'   : ['weekly','daily'],
            'current_price' : 'Not Found',
            'sell_to_buy'   : 0,
            'skweness'      : '',
            'utilization'   : '',
            'selected_stock': 'BAJFINANCE.NS',
            'selected_volm' : 'weekly',
            'information'   : None,
            'threshold_limit':[10,15,25,5,1,50,75],
            'type_of_sector_plot' : ['best performer','stock gainer','stock losser'],
            'sell_to_buy_sector_info':['>=1','<=1'],
            'sector_start_date':'2024-01-01',
            'sector_end_date'  :str(datetime.now()).split(" ")[0],
            'Best_Stock_Metadata' : pd.DataFrame(),
            "selected_sector_plot": 'best performer',
            'selected_thresh_limit': '10',
            'selected_sell_to_buy_ratio':'>=1',
            'sector_stats': None
            }