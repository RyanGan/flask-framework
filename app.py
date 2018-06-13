# ----------------
# Title: Data Incubator Heroku/Flask Project
# Author: Ryan Gan
# Date Created: 2018-06-13
# ----------------

# ----------------
# loading required packages

# from flask import
from flask import Flask, render_template, request, redirect
# import requests; required for flask
import requests
# import pandas
import pandas as pd
# import bokeh
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.embed import components
# ----------------

# define app name
app = Flask(__name__)

# ----------------
# import stock prices csv
wiki_stock = pd.read_csv('./data/wiki_stock_price.csv')
# ----------------

# ----------------
# CUSTOM FUNCTIONS FOR PLOT

# custom function to return dataframe based on ticker price
def sub_data(stock_name):
    df = wiki_stock.loc[wiki_stock['ticker'] == stock_name]
    return df

# create time series plot function
def make_plot(df, pars):
    features = pars['features']
    stock_name = pars['stock_name']

    source = ColumnDataSource(data={
        'date': pd.to_datetime(df['date']),
        'adj_open': df.adj_open,
        'adj_close': df.adj_close,
        'open': df.open,
        'close': df.close,
    })

    # plot framework
    p = figure(title= stock_name + ' Stock Prices', x_axis_label='Date',
               x_axis_type='datetime', y_axis_label=r'Price ($)',
               plot_height=600, plot_width=600)

    # if nothing selected, then show close
    if not features:
        p.line(x='date', y='close', source=source, color='green', legend='Closing Price')

    if 'open' in features:
        p.line(x='date', y='open', source=source, color='blue', legend='Opening Price')

    if 'close' in features:
        p.line(x='date', y='close', source=source, color='green', legend='Closing Price')

    if 'adj_open' in features:
        p.line(x='date', y='adj_open', source=source, color='black',
               legend='Adjusted Opening Price')

    if 'adj_close' in features:
        p.line(x='date', y='adj_close', source=source, color='red',
               legend='Adjusted Closing Price')

    p.legend.location = 'top_left'

    return p


# Flask Application ----------------------------
@app.route('/')
def home():
    return render_template('index.html')

# define app route
@app.route('/index', methods=['GET', 'POST'])
def index():
    # register empty par dictionary
    pars = {}
    # GET method pulls up the base html page
    if request.method == 'GET':
        return render_template('index.html')
    # If not GET then POST; allows user requests
    elif request.method == 'POST':
        pars['stock_name'] = request.form['ticker']

        # request features from ticker options (i hope)
        pars['features'] = request.form.getlist('features')

        # subset df from wiki_stock
        df = sub_data(pars['stock_name'])

        plot = make_plot(df, pars)

        script, div = components(plot)

    return render_template('plot.html', p_script=script, p_div=div)

@app.route('/about')
def about():
    return render_template('about.html')

# ----------------
#if __name__ == '__main__':
#    app.run(host='0.0.0.0',port=33507, debug=True)
if __name__ == '__main__':
  app.run(port=33507, debug=True)
