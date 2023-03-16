import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as pdr
import seaborn as sns
import yfinance as yf
from datetime import datetime

sns.set_style('whitegrid')
plt.style.use("fivethirtyeight")

yf.pdr_override()

tech_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN']

end = datetime.now()
start = datetime(end.year - 1, end.month, end.day)

for stock in tech_list:
     globals()[stock] = yf.download(stock, start, end)

company_list = [AAPL, GOOG, MSFT, AMZN]
company_name = ["APPLE", "GOOGLE", "MICROSOFT", "AMAZON"]

for company, com_name in zip(company_list, company_name):
    company["company_name"] = com_name

df = pd.concat(company_list, axis=0)

closing_df = pdr.get_data_yahoo(tech_list, start=start, end=end)['Adj Close']


tech_rets = closing_df.pct_change()
tech_rets.head()

def get_data_frame():
    dict = []
    i=1
    for index, row in df.iterrows():
        dict1 = {}
        dict1['id'] = i
        dict1['date'] = str(index)
        for c, v in row.items():
            s = str(c).lower()
            dict1[s] = v
        dict.append(dict1)
        i+=1
    return dict


def descriptive_historical_cv():
    plt.figure(figsize=(15, 10), facecolor='white')
    plt.subplots_adjust(top=1.25, bottom=1.2)

    for i, company in enumerate(company_list, 1):
        plt.subplot(2, 2, i)
        company['Adj Close'].plot()
        plt.ylabel('Adj Close')
        plt.xlabel(None)
        plt.title(f"Closing Price of {tech_list[i - 1]}")

    plt.tight_layout()
    plt.savefig("C:/Users/milja/PycharmProjects/flaskProject/stocks.png")

    return 'stocks.png'


def descriptive_historical_vos():
    plt.figure(figsize=(15, 10), facecolor='white')
    plt.subplots_adjust(top=1.25, bottom=1.2)

    for i, company in enumerate(company_list, 1):
        plt.subplot(2, 2, i)
        company['Volume'].plot()
        plt.ylabel('Volume')
        plt.xlabel(None)
        plt.title(f"Sales Volume for {tech_list[i - 1]}")

    plt.tight_layout()
    plt.savefig("C:/Users/milja/PycharmProjects/flaskProject/stocks2.png")

    return 'stocks2.png'


def moving_average_price(day1, day2, day3):
    ma_day = [int(day1), int(day2), int(day3)]

    str1 = 'MA for ' + day1 + ' days'
    str2 = 'MA for ' + day2 + ' days'
    str3 = 'MA for ' + day3 + ' days'

    for ma in ma_day:
        for company in company_list:
            column_name = f"MA for {ma} days"
            company[column_name] = company['Adj Close'].rolling(ma).mean()

    fig, axes = plt.subplots(nrows=2, ncols=2)
    fig.set_figheight(10)
    fig.set_figwidth(15)

    AAPL[['Adj Close', str1, str2, str3]].plot(ax=axes[0, 0])
    axes[0, 0].set_title('APPLE')

    GOOG[['Adj Close', str1, str2, str3]].plot(ax=axes[0, 1])
    axes[0, 1].set_title('GOOGLE')

    MSFT[['Adj Close', str1, str2, str3]].plot(ax=axes[1, 0])
    axes[1, 0].set_title('MICROSOFT')

    AMZN[['Adj Close', str1, str2, str3]].plot(ax=axes[1, 1])
    axes[1, 1].set_title('AMAZON')

    fig.tight_layout()
    fig.savefig("C:/Users/milja/PycharmProjects/flaskProject/stocks3.png")

    return 'stocks3.png'


def daily_returns():
    for company in company_list:
        company['Daily Return'] = company['Adj Close'].pct_change()

    fig, axes = plt.subplots(nrows=2, ncols=2)
    fig.set_figheight(10)
    fig.set_figwidth(15)

    AAPL['Daily Return'].plot(ax=axes[0, 0], legend=True, linestyle='--', marker='o')
    axes[0, 0].set_title('APPLE')

    GOOG['Daily Return'].plot(ax=axes[0, 1], legend=True, linestyle='--', marker='o')
    axes[0, 1].set_title('GOOGLE')

    MSFT['Daily Return'].plot(ax=axes[1, 0], legend=True, linestyle='--', marker='o')
    axes[1, 0].set_title('MICROSOFT')

    AMZN['Daily Return'].plot(ax=axes[1, 1], legend=True, linestyle='--', marker='o')
    axes[1, 1].set_title('AMAZON')

    fig.tight_layout()
    fig.savefig("C:/Users/milja/PycharmProjects/flaskProject/stocks4.png")

    return 'stocks4.png'


def avg_daily_returns():
    plt.figure(figsize=(12, 9), facecolor='white')

    for i, company in enumerate(company_list, 1):
        plt.subplot(2, 2, i)
        company['Daily Return'].hist(bins=50)
        plt.xlabel('Daily Return')
        plt.ylabel('Counts')
        plt.title(f'{company_name[i - 1]}')

    plt.tight_layout()
    plt.savefig("C:/Users/milja/PycharmProjects/flaskProject/stocks5.png")

    return 'stocks5.png'


def correlation():

    plt.figure(figsize=(12, 10), facecolor='white')

    plt.subplot(2, 2, 1)
    sns.heatmap(tech_rets.corr(), annot=True, cmap='summer')
    plt.title('Correlation of stock return')

    plt.subplot(2, 2, 2)
    sns.heatmap(closing_df.corr(), annot=True, cmap='summer')
    plt.title('Correlation of stock closing price')

    plt.savefig("C:/Users/milja/PycharmProjects/flaskProject/stocks6.png")

    return 'stocks6.png'


def risk():
    rets = tech_rets.dropna()

    area = np.pi * 20

    plt.figure(figsize=(10, 8), facecolor='white')
    plt.scatter(rets.mean(), rets.std(), s=area)
    plt.xlabel('Expected return')
    plt.ylabel('Risk')

    for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
        plt.annotate(label, xy=(x, y), xytext=(50, 50), textcoords='offset points', ha='right', va='bottom',
                 arrowprops=dict(arrowstyle='-', color='blue', connectionstyle='arc3,rad=-0.3'))

    plt.savefig("C:/Users/milja/PycharmProjects/flaskProject/stocks7.png")

    return 'stocks7.png'