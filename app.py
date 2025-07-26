import os
import secrets
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio


import warnings
warnings.filterwarnings('ignore')

from quart import Quart, flash, jsonify, redirect, render_template, request, send_file, session, url_for
from plotly import graph_objects as go
from datetime import datetime, timedelta
from src.utility import users, get_home_dropdwon_info
from src.connection import DB
from src.functions import Analysis, Stock_Info, stock_statistics, trend_plot, bar_plot,Best_Stocks,Stock_Performance,area_plot_best_stock,area_plot_stocks,sector_stats
import asyncio

db          = DB()
postgres_db = db.initiate_db()

# User data for Demonstration
USERS = users.get("users")
current_date = str(datetime.now()).split(" ")[0]

# Application Configrations
app = Quart(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(24))

metadata = get_home_dropdwon_info()

@app.route("/login", methods=["GET", "POST"])
async def login():
    if request.method == "POST":
        form = await request.form
        username = form.get("username")
        password = form.get("password")
        if USERS.get(username) == password:
            session["username"] = username
            await flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            await flash("Invalid credentials, please try again.", "danger")
    return await render_template("login.html")


@app.route("/logout")
async def logout():
    session.pop("username", None)
    session.pop("home_form_data", None)
    session.pop("page_form_data", None)
    await flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/")
async def home():
    if "username" in session:

        get_stock_info = Stock_Info(stock_name = metadata["selected_stock"],
                                    start_date = metadata["start_date"],
                                    end_date   = metadata["end_date"])
        
        data_processing     = get_stock_info.load_data(postgres_db=postgres_db)
        
        data_transformation = Analysis(dataset=data_processing)

        information         = data_transformation.transform_info()
        
        home_stats          = stock_statistics(information  = information,
                                                start_date  = metadata["start_date"],
                                                end_date    = metadata["end_date"])
        
        #{'current_price': 2530.0, 'sell_to_buy': 2.97, 'skweness': 0.758, 'utilization': -61.0}
        metadata['current_price'] = home_stats['current_price']
        metadata['sell_to_buy']   = home_stats['sell_to_buy']
        metadata['skweness']      = home_stats['skweness']
        metadata['utilization']   = home_stats['utilization']
        metadata['information']   = information

        # print(metadata['information'].keys())

        return await render_template(
            "home.html",
            username=session["username"],
            form_data=metadata,
            current_date=current_date,
            years = current_date.split("-")[0]
        )
    return redirect(url_for("login"))


@app.route("/submit_home_form", methods=["POST"])
async def submit_home_form():
    form = await request.form
    start_date = form.get("start_date")
    end_date   = form.get("end_date")
    stock_name = form.get("stock_names")
    volm_plot_type = form.get('volume_plot_type') 

    # print(stock_name,start_date,end_date)

    unselected_stocks = [stocks for stocks in metadata['stock_names'] if stocks!=stock_name]
    unselected_volm   = [volm_info for volm_info in metadata['volume_plot_type'] if volm_info!=volm_plot_type]

    metadata["stock_names"]    = [stock_name] + unselected_stocks
    metadata['volume_plot_type']    = [volm_plot_type] + unselected_volm
    metadata["start_date"]     = start_date
    metadata["end_date"]       = end_date
    metadata['selected_stock'] = stock_name
    metadata['selected_volm']  = volm_plot_type

    flash("Form submitted successfully for Home page!", "success")
    return redirect(url_for("home"))

@app.route("/sector")
async def sector():
    if "username" in session:
        
        if metadata['selected_sector_plot']=='best performer':
            get_best_stocks     = Best_Stocks(start_date  = metadata["sector_start_date"],
                                              end_date    = metadata["sector_end_date"],
                                            )
            
            load_best_stock_dataset = get_best_stocks.load_dataset(postgres_db=postgres_db)
            plot_dataset            = get_best_stocks.get_best_performing_stocks(dataset=load_best_stock_dataset)

        if metadata['selected_sector_plot']!='best performer':
            get_stock_performance = Stock_Performance(start_date  = metadata["sector_end_date"],
                                                      thresh      = int(metadata["selected_thresh_limit"]),
                                                      sell_to_buy_info = metadata["selected_sell_to_buy_ratio"],
                                                      type_plot        = metadata["selected_sector_plot"])
            
            load_best_stock_dataset = get_stock_performance.load_dataset(postgres_db=postgres_db)
            plot_dataset            = get_stock_performance.get_stock_info(dataset=load_best_stock_dataset)

        metadata['Best_Stock_Metadata'] = plot_dataset

        metadata['sector_stats'] = sector_stats(dataset = plot_dataset,
                                                thresh  = int(metadata["selected_thresh_limit"]),
                                                lable   = metadata['selected_sector_plot'])

        # print(metadata['sector_stats'])

        # print(meta_info,'sectorial info')
        return await render_template(
                "sector.html",
                username=session["username"],
                form_data=metadata,
                current_date=current_date,
                years = current_date.split("-")[0]
            )
    
    return redirect(url_for("login"))

@app.route("/submit_sectoral_form", methods=["POST"])
async def submit_sectoral_form():

    form = await request.form
    sector_start_date              = form.get("sector_start_date")
    sector_end_date                = form.get("sector_end_date")
   
    threshold_limit         = form.get('threshold_limit') 
    type_of_sector_plot     = form.get('type_of_sector_plot') 
    sell_to_buy_sector_info = form.get('sell_to_buy_sector_info') 

    unselected_threshold     = [thresh for thresh in metadata['threshold_limit'] if thresh!=threshold_limit]
    unselected_sector_plot   = [type_sector for type_sector in metadata['type_of_sector_plot'] if type_sector!=type_of_sector_plot]
    unselected_sell_buy_info = [but_sell_info for but_sell_info in metadata['sell_to_buy_sector_info'] if but_sell_info!=sell_to_buy_sector_info]

    metadata["threshold_limit"]         = [threshold_limit] + unselected_threshold
    metadata['type_of_sector_plot']        = [type_of_sector_plot] + unselected_sector_plot
    metadata['sell_to_buy_sector_info'] = [sell_to_buy_sector_info] + unselected_sell_buy_info

    metadata["sector_start_date"]   = sector_start_date
    metadata["sector_end_date"]     = sector_end_date

    metadata["selected_sector_plot"]       = type_of_sector_plot
    metadata["selected_thresh_limit"]      = threshold_limit
    metadata["selected_sell_to_buy_ratio"] = sell_to_buy_sector_info

    flash("Form submitted successfully for Home page!", "success")
    return redirect(url_for("sector"))

@app.route("/line-chart")
async def line_chart_data():
    plotdata = await asyncio.to_thread(trend_plot, information=metadata['information'])
    graph_json = pio.to_json(plotdata)
    return jsonify({"graph_json": graph_json})


@app.route("/bar-chart")
async def bar_chart_data():
    plotdata = await asyncio.to_thread(bar_plot, information=metadata['information'], type_plot=metadata['selected_volm'])
    # Convert the chart to JSON
    graph_json = pio.to_json(plotdata)
    return jsonify({"graph_json": graph_json})

@app.route("/tree-sectoral-chart")
async def tree_sectoral_chart_data():

    if metadata['Best_Stock_Metadata'].shape[0]!=0:
        if metadata['selected_sector_plot']=='best performer':
            plotdata = await asyncio.to_thread(area_plot_best_stock, 
                                            plotset   = metadata['Best_Stock_Metadata'], 
                                            thresh    = int(metadata['selected_thresh_limit']))
    
        if metadata['selected_sector_plot']!='best performer':
            plotdata = await asyncio.to_thread(area_plot_stocks, 
                                            plotset   = metadata['Best_Stock_Metadata'],
                                            type_plot = metadata['selected_sector_plot'], 
                                            thresh    = int(metadata['selected_thresh_limit']))
            
    if metadata['Best_Stock_Metadata'].shape[0]==0:
        plotdata = go.Figure()
        plotdata.update_layout(yaxis_title=None)
        plotdata.update_layout(xaxis_title=None)
        plotdata.update_layout(
            showlegend=True,
            margin=dict(l=4, r=4, b=10, t=30, pad=1),
            title="",
            template="plotly_white",
            font=dict(size=10),
            legend_title_text=None,
        )

        plotdata.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="right", x=0.85)
        )

    # Convert the chart to JSON
    graph_json = pio.to_json(plotdata)
    return jsonify({"graph_json": graph_json})

if __name__ == "__main__":
    app.run(debug=True)