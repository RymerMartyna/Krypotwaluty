import pandas as pd
from prophet import Prophet

# df = pd.read_csv('fake_data.csv',sep=";")

historical_data = select_historical_prices_from_db("bitcoin")
df = pd.DataFrame(historical_data, columns=["date_of_price", "price"])

# Creating forecast
pr = Prophet()
pr.fit(df)
future = pr.make_future_dataframe(periods=365)
forecast = pr.predict(future)
print(
    forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail()
)  # Checking the outcome

# Clearing the records in predicitions table, not to have duplicate values
clear_predicitions_db()

# Adding rows to predictions table
for index, row in forecast.iterrows():
    write_price_to_forecast_db("bitcoin", row["yhat"], row["ds"])
