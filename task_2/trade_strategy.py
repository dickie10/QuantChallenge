import pandas as pd
import plotly.graph_objects as go

def trading_strategy(df, position_size=100):
    """
    Trading strategy between DA and Intraday prices considering renewable production levels (Wind & PV).
    """
    strategy_results = []
    
    for date, group in df.groupby(df.index.date):
        # Extract data for the specific date
        da_wind = group['Wind Day Ahead Forecast [in MW]']
        id_wind = group['Wind Intraday Forecast [in MW]']
        da_pv = group['PV Day Ahead Forecast [in MW]']
        id_pv = group['PV Intraday Forecast [in MW]']
        
        da_prices = group['Day Ahead Price hourly [in EUR/MWh]']
        id_prices = group['Intraday Price Hourly  [in EUR/MWh]']
        
        hours = group.index.hour
        
        # Calculate total renewable production (Wind + PV)
        da_total_renewable_prod = da_wind + da_pv  # DA forecasted production
        id_total_renewable_prod = id_wind + id_pv  # Intraday forecasted production
        
        # Define the trading condition:
        # Buy in DA when renewable production is high (and DA prices are low)
        # Sell in Intraday when renewable production is low (and Intraday prices are high)
        
        for hour in hours:
            # Trading Condition:
            buy_condition = (da_total_renewable_prod.iloc[hour] > da_total_renewable_prod.mean()) and \
                             (da_prices.iloc[hour] < da_prices.mean())  # Buy when DA forecast and price are favorable
            
            sell_condition = (id_total_renewable_prod.iloc[hour] < id_total_renewable_prod.mean()) and \
                             (id_prices.iloc[hour] > id_prices.mean())  # Sell when Intraday forecast and price are favorable
            
            if buy_condition:
                buy_price = da_prices.iloc[hour]
                sell_price = id_prices.iloc[hour]
                profit = (sell_price - buy_price) * position_size
                strategy_results.append({
                    "Date": date,
                    "Hour": hour,
                    "Buy Price (EUR/MWh)": buy_price,
                    "Sell Price (EUR/MWh)": sell_price,
                    "Profit (EUR)": profit,
                    "Trade": "Buy"
                })
            elif sell_condition:
                buy_price = da_prices.iloc[hour]
                sell_price = id_prices.iloc[hour]
                profit = (sell_price - buy_price) * position_size
                strategy_results.append({
                    "Date": date,
                    "Hour": hour,
                    "Buy Price (EUR/MWh)": buy_price,
                    "Sell Price (EUR/MWh)": sell_price,
                    "Profit (EUR)": profit,
                    "Trade": "Sell"
                })

    # Convert results to a DataFrame
    results_df = pd.DataFrame(strategy_results)
    
    # Calculate cumulative profit over time
    results_df["Cumulative Profit (EUR)"] = results_df["Profit (EUR)"].cumsum()

    return results_df

# Sample DataFrame (replace with your actual data) 
# Assuming the 'hourly_data.csv' contains a datetime column 'time' which is parsed as datetime and set as index

df = pd.read_csv("hourly_data.csv", parse_dates=["time"], index_col="time")

# Call the strategy function
results_df = trading_strategy(df)

# Display the results
print("Cumulative Profit Over Time:")
print(results_df)

# Plot Cumulative Profit

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=results_df["Date"],
    y=results_df["Cumulative Profit (EUR)"],
    mode='lines',
    name='Cumulative Profit',
    line=dict(color='green')
))

fig.update_layout(
    title="Cumulative Profit from Trading Strategy",
    xaxis_title="Date",
    yaxis_title="Cumulative Profit (EUR)",
    template="plotly_white"
)

fig.show()
