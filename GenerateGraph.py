import bs4 as soup
import requests
import time
import os, sys
from time import gmtime, strftime
import pandas as pd
from bokeh.plotting import figure, show, output_file, save
import json

def makeGraph(ticker):
    try:
        os.remove('stock_information.html')
    except:
        print('file not currently existing')
    pi=3.14159265

    interval = '1min'

    with open('Secret.json') as f:
        keys = json.load(f)
    apikey = keys['AlphaAdvantageKey']
    # url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + ticker + '&interval='+interval+'&outputsize=full&apikey='+apikey
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&outputsize=full&apikey='+apikey
    print(url)
    r = requests.get(url)
    result = r.json()
    dataForAllDays = result['Time Series (Daily)']

    #convert to dataframe
    df = pd.DataFrame.from_dict(dataForAllDays, orient='index') 
    df = df.reset_index()

    #rename columns
    df = df.rename(index=str, columns={"index": "date", "1. open": "open", "2. high": "high", "3. low": "low", "4. close": "close","5. volume":"volume"})

    #Changing to datetime
    df['date'] = pd.to_datetime(df['date'])

    #Sort according to date
    df = df.sort_values(by=['date'])

    #Changing the datatype 
    df.open = df.open.astype(float)
    df.close = df.close.astype(float)
    df.high = df.high.astype(float)
    df.low = df.low.astype(float)
    df.volume = df.volume.astype(int)

    #check the data
    df.head()

    #Check the datatype
    df.info()

    inc = df.close > df.open
    dec = df.open > df.close
    w = 12*60*60*1000 # half day in ms
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    title = ticker + ' Chart'
    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title = title)
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha=0.3
    p.segment(df.date, df.high, df.date, df.low, color="black")
    p.vbar(df.date[inc], w, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
    p.vbar(df.date[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")
    #Store as a HTML file
    output_file("stock_information.html", title="candlestick.py example")
    save(p)
    # Display in browser
    # show(p)




# THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# my_file_path = os.path.join(THIS_FOLDER, ticker+' '+strftime("%Y_%m_%d %H_%M_%S", gmtime())+ '.json')
# my_file = open(my_file_path, 'w')
# my_file.write(r.text)
# my_file.close()
