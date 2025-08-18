import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

import plotly.express as px
import plotly.io as pio
from plotly import graph_objects as go

from typing import List, Dict
from sqlalchemy import text
from src.basemodels import Share_Price_Info

def trend_plot(information):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=information.get('stock_info')["Date"].values,
            y=information.get('stock_info')["Close"].values,
            name="Close",
            text=information.get('stock_info')[["Date", "Close", "Stock_Name",  "Volume_Upg"]].apply(
                lambda row: f"Date: {row['Date']}<br>Close: {round(row['Close'], 2)}<br>Stock Name: {row['Stock_Name']}<br>Volume: {round(row['Volume_Upg'], 2)}",
                axis=1,
            ),
            hoverinfo="text",
            line=dict(color='#636EFA', width=2),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=information.get('stock_info')["Date"].values,
            y=information.get('stock_info')["MAE_25"].values+information.get('limit_threshold'),
            name="Upper Limit",
            text=information.get('stock_info')[["Date", "MAE_25", "Stock_Name"]].apply(
                lambda row: f"Date: {row['Date']}<br>Upper Limit: {round(row['MAE_25']+information.get('limit_threshold'),2)}<br>Stock Name: {row['Stock_Name']}",
                axis=1,
            ),
            hoverinfo="text",
            line=dict(color="black", width=1.5,dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=information.get('stock_info')["Date"].values,
            y=information.get('stock_info')["MAE_25"].values-information.get('limit_threshold'),
            name="Lower Limit",
            text=information.get('stock_info')[["Date", "MAE_25", "Stock_Name"]].apply(
                lambda row: f"Date: {row['Date']}<br>Lower Limit: {round(row['MAE_25']-information.get('limit_threshold'),2)}<br>Stock Name: {row['Stock_Name']}",
                axis=1,
            ),
            hoverinfo="text",
            line=dict(color="black", width=1.5,dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=information.get('buy_signal_info')["Date"],
            y=information.get('buy_signal_info')["Close"],
            name="Buy Signal",
            mode='markers',  # Show both markers and lines
            text=information.get('buy_signal_info')[["Date", "Close", "Stock_Name"]].apply(
                lambda row: f"Date: {row['Date']}<br>Close: {round(row['Close'],2)}<br>Stock Name: {row['Stock_Name']}",
                axis=1,
            ),
            marker=dict(symbol='circle', size=9, color='green',opacity=0.6),  # Marker style
        )
    )

    fig.add_trace(
        go.Scatter(
            x=information.get('sell_signal_info')["Date"],
            y=information.get('sell_signal_info')["Close"],
            name="Sell Signal",
            mode='markers',  # Show both markers and lines
            text=information.get('sell_signal_info')[["Date", "Close", "Stock_Name"]].apply(
                lambda row: f"Date: {row['Date']}<br>Close: {round(row['Close'],2)}<br>Stock Name: {row['Stock_Name']}",
                axis=1,
            ),
            marker=dict(symbol='circle', size=9, color='red',opacity=0.6),  # Marker style
        )
    )

    fig.add_trace(
        go.Scatter(
            x=information.get('trend_change_info')["Date"],
            y=information.get('trend_change_info')["Close"],
            name="Trend Change Signal",
            mode='markers',  # Show both markers and lines
            text=information.get('trend_change_info')[["Date", "Close", "Stock_Name"]].apply(
                lambda row: f"Date: {row['Date']}<br>Close: {round(row['Close'],2)}<br>Stock Name: {row['Stock_Name']}",
                axis=1,
            ),
            marker=dict(symbol='circle', size=9, color='orange',opacity=0.6),  # Marker style
        )
    )

    fig.add_trace(

        go.Scatter(
            x=information.get('stock_info')["Date"].values,
            y=information.get('stock_info')["MAE_25"].values,
            name="MAE_25",
            text=information.get('stock_info')[["Date", "MAE_25", "Stock_Name",  "Volume_Upg"]].apply(
                lambda row: f"Date: {row['Date']}<br>MAE_25: {round(row['MAE_25'], 2)}<br>Stock Name: {row['Stock_Name']}<br>Volume: {round(row['Volume_Upg'], 2)}",
                axis=1,
            ),
            hoverinfo="text",
            line=dict(color="gray", width=1.5,dash="dash"),
        )
    )

    fig.add_trace(

        go.Scatter(
            x=information.get('stock_info')["Date"].values,
            y=information.get('stock_info')["MAE_50"].values,
            name="MAE_50",
            text=information.get('stock_info')[["Date", "MAE_50", "Stock_Name",  "Volume_Upg"]].apply(
                lambda row: f"Date: {row['Date']}<br>MAE_50: {round(row['MAE_50'], 2)}<br>Stock Name: {row['Stock_Name']}<br>Volume: {round(row['Volume_Upg'], 2)}",
                axis=1,
            ),
            hoverinfo="text",
            line=dict(color="firebrick", width=1.5,dash="dash"),
        )
    )

    fig.update_layout(yaxis_title=None)
    fig.update_layout(xaxis_title=None)
    fig.update_layout(
        showlegend=True,
        margin=dict(l=4, r=4, b=10, t=30, pad=1),
        title="",
        template="plotly_white",
        font=dict(size=10),
        legend_title_text=None,
    )

    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="right", x=0.85)
    )
    
    fig.update_layout(
        xaxis=dict(
            range=[
                information['stock_info']["Date"].iloc[0],
                information['stock_info']["Date"].iloc[-1]
            ],
            automargin=True
        )
    )

    return fig

def bar_plot(information,type_plot):
    fig = go.Figure()
    if type_plot=='daily':
        upper_limit = round(float((information.get('stock_info')["Volume_Upg"]/1000000).quantile(0.85)),2)
        lower_limit = round(float((information.get('stock_info')["Volume_Upg"]/1000000).quantile(0.045)),2)
        length      = information.get('stock_info').shape[0]
        fig.add_trace(
            go.Bar(
                x=information.get('stock_info')["Date"],
                y=information.get('stock_info')["Volume_Upg"]/1000000,
                name="Volume Upg",

                text=information.get('stock_info')[["Date", "Close", "Stock_Name", "nature", "Volume_Upg"]].apply(
                    lambda row: f"Date: {row['Date']}<br>Close: {round(row['Close'], 2)}<br>Stock Name: {row['Stock_Name']}<br>Nature:{row['nature']}<br>Volume: {round(row['Volume_Upg'], 2)}",
                    axis=1,
                ),
                hoverinfo="text",
                marker=dict(
                    color=information.get('stock_info')['nature'].map({'Buy': 'green', 'Sell': 'red'}),  # Assign colors manually
                ),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=information.get('stock_info')["Date"].values,
                y=np.repeat(upper_limit,length),
                name="upper_limit",
                # text=information.get('stock_info')[["Date", "MAE_25", "Stock_Name",  "Volume_Upg"]].apply(
                #     lambda row: f"Date: {row['Date']}<br>MAE_25: {round(row['MAE_25'], 2)}<br>Stock Name: {row['Stock_Name']}<br>Volume: {round(row['Volume_Upg'], 2)}",
                #     axis=1,
                # ),
                hoverinfo="text",
                line=dict(color="black", width=1.5,dash="dash"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=information.get('stock_info')["Date"].values,
                y=np.repeat(lower_limit,length),
                name="lower_limit",
                # text=information.get('stock_info')[["Date", "MAE_25", "Stock_Name",  "Volume_Upg"]].apply(
                #     lambda row: f"Date: {row['Date']}<br>MAE_25: {round(row['MAE_25'], 2)}<br>Stock Name: {row['Stock_Name']}<br>Volume: {round(row['Volume_Upg'], 2)}",
                #     axis=1,
                # ),
                hoverinfo="text",
                line=dict(color="black", width=1.5,dash="dash"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=information.get('buy_signal_info')["Date"],
                y=information.get('buy_signal_info')["Volume_Upg"]/1000000,
                name="Buy Signal",
                mode='markers',  # Show both markers and lines
                #line=dict(width=2, dash="solid"),  # Solid line connecting points
                marker=dict(symbol='circle', size=10, color='green',opacity=0.6),  # Marker style
            )
        )

        fig.add_trace(
            go.Scatter(
                x=information.get('sell_signal_info')["Date"],
                y=information.get('sell_signal_info')["Volume_Upg"]/1000000,
                name="Sell Signal",
                mode='markers',  # Show both markers and lines
                #line=dict(width=2, dash="solid"),  # Solid line connecting points
                marker=dict(symbol='circle', size=10, color='red',opacity=0.6),  # Marker style
            )
        )

        fig.add_trace(
            go.Scatter(
                x=information.get('trend_change_info')["Date"],
                y=information.get('trend_change_info')["Volume_Upg"]/1000000,
                name="Trend Change Signal",
                mode='markers',  # Show both markers and lines
                #line=dict(width=2, dash="solid"),  # Solid line connecting points
                marker=dict(symbol='circle', size=10, color='orange',opacity=0.6),  # Marker style
            )
        )

        fig.update_layout(yaxis_title=None)
        fig.update_layout(xaxis_title=None)
        fig.update_layout(
            showlegend=True,
            margin=dict(l=4, r=4, b=10, t=30, pad=1),
            title="",
            template="plotly_white",
            font=dict(size=10),
            legend_title_text=None,
        )
        fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="right", x=0.8)
        )  
        fig.update_layout(
            xaxis=dict(
                range=[
                    information.get('stock_info')["Date"].iloc[0],
                    information.get('stock_info')["Date"].iloc[-1]
                ],
                automargin=True
            )
        )
        
    if type_plot=='weekly':   
        upper_limit = round(float((information.get('volume_info')["Total Volume"]/1000000).quantile(0.85)),2)
        lower_limit = round(float((information.get('volume_info')["Total Volume"]/1000000).quantile(0.045)),2)
        length      = information.get('volume_info').shape[0]
        fig.add_trace(
            go.Bar(
                x=information.get('volume_info')['weekly_date'],
                y=information.get('volume_info')["Total Volume"]/1000000,
                name="Total Volume",

                text=information.get('volume_info')[['weekly_date',"Total Volume"]].apply(
                    lambda row: f"Date: {row['weekly_date']}<br>Volume: {round(row['Total Volume']/1000000, 2)}",
                    axis=1,
                ),
                hoverinfo="text",
                marker=dict(
                    color=information.get('volume_info')['nature'].map({'Buy': 'green', 'Sell': 'red'}),  # Assign colors manually
                ),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=information.get('volume_info')["weekly_date"].values,
                y=np.repeat(upper_limit,length),
                name="upper_limit",
                # text=information.get('stock_info')[["Date", "MAE_25", "Stock_Name",  "Volume_Upg"]].apply(
                #     lambda row: f"Date: {row['Date']}<br>MAE_25: {round(row['MAE_25'], 2)}<br>Stock Name: {row['Stock_Name']}<br>Volume: {round(row['Volume_Upg'], 2)}",
                #     axis=1,
                # ),
                hoverinfo="text",
                line=dict(color="black", width=1.5,dash="dash"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=information.get('volume_info')["weekly_date"].values,
                y=np.repeat(lower_limit,length),
                name="lower_limit",
                # text=information.get('stock_info')[["Date", "MAE_25", "Stock_Name",  "Volume_Upg"]].apply(
                #     lambda row: f"Date: {row['Date']}<br>MAE_25: {round(row['MAE_25'], 2)}<br>Stock Name: {row['Stock_Name']}<br>Volume: {round(row['Volume_Upg'], 2)}",
                #     axis=1,
                # ),
                hoverinfo="text",
                line=dict(color="black", width=1.5,dash="dash"),
            )
        )
        fig.update_layout(yaxis_title=None)
        fig.update_layout(xaxis_title=None)
        fig.update_layout(
            showlegend=False,
            margin=dict(l=4, r=4, b=10, t=30, pad=1),
            title="",
            template="plotly_white",
            font=dict(size=10),
            legend_title_text=None,
        )
        fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="right", x=0.9)
        )  

        fig.update_layout(
            xaxis=dict(
                range=[
                    information.get('volume_info')["weekly_date"].iloc[0],
                    information.get('volume_info')["weekly_date"].iloc[-1]
                ],
                automargin=True
            )
        )
            
    return fig

class Analysis:
    def __init__(self,dataset):
        self.__data = pd.DataFrame(dataset)
        self.__data.columns = ['Date','Stock_Name','Close', 'High', 'Low', 'Open', 'Volume','Volume_Upg','MAE_200', 'MAE_100', 'MAE_50', 'MAE_25', 'MAE_9']

    def transform_info(self):
        stock_info = self.__data.copy()
            
        stock_info['Volume_Upg'] = [volume if close_price>=open_price else -volume 
                                            for open_price, close_price, volume in zip(stock_info['Open'],
                                                                                        stock_info['Close'],
                                                                                        stock_info['Volume'])
                                ]
            
        stock_info['diff_mae'] = stock_info['MAE_25']-stock_info['MAE_50']
        

        limit_threshold   = int((stock_info['Close']-stock_info['MAE_25']).quantile(0.84))
        moving_avg_thresh = abs(int((stock_info['MAE_25']-stock_info['MAE_50']).quantile(0.25)))
        
        stock_info['diff_close_mae'] = stock_info['Close']-(stock_info['MAE_25']-limit_threshold)    
        diff_close_info   = abs(int(stock_info['diff_close_mae'].quantile(0.25)))
        
        trend_change_info = stock_info[
                                        (stock_info['MAE_25'] > stock_info['MAE_50']) &
                                        ((stock_info['diff_mae'] <= moving_avg_thresh) | 
                                        (stock_info['diff_mae'] <= -moving_avg_thresh))
                                    ]
        
        buy_signal_info  = stock_info[
                            ((stock_info['MAE_25']-limit_threshold+diff_close_info//2)>stock_info['Close'])
                            ]
        
        sell_signal_info = stock_info[
                            (stock_info['Close']>stock_info['MAE_25']+limit_threshold)
                            ]
        if buy_signal_info.shape[0]!=0:
            buy_to_sell_ratio = round(sell_signal_info.shape[0]/buy_signal_info.shape[0],2)
            
        if buy_signal_info.shape[0]==0:    
            buy_to_sell_ratio = round(sell_signal_info.shape[0]/1,2)
            
        stock_info['nature']      = stock_info["Volume_Upg"].apply(lambda text:'Buy' if text>0 else 'Sell')
        stock_info['weekly_date'] = pd.to_datetime(stock_info['Date']).dt.to_period('W').apply(lambda r: r.end_time)
        stock_info['weekly_date'] = stock_info['weekly_date'].apply(lambda text_info:str(text_info).split(" ")[0])
        
        volume_info = stock_info.groupby(['weekly_date'])['Volume_Upg'].agg(['sum']).reset_index()
        volume_info.rename(columns={"sum":"Total Volume"},inplace=True)    
        volume_info['nature'] = volume_info['Total Volume'].apply(lambda text_info: 'Buy' if  text_info>0 else 'Sell')

        return {'stock_info':stock_info,
                'trend_change_info':trend_change_info,
                'buy_signal_info':buy_signal_info,
                'sell_signal_info':sell_signal_info,
                'buy_to_sell_ratio':buy_to_sell_ratio,
                'limit_threshold':limit_threshold,
                'stock_name':stock_info['Stock_Name'].unique()[0],
                'volume_info':volume_info
            }
       
def stock_statistics(information,start_date,end_date):
    stock_info = information.get("stock_info")
    if stock_info.shape[0]!=0:
        current_info  = stock_info[stock_info['Date']==stock_info['Date'].max()]
        current_price = round(float(current_info['Close'].values[0]),2)
        sell_to_buy   = information.get("buy_to_sell_ratio")
        skweness      = float(round((information.get("volume_info")[(information.get("volume_info")['weekly_date']>=start_date) &
                                                       (information.get("volume_info")['weekly_date']<=end_date)
                                                       ]["Total Volume"]/1000000).skew(),3))
        
        utilization   = float((round((current_info['Close']-current_info['MAE_25'])/(information.get("limit_threshold")+1),2)*100).values[0])
    
    if stock_info.shape[0]==0:
        current_price = 'Not Found'
        sell_to_buy   = 0
        skweness      = ''
        utilization   = ''

    return {
        'current_price': current_price,
        'sell_to_buy'  : sell_to_buy,
        'skweness'     : skweness,
        'utilization'  : round(utilization,2)
    }
    
class Stock_Info:
    def __init__(self,stock_name,start_date,end_date):
        self.stock_name  = stock_name
        self.start_date  = start_date
        self.end_date    = end_date

    def load_data(self,postgres_db):
        query = text("""
                        SELECT time, stock_name, close_price, high_price, low_price, open_price, volume, volume_upg, 
                                moving_avg_200, moving_avg_100, moving_avg_50, moving_avg_25, moving_avg_9 FROM share_price
                        WHERE stock_name = :stock_name AND 
                              time       >=:start_date AND 
                              time       <=:end_date
                        ORDER BY time ASC                    
                     """)
        
        query_parameter = {
            "stock_name" : self.stock_name,
            "start_date" : self.start_date,
            "end_date"   : self.end_date    
        }

        with postgres_db.connect() as conn:
            stock_info         = conn.execute(query,query_parameter)
            fetch_stock_detail = stock_info.fetchall()

            transform_info = [Share_Price_Info( time            = row[0],
                                                stock_name      = row[1],
                                                close_price     = row[2],
                                                high_price      = row[3],
                                                low_price       = row[4],
                                                open_price      = row[5],
                                                volume          = row[6],
                                                volume_upg      = row[7],
                                                moving_avg_200  = row[8],
                                                moving_avg_100  = row[9],
                                                moving_avg_50   = row[10],
                                                moving_avg_25   = row[11],
                                                moving_avg_9    = row[12]).model_dump() for row in fetch_stock_detail]
            
            return transform_info
        
def get_categorical_info(dataset,cols_name):
    common_info =[]
    for text in abs(dataset[cols_name].values): # cols_name = 'percent'
        if 0<=text<=10:
            status ='L1'
            
        if 10<text<=20:
            status ='L2'
            
        if 20<text<30:
            status ='L3'
            
        if 30<text<=40:
            status ='L4'
            
        if 40<text<=50:
            status ='L5'
            
        if 50< text<=60:
            status ='L6'
            
        if 60<text<=70:
            status = 'L7'
        
        if 70<text<=80:
            status = 'L8'
        
        if 80<text<=90:
            status = 'L9'
            
        if text>90:
            status='L10'
        common_info.append(status)
    return common_info

class Best_Stocks:
    def __init__(self, start_date, end_date):
        self.__start_date = start_date
        self.__end_date   = end_date  

    def load_dataset(self,postgres_db):
        query = text("""SELECT  
                                t2.time, 
                                t2.stock_name, 
                                t2.close_price, 
                                t2.moving_avg_25, 
                                t2.status, 
                                t1.industry 
                            FROM 
                                price_action_info AS t2
                            LEFT JOIN 
                                nifty500 AS t1
                                ON t2.stock_name = t1.stock_name
                            WHERE 
                                t2.time > :start_date
                                AND t2.time <= :end_date;
                    """)
        
        query_parameter = {
                            "start_date" : self.__start_date,
                            "end_date"   : self.__end_date    
                          }
        
        with postgres_db.connect() as conn:
            extracted_info   = conn.execute(query,query_parameter)
            outcomes         = extracted_info.fetchall()        
            result1 = pd.DataFrame(outcomes,columns=['Date','Stock_Name','Close','MAE_25','Status','Industry'])
            return result1
        
    def get_best_performing_stocks(self,dataset):
        sell_info = dataset[dataset['Status']=='Sell Signal'].groupby(['Stock_Name'])['Status'].agg(['count']).reset_index()
        sell_info.rename(columns={"count":"Sell"},inplace=True)
        sell_info['Sell'].fillna(0,inplace=True)   

        buy_info = dataset[dataset['Status']=='Buy Signal'].groupby(['Stock_Name'])['Status'].agg(['count']).reset_index()
        buy_info.rename(columns={"count":"Buy"},inplace=True)
        buy_info['Buy'].fillna(0,inplace=True)     

        mapping = dataset.groupby(['Stock_Name','Industry'])['Industry'].agg(['count']).reset_index().iloc[:,:-1]
        merge_info1 = pd.merge(sell_info,buy_info,left_on=['Stock_Name'],right_on=['Stock_Name'],how='left')
        merge_info2 = pd.merge(merge_info1,mapping,left_on=['Stock_Name'],right_on=['Stock_Name'],how='left')
        merge_info2.fillna(1,inplace=True)

        merge_info2['Sell_to_Buy_Ratio'] = round((merge_info2['Sell']/merge_info2['Buy'])*10,2)
        merge_info2 = merge_info2.sort_values("Sell_to_Buy_Ratio",ascending=False)

        merge_info2['info'] = get_categorical_info(merge_info2,"Sell_to_Buy_Ratio")
        
        return merge_info2
    
def area_plot_best_stock(plotset,thresh):

    fig = go.Figure()
    color_discrete_gainer  = {
        'L1': 'honeydew', 'L2': 'palegreen', 'L3': 'lightgreen', 
        'L4': 'mediumseagreen', 'L5': 'limegreen', 'L6': 'yellowgreen', 
        'L7': 'darkseagreen', 'L8': 'forestgreen', 'L9': 'forestgreen', 'L10': 'green'
    }

    # Plot
    fig = px.treemap(
        plotset[(plotset['Sell_to_Buy_Ratio']>=thresh)],
        path=['Industry', 'Stock_Name'],
        values='Sell_to_Buy_Ratio',
        color='info',
        hover_data=['Sell_to_Buy_Ratio','info'],
        color_discrete_map=color_discrete_gainer,
    )

    fig.update_layout(margin=dict(t=5,l=10,r=10,b=10))   

    return fig

class Stock_Performance:
    def __init__(self, start_date, thresh, sell_to_buy_info,type_plot):
        self.start_date        = start_date   
        self.sell_to_buy_info  = sell_to_buy_info   
        self.type_plot         = type_plot
        self.thresh            = thresh

    def load_dataset(self,postgres_db):
        query = text("""
                SELECT 
                    t1.time,
                    t1.stock_name,
                    t1.close_price,
                    t1.volume_upg,
                    t1.moving_avg_25,
                    t2.threshold, 
                    t3.industry,
                    t2.sell_to_buy_ratio

                FROM share_price AS t1
                LEFT JOIN important_stocks AS t2
                ON t2.stock_name = t1.stock_name
                
                LEFT JOIN  nifty500 as t3
                    ON t1.stock_name = t3.stock_name
                WHERE t1.time = :start_date AND 
                      t2.time = '2025-01-01';
                """)        
        
        query_parameter = {
                            "start_date" : self.start_date
                          }
        
        with postgres_db.connect() as conn:
            extracted_info   = conn.execute(query,query_parameter)
            outcomes         = extracted_info.fetchall()        
            result = pd.DataFrame(outcomes,columns=['Date','Stock_Name','Close','Volume','Moving_avg_25','Thresh','Industry','Sell_to_Buy_ratio'])
            return result
        
    def get_stock_info(self, dataset):
        dataset['Utilization'] = ((dataset['Close']-dataset['Moving_avg_25'])/(dataset['Thresh']+1))*100
        dataset['Status']      =  dataset['Utilization'].apply(lambda text_info:'Sell' if text_info>0 else 'Buy')
        dataset['Utilization'] = dataset['Utilization'].apply(lambda text_info:abs(text_info))
        dataset['info']        = get_categorical_info(dataset,'Utilization')
       
        if self.type_plot =='stock gainer':
           status_info = 'Sell'

        if self.type_plot =='stock losser':
            status_info = 'Buy'

        if self.sell_to_buy_info=='>=1':
            filter_info = dataset[(dataset['Status']==status_info) & (dataset['Sell_to_Buy_ratio']>=1)]
        
        if self.sell_to_buy_info=='<=1':
            filter_info = dataset[(dataset['Status']==status_info) & (dataset['Sell_to_Buy_ratio']<=1)]


        return filter_info
    
def area_plot_stocks(plotset,type_plot, thresh):
    if type_plot =='stock gainer':
        color_discrete_map ={
                                    'L1': 'honeydew', 'L2': 'palegreen', 'L3': 'lightgreen', 
                                    'L4': 'mediumseagreen', 'L5': 'limegreen', 'L6': 'yellowgreen', 
                                    'L7': 'darkseagreen', 'L8': 'forestgreen', 'L9': 'forestgreen', 'L10': 'green'
                                } # color_discrete_gainer

    if type_plot =='stock losser':
        color_discrete_map = {
                                    'L1': 'lightcoral', 'L2': 'salmon', 'L3': 'darksalmon', 
                                    'L4': 'tomato', 'L5': 'orangered', 'L6': 'darkorange', 
                                    'L7': 'coral', 'L8': 'lightpink', 'L9': 'mistyrose', 'L10': 'firebrick'
                                } # color_discrete_losser
        
    fig = px.treemap(
        plotset[plotset['Utilization']>=thresh],
        path=['Industry', 'Stock_Name'],
        values='Utilization',
        color='info',
        hover_data=['Utilization','info','Close','Volume'],
        color_discrete_map=color_discrete_map,
    )
    fig.update_layout(margin=dict(t=5,l=10,r=10,b=10))

    return fig
        
def sector_stats(dataset,thresh,lable):
    if lable=='best performer':
        stats_info = dataset[dataset['Sell_to_Buy_Ratio']>=thresh].groupby(['Industry'])['info'].agg(['count']).reset_index()
        stats_info = stats_info.sort_values("count",ascending=False)

    if lable!='best performer':
        stats_info = dataset[dataset['Utilization']>=thresh].groupby(['Industry'])['info'].agg(['count']).reset_index()
        stats_info = stats_info.sort_values("count",ascending=False)

    mapping = []
    counter = 0
    if stats_info.shape[0]>=4:
        for row in  stats_info.values:
                mapping.append([row[0],round(row[1],2)])
                counter+=1
                if counter>=4:
                    break

    if stats_info.shape[0]<4:
        length = stats_info.shape[0]
        for row in  stats_info.values:
            mapping.append([row[0],round(row[1],2)])
            
        for i in range(0,4-length):
            mapping.append(['Not Found:{}'.format(i),''])

    return mapping


def get_signal(information, investment=80000, min_loss=1000, interval=5, min_return_threshold=0):
    import pandas as pd
    
    # Extract necessary columns
    filter_info = information.get('stock_info')[['Date', 'Stock_Name', 'Close', 'High', 'MAE_25', 'MAE_50']].copy()
    filter_info['Date'] = pd.to_datetime(filter_info['Date'])

    # Calculate the average reference price (simple moving average midpoint)
    filter_info['Reference'] = ((filter_info['MAE_25'] + filter_info['MAE_50']) / 2).round(2)

    date_map = {}
    iteration = 0

    for idx in range(0, len(filter_info), interval):
        # Limit to interval range
        window = filter_info.iloc[idx:idx + interval]
        if len(window) < 2:
            continue  # Not enough data to compare
        
        start_row = window.iloc[0]
        end_row = window.iloc[-1]

        current_price = start_row['Close']
        quantity = int(investment / current_price)
        threshold = int(min_loss / quantity)

        buy_counter = (window['Close'] > window['MAE_25']).sum()
        sell_counter = (window['MAE_25'] + threshold >= window['Close']).sum()

        # Determine status based on counter values
        if buy_counter > sell_counter:
            status = 'Buy'
        elif sell_counter > buy_counter:
            status = 'Sell'
        else:
            status = 'Neutral'

        # Map start-end information for each window
        start_date = str(start_row['Date'].date())
        end_date = str(end_row['Date'].date())
        date_map[start_date] = {
            'Start_Date': start_date,
            'End_Date': end_date,
            'Status': status,
            'Thresh': threshold,
            'Quantity': quantity,
            'Start_Price': round(current_price, 2),
            'End_Price': round(end_row['Close'], 2)
        }

    outcome = pd.DataFrame.from_dict(date_map, orient='index').reset_index(drop=True)

    # Clean up repeated statuses
    new_status = []
    previous_status = None
    for current_status in outcome['Status']:
        if current_status == previous_status:
            new_status.append(previous_status)
        else:
            new_status.append(current_status)
        previous_status = current_status
    outcome['New_Status'] = new_status

    # Label buy sequences
    label = 0
    in_sequence = False
    labels = []

    for status in outcome['New_Status']:
        if status in ['Buy', 'Neutral']:
            if not in_sequence:
                label += 1
                in_sequence = True
            labels.append(label)
        elif status == 'Sell':
            if in_sequence:
                labels.append(label)
                in_sequence = False
            else:
                labels.append(None)
        else:
            labels.append(None)

    outcome['Labels'] = labels

    return outcome


def calculate_revenue(insights, categories, stock_data, min_return_threshold=0):
    total_profit = []
    buy_dates = []
    sell_dates = []
    comments = []
    for label in categories:
        trades = insights[insights['Labels'] == label]
        if trades.empty or len(trades) < 2:
            continue  # Skip if no valid trade sequence

        purchase_price = float(trades['End_Price'].values[0])
        sold_price = float(trades['End_Price'].values[-1])
        quantity = int(trades['Quantity'].values[0])

        profit_per_unit = sold_price - purchase_price
        profit_total = round(profit_per_unit * quantity, 2)

        # Apply return threshold filter
        if profit_total < min_return_threshold:
            continue

        start_date = trades['End_Date'].values[0]
        end_date = trades['End_Date'].values[-1]

        # print(f"Stock purchased at ₹{purchase_price} & sold at ₹{sold_price} "
        #       f"from {start_date} to {end_date} gives return: ₹{profit_total} "
        #       f"Qty: {quantity} per unit: ₹{round(profit_per_unit, 2)}")

        total_profit.append(profit_total)

        comments.append(f"Stock purchased at ₹{purchase_price} & sold at ₹{sold_price}  "
              f"from {start_date} to {end_date} gives return of ₹{profit_total}  "
              f"   (₹{round(profit_per_unit, 2)} profit get per {quantity}.Qty)")
        # Get all dates within this range
        date_range = stock_data[
            stock_data["Date"].astype(str).between(str(start_date), str(end_date))
        ]["Date"].values

        for d in date_range[:-1]:
            buy_dates.append(d)
        sell_dates.append(date_range[-1])

    # print(f"\n💰 Total revenue generated by Stock: ₹{round(sum(total_profit), 2)}")
     
    return total_profit, buy_dates, sell_dates, comments

def buy_to_sell_representations(information,buy_info,sell_info):

    fig = go.Figure()
    # print(information,'information')

    if type(information)==dict:
        # print(information.get('stock_info'),'information detail')
        if information.get('stock_info').shape[0]!=0:
            
            buy_information  = information.get('stock_info')[information.get('stock_info')['Date'].isin(buy_info)]
            sell_information = information.get('stock_info')[information.get('stock_info')['Date'].isin(sell_info)]

            # print(buy_information.shape,sell_information.shape)
            fig.add_trace(
                go.Scatter(
                    x=information.get('stock_info')["Date"].values,
                    y=information.get('stock_info')["Close"].values,
                    name="Close",
                    text=information.get('stock_info')[["Date", "Close", "Stock_Name",  "Volume_Upg"]].apply(
                        lambda row: f"Date: {row['Date']}<br>Close: {round(row['Close'], 2)}<br>Stock Name: {row['Stock_Name']}<br>Volume: {round(row['Volume_Upg'], 2)}",
                        axis=1,
                    ),
                    hoverinfo="text",
                    line=dict(color='#636EFA', width=2),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=information.get('stock_info')["Date"].values,
                    y=information.get('stock_info')["MAE_25"].values+information.get('limit_threshold'),
                    name="Upper Limit",
                    text=information.get('stock_info')[["Date", "MAE_25", "Stock_Name"]].apply(
                        lambda row: f"Date: {row['Date']}<br>Upper Limit: {round(row['MAE_25']+information.get('limit_threshold'),2)}<br>Stock Name: {row['Stock_Name']}",
                        axis=1,
                    ),
                    hoverinfo="text",
                    line=dict(color="black", width=1.5,dash="dash"),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=information.get('stock_info')["Date"].values,
                    y=information.get('stock_info')["MAE_25"].values-information.get('limit_threshold'),
                    name="Lower Limit",
                    text=information.get('stock_info')[["Date", "MAE_25", "Stock_Name"]].apply(
                        lambda row: f"Date: {row['Date']}<br>Lower Limit: {round(row['MAE_25']-information.get('limit_threshold'),2)}<br>Stock Name: {row['Stock_Name']}",
                        axis=1,
                    ),
                    hoverinfo="text",
                    line=dict(color="black", width=1.5,dash="dash"),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=buy_information["Date"],
                    y=buy_information["Close"],
                    name="SELL Signal",
                    mode='markers',  # Show both markers and lines
                    marker=dict(symbol='circle', size=7, color='green',opacity=0.6),  # Marker style
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=sell_information["Date"],
                    y=sell_information["Close"],
                    name="SELL Signal",
                    mode='markers',  # Show both markers and lines
                    marker=dict(symbol='circle', size=8, color='red',opacity=0.6),  # Marker style
                )
            )

            fig.add_trace(

                go.Scatter(
                    x=information.get('stock_info')["Date"].values,
                    y=information.get('stock_info')["MAE_25"].values,
                    name="MAE_25",
                    text=information.get('stock_info')[["Date", "MAE_25", "Stock_Name",  "Volume_Upg"]].apply(
                        lambda row: f"Date: {row['Date']}<br>MAE_25: {round(row['MAE_25'], 2)}<br>Stock Name: {row['Stock_Name']}<br>Volume: {round(row['Volume_Upg'], 2)}",
                        axis=1,
                    ),
                    hoverinfo="text",
                    line=dict(color="gray", width=1.5,dash="dash"),
                )
            )

            fig.add_trace(

                go.Scatter(
                    x=information.get('stock_info')["Date"].values,
                    y=information.get('stock_info')["MAE_50"].values,
                    name="MAE_50",
                    text=information.get('stock_info')[["Date", "MAE_50", "Stock_Name",  "Volume_Upg"]].apply(
                        lambda row: f"Date: {row['Date']}<br>MAE_50: {round(row['MAE_50'], 2)}<br>Stock Name: {row['Stock_Name']}<br>Volume: {round(row['Volume_Upg'], 2)}",
                        axis=1,
                    ),
                    hoverinfo="text",
                    line=dict(color="firebrick", width=1.5,dash="dash"),
                )
            )

            fig.update_layout(
                xaxis=dict(
                    range=[
                        information['stock_info']["Date"].iloc[0],
                        information['stock_info']["Date"].iloc[-1]
                    ],
                    automargin=True
                )
            )

    fig.update_layout(yaxis_title=None)
    fig.update_layout(xaxis_title=None)
    fig.update_layout(
        showlegend=True,
        margin=dict(l=4, r=4, b=10, t=30, pad=1),
        title="",
        template="plotly_white",
        font=dict(size=10),
        legend_title_text=None,
    )

    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="right", x=0.65)
    )
    
    return fig

class Historic_Info:
    def __init__(self,day_info):
        self.__day_info = day_info
        #   self.__query    = text(f"""
        #                             WITH dataset AS (
        #                                 SELECT *, 
        #                                        abs(close_price - moving_avg_50) AS diff,
        #                                        100 * abs(close_price - moving_avg_50) / moving_avg_50 AS percentage
        #                                 FROM price_action_info
        #                                 WHERE status != 'Buy Signal' 
        #                                   AND time = '{self.__day_info}'
        #                             )
        #                             SELECT 
        #                                 t1.time, 
        #                                 t1.stock_name, 
        #                                 t1.close_price, 
        #                                 t1.volume_upg, 
        #                                 t1.moving_avg_50, 
        #                                 t1.moving_avg_25, 
        #                                 t1.percentage, 
        #                                 ROUND(t1.diff::numeric, 2) AS rounded_diff,
        #                                 t2.sell_to_buy_ratio, 
        #                                 t2.threshold, 
        #                                 t2.skewness

        #                             FROM dataset AS t1

        #                             LEFT JOIN important_stocks AS t2
        #                                 ON t1.stock_name = t2.stock_name

        #                             WHERE (t1.close_price>t1.moving_avg_25) --and (t1.moving_avg_25 > t1.moving_avg_50)
        #                             ORDER BY t1.percentage DESC;             
        #                           """)
        self.__query    = text(f"""
                                    SELECT * FROM strategy_stocks
                                    WHERE time = '{self.__day_info}' AND
                                          percentage>1
                                """)
            
    def load_data(self, postgres_db):
          with postgres_db.connect() as conn:
                stock_info         = conn.execute(self.__query)
                fetch_stock_detail = stock_info.fetchall()
                
                return fetch_stock_detail
          

def categorical_info(feature):
    lable = []
    status = '0-5%'
    for vals in feature:
        if vals<=5:
            status = '0-5%'
            
        if 6<=vals<=10:
            status = '6-10%'
            
        if 11<=vals<=15:
            status = '11-15%'
            
        if 16<=vals<=20:
            status = '16-20%'
            
        if 21<=vals<=25:
            status = '21-25%'
            
        if 26<=vals<=30:
            status = '26-30%'
            
        if vals>=31:
            status = '>=31%'
        lable.append(status)    
    return lable   


def get_historical_info_bar_plot(plotset):
    # print(plotset.head())
    fig = go.Figure()
    if plotset.shape[0]!=0:
        plotset['percentage'] = plotset['percentage'].apply(lambda text_info:round(text_info,2))
        plotset['stock_name'] = plotset['stock_name'].apply(lambda text_info:text_info.replace(".NS",""))  
        
        plotset  = plotset.sort_values('stock_name',ascending=True)
        color_mapping = {
                        '0-5%': '#d4e157',       # Light green
                        '6-10%': '#aed581',
                        '11-15%': '#81c784',
                        '16-20%': '#4caf50',
                        '21-25%': '#388e3c',
                        '26-30%': '#2e7d32',
                        '31%+': '#1b5e20'
                        }
        plotset['color_code'] = categorical_info(plotset['percentage'])
        plotset['bar_color'] = plotset['color_code'].map(color_mapping)

        fig.add_trace(
            go.Bar(
                x=plotset['stock_name'],
                y=plotset['percentage'],
                marker=dict(color=plotset['bar_color']),
                name="Price Action",
                # REMOVE `text=...` to avoid label on bar
                hovertemplate=(
                    'Date: %{customdata[0]}<br>'
                    'Stock Name: %{customdata[1]}<br>'
                    'Percentage: %{customdata[2]}%<br>'
                    'Price: ₹%{customdata[3]}<extra></extra>'
                ),
                customdata=plotset[['time', 'stock_name', 'percentage', 'close_price']].values
            )
        )

    fig.update_layout(
        hovermode="x",  # or "closest"
        template="plotly_white",
        legend_title_text=None,
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=4, r=4, b=10, t=30, pad=1),
        title="",
        template="plotly_white",
        font=dict(size=10),
        legend_title_text=None,
    )
    
    return fig

# if __name__ == "__main__":
#     from connection import DB
#     db          = DB()
#     postgres_db = db.initiate_db()

#     obj = Stock_Info(stock_name = 'BAJFINANCE.NS',
#                      start_date = '2024-01-01',
#                      end_date   = '2025-12-31')
    
#     data = obj.load_data(postgres_db=postgres_db)

#     obj1 = Analysis(dataset=data)
#     info = obj1.transform_info()

#     plot1 = trend_plot(information=info)
#     plot1.show()

#     plot2 = bar_plot(information=info, type_plot='weekly')
#     plot2.show()
    
#     print(stock_statistics(information = info,
#                            start_date  = '2024-01-01',
#                            end_date    = '2025-12-31'))

    # obj3                 = Best_Stocks(start_date='2025-01-01',
    #                                    end_date='2025-12-31',
    #                                    )
    # load_data_best_stock = obj3.load_dataset(postgres_db=postgres_db)
    # plot_dataset         = obj3.get_best_performing_stocks(dataset=load_data_best_stock)

    # plot = obj3.area_plot(plotset=plot_dataset,thresh=50)
    # plot.show()

    # obj4 = Stock_Performance(start_date  = '2025-07-11',
    #                          thresh=25,
    #                          sell_to_buy_info='>=1',
    #                          type_plot='stock losser')
    
    # stock_performance_info = obj4.load_dataset(postgres_db=postgres_db)
    # clean_stock_info       =  obj4.get_stock_info(dataset=stock_performance_info)

    # plotset = obj4.area_plot(dataset=clean_stock_info)
    # plotset.show()
