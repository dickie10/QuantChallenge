import pandas as pd 
import matplotlib.pyplot as plt

########### Task 2.1 ######### 

def forecasted_power(data):
    #converting the qurately hour data to hourly data
    hourly_data = data.resample("h").sum() / 4
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


def cmp_pv_wind(avg_pv_da,avg_wind_da,data):

    #as the price is repeated 4 times for qurtely hourly need to avg for each hour for hourly
    avg_da_price = calculate_average(data['Day Ahead Price hourly [in EUR/MWh]'], data['hour']) 
    avg_wind_value = avg_wind_da * avg_da_price 
    avg_pv_value = avg_pv_da * avg_da_price 
    print(avg_da_price) 
    print(avg_wind_value) 
    print(avg_wind_da)

    if avg_wind_value > avg_da_price:
        print("The average value of Wind is higher than the average DA price.")
    else:
        print("The average value of Wind is lower than the average DA price.")

    if avg_pv_value > avg_da_price:
        print("The average value of PV is higher than the average DA price.")
    else:
        print("The average value of PV is lower than the average DA price.")








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

    cmp_pv_wind(avg_pv_da, avg_wind_da,df) 

    print("after plot")