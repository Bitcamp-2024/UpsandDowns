import requests
from datetime import date
import sys
import pandas as pd
from prophet import Prophet

arguements = sys.argv
symbol = arguements[1]


from_date = "2010-01-01"
to_date = date.today()
url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={from_date}&to={to_date}&apikey=rvZ1Ul1zJ6tSpIgaIAPLl82TadAQskXP"
def fetch_data(url):
    response = requests.get(url).json()
    return response
data = fetch_data(url)


def preprocess_data(data):
    df = pd.DataFrame(data["historical"])
    df.reset_index(inplace=True)
    df.rename(columns={'date': 'ds', 'adjClose': 'y'}, inplace=True)
    return df


def train_prophet_model(data):
    model = Prophet(
        changepoint_prior_scale=0.05,
        holidays_prior_scale=15,
        seasonality_prior_scale=10,
        weekly_seasonality=True,
        yearly_seasonality=True,
        daily_seasonality=False
    )
    data.reset_index(inplace=True)
    data.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)
    model.add_country_holidays(country_name='US')
    model.fit(data)
    return model

def generate_forecast(model, periods=365):
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast

def plot_forecast(model, forecast):
    model.plot(forecast)

df = preprocess_data(data)

m = train_prophet_model(df)

f = generate_forecast(m)
export = f[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(365) # 365 days forecast
print(export.tail)
# plot_forecast(m, f)
