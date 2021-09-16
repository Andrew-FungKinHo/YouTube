import pandas as pd
import datetime as dt
import pandas_datareader.data as web

# change the default plotting to plotly
pd.options.plotting.backend = 'plotly'

# specify stock ticker and timeframe in concern
stock_chosen = ‘GME’
start = dt.datetime(2020,12,1)
end = dt.datetime(2021,2,17)
days_concerned = 14

# retrieve data within the timeframe and store it in df
df = web.get_data_yahoo(stock_chosen,start,end)

# get the closing price of the previous day
df['Previous Close'] = df['Adj Close'].shift()

# The 3 calculations of True Range 
df['High - Low'] = df['High'] - df['Low']
df['High - PClose'] = abs(df['High'] - df['Previous Close'])
df['Low - PClose'] = abs(df['Low'] - df['Previous Close'])

# Compute the max out of the 3
df['True_Range'] = df[['High - Low','High - PClose','Low - PClose']].max(axis=1)

# get the average TR for the previous 14 days or days_concerned 
df['ATR'] = df.True_Range.rolling(window = days_concerned).mean() / df['Adj Close'] * 100

# actual figure plotting
fig = df['ATR'].plot()

# customize the plot
fig.update_layout(
    title = f'{stock_chosen} {days_concerned}-day Average True Range %',
    yaxis_title= 'ATR (%)',
    legend_title='technical indicator'
)

# visualize the plot
fig.show()
