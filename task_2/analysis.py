import pandas as pd 
import matplotlib.pyplot as plt

########### Task 2.1 ######### 

def forecasted_power(data):
    #converting the qurately hour data to hourly data 
    hourly_data = data.resample("h").sum()/4
    #returning the sum of the each product forecast (DA/Intraday) in hourly basis 
    return hourly_data.sum()   



########## Task 2.2  ###########  


def calculate_average(data, hour_column):
    # Group by the hour column and calculate the mean
    average_value = data.groupby(hour_column).mean()
    return average_value



def plot_power(data):

    # Calculate average Wind Power production for Intraday and Day Ahead basis
    average_wind_da = calculate_average(data['Wind Day Ahead Forecast [in MW]'], data['hour'])
    average_wind_id = calculate_average(data['Wind Intraday Forecast [in MW]'], data['hour'])

    # Calculate average PV Power production for Intraday and Day Ahead basis
    average_pv_da = calculate_average(data['PV Day Ahead Forecast [in MW]'], data['hour'])
    average_pv_id = calculate_average(data['PV Intraday Forecast [in MW]'], data['hour'])

    # Plot the results
    plt.figure(figsize=(12, 6))
    plt.plot(average_wind_da, label='Wind Day Ahead')
    plt.plot(average_wind_id, label='Wind Intraday')
    plt.plot(average_pv_da, label='PV Day Ahead')
    plt.plot(average_pv_id, label='PV Intraday')

    plt.xlabel('Hour of the Day')
    plt.ylabel('Average Power Production (MW)')
    plt.title('Average Wind/Solar Production for 2021 Over a 24h Period')
    plt.legend()
    plt.grid(True) 

    # Save the plot as an image file
    plt.savefig('average_wind_solar_production_2021.png')
    return average_pv_da, average_wind_da


############# Task 2.3 ############################# 


def cmp_pv_wind(df):

    df["Wind_DA_MWh"] = df["Wind Day Ahead Forecast [in MW]"] / 4
    df["PV_DA_MWh"] = df["PV Day Ahead Forecast [in MW]"] / 4

    df = df.reset_index()
    df_hourly = df.resample("H", on="time").sum()
    print(df_hourly) 
    df_hourly.to_csv("analysis.csv")
    #  Compute the weighted average value for Wind & Solar (PV)
    wind_avg_value = (df_hourly["Wind_DA_MWh"] * df_hourly["Day Ahead Price hourly [in EUR/MWh]"]).sum() / df_hourly["Wind_DA_MWh"].sum()
    pv_avg_value = (df_hourly["PV_DA_MWh"] * df_hourly["Day Ahead Price hourly [in EUR/MWh]"]).sum() / df_hourly["PV_DA_MWh"].sum()

    #  Compute the average DA price
    avg_da_price = df_hourly["Day Ahead Price hourly [in EUR/MWh]"].mean()

    #  Print results
    print(f"Average Value for Wind Power: {wind_avg_value:.2f} EUR/MWh")
    print(f"Average Value for Solar (PV) Power: {pv_avg_value:.2f} EUR/MWh")
    print(f"Average Day-Ahead Price: {avg_da_price:.2f} EUR/MWh")

    #Compare the average values with the DA price
    if wind_avg_value > avg_da_price:
        print("Wind power received a higher price than the average DA price.")
    else:
        print("Wind power received a lower price than the average DA price.")

    if pv_avg_value > avg_da_price:
        print("Solar (PV) power received a higher price than the average DA price.")
    else:
        print("Solar (PV) power received a lower price than the average DA price.") 

    """ 
    Conclusion: 
    # Wind & PV tend to generate more during low-price periods (e.g., night for wind, midday for solar).
    # Their high supply reduces market prices (Merit Order Effect), lowering their average value.
    # Wind/PV production often misses peak-price hours (morning & evening demand peaks).
    # As a result, the average value received by Wind/PV is typically lower than the average DA price.
    """ 

    print("\nAdditional Conclusion:")
    print("Wind & PV tend to generate more during low-price periods (e.g., night for wind, midday for solar).")
    print("Their high supply reduces market prices (Merit Order Effect), lowering their average value.")
    print("Wind/PV production often misses peak-price hours (morning & evening demand peaks).")
    print("As a result, the average value received by Wind/PV is typically lower than the average DA price.")


################ Task 2.4 #################################### 

def max_min_power(df): 

    
    # Convert MW (quarter-hourly) to MWh (hourly) by dividing by 4
    df["Wind Total (MWh)"] = df["Wind Day Ahead Forecast [in MW]"] / 4
    df["Solar Total (MWh)"] = df["PV Day Ahead Forecast [in MW]"] / 4

    # Calculate total renewable energy production per hour
    df["Total Renewable (MWh)"] = df["Wind Total (MWh)"] + df["Solar Total (MWh)"]

    # Aggregate daily totals
    daily_production = df.resample("D")["Total Renewable (MWh)"].sum()

    # Find the day with the highest and lowest renewable production
    highest_day = daily_production.idxmax()  # Day with max production
    lowest_day = daily_production.idxmin()   # Day with min production

    # Get average DA price for these days
    daily_prices = df.resample("D")["Day Ahead Price hourly [in EUR/MWh]"].mean()

    highest_day_price = daily_prices.loc[highest_day]
    lowest_day_price = daily_prices.loc[lowest_day]

    # Print results
    print(f"Highest Renewable Production Day: {highest_day.date()}, DA Price: {highest_day_price:.2f} EUR/MWh")
    print(f"Lowest Renewable Production Day: {lowest_day.date()}, DA Price: {lowest_day_price:.2f} EUR/MWh") 

    results_df = pd.DataFrame({
    "Date": [highest_day.date(), lowest_day.date()],
    "Total Renewable (MWh)": [daily_production.loc[highest_day], daily_production.loc[lowest_day]],
    "Avg DA Price (EUR/MWh)": [highest_day_price, lowest_day_price]
    })

    # Reset index for cleaner display
    results_df.set_index("Date", inplace=True)

    # Display the DataFrame
    print(results_df) 

    print("\nConclusion:")
    print("The average DA price is lower when renewable energy production (Wind/Solar) is high,")
    print("due to the merit-order effect. Renewables like PV and Wind have zero marginal costs,")
    print("meaning they can meet demand at lower prices.")
    print("When renewable generation is low, fossil fuel-based power generation is relied upon,")
    print("which has higher operating costs, driving the DA prices higher.")

########### Task 2.5 #############################
def demand_weekday_weekend(df): 

    # Ensure the 'time' index is in datetime format if it's not already
    df.index = pd.to_datetime(df.index)

    # Extract day of the week (0=Monday, 1=Tuesday, ..., 6=Sunday)
    df['day_of_week'] = df.index.weekday

    # Define weekdays and weekends
    weekdays = df[df['day_of_week'] < 5]  # Monday to Friday (weekdays)
    weekends = df[df['day_of_week'] >= 5]  # Saturday and Sunday (weekends)

    # Calculate the average DA price for weekdays and weekends
    avg_da_weekdays = weekdays['Day Ahead Price hourly [in EUR/MWh]'].mean()
    avg_da_weekends = weekends['Day Ahead Price hourly [in EUR/MWh]'].mean()

    # Print the results
    print(f"Average DA Price during Weekdays: {avg_da_weekdays:.2f} EUR/MWh")
    print(f"Average DA Price during Weekends: {avg_da_weekends:.2f} EUR/MWh")

    # Conclusion about the possible reason for price differences
    print("\nConclusion:")
    print("Average prices may differ between weekdays and weekends due to varying demand patterns.")
    print("1. On weekdays, demand tends to be higher due to industrial and commercial activity, resulting in higher prices.")
    print("2. On weekends, demand may be lower as industrial and commercial activities are reduced, leading to lower prices.")
    print("3. Additionally, renewable energy availability (such as solar power on weekends) may influence prices, but above points seems more reasonable answer.")

####### Task 2.6 ############################################## 

def calculate_battery_revenue(df): 

    """
    idea: to charge when the da is low and discharge when da is high  
    """  
    df = convert_hour(df)
    df['day'] = df.index.date 
    
    # Calculate the low price (charging hours) and high price (discharging hours)
    # Let's assume the battery is charged during the lowest 12-hour period (charging) and discharged during the highest 12-hour period (discharging)
   
    revenue_per_day = [] 

    # Loop through each day of the year
    for day,group in df.groupby('day'):
        # Sort prices for the day
        sorted_prices = group['Day Ahead Price hourly [in EUR/MWh]'].sort_values()

        # The 12 lowest prices will be used for charging (you can adjust if needed)
        charging_prices = sorted_prices.head(12)  # Charging during lowest 12 hours
        discharging_prices = sorted_prices.tail(12)  # Discharging during highest 12 hours

        # Revenue is the sum of charging during low price and discharging during high price
        revenue_day = discharging_prices.sum() - charging_prices.sum()
        revenue_per_day.append(revenue_day)

    # Total revenue for the year
    total_revenue = sum(revenue_per_day)

    return total_revenue, revenue_per_day 

########## Task 2.7 ############################

def convert_hour(df):
    # Resample the data from quarter-hourly (15 minutes) to hourly
    df_hourly = df.resample('H').sum()
    df_hourly.reset_index(inplace=True)
    df_hourly.to_csv('hourly_data.csv', index=False) 
    return df 

""""
in trading_strategy.py file and stratgy explained in trading_strategy.txt
"""






if __name__ == "__main__":
    df = pd.read_excel("analysis_task_data.xlsx",parse_dates=["time"],index_col="time") 
    
     
    # Calculate total Wind Power forecasted on Day Ahead basis
    total_wind_da = forecasted_power(df['Wind Day Ahead Forecast [in MW]']) 
    
    
    # Calculate total PV Power forecasted on Day Ahead basis
    total_pv_da = forecasted_power(df['PV Day Ahead Forecast [in MW]'])

    # Calculate total Wind Power forecasted on Intraday basis
    total_wind_id = forecasted_power(df['Wind Intraday Forecast [in MW]'])

    # Calculate total PV Power forecasted on Intraday basis
    total_pv_id = forecasted_power(df['PV Intraday Forecast [in MW]'])

    print(f"Total Wind Power forecasted on Day Ahead basis: {total_wind_da} MWh")
    print(f"Total PV Power forecasted on Day Ahead basis: {total_pv_da} MWh")
    print(f"Total Wind Power forecasted on Intraday basis: {total_wind_id} MWh")
    print(f"Total PV Power forecasted on Intraday basis: {total_pv_id} MWh") 
 
    
    avg_pv_da, avg_wind_da = plot_power(df) 

    cmp_pv_wind(df) 

    print("after plot")
     
    max_min_power(df)  

    demand_weekday_weekend(df) 
    
    # Calculate total revenue and daily revenues
    total_revenue, revenue_per_day = calculate_battery_revenue(df) 
    # Output the results 
    print(f"Total revenue for the year from the battery (1 MWh) charging and discharging: {total_revenue:.2f} EUR")
     
    
   
      
