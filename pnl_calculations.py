from DB import load_data_as_dataframe  
import pandas as pd


########### Task 1.1 #################################
def compute_total_buy_volume(side_variable,df: pd.DataFrame) -> float:
    """
    Computes the total buy volume from a DataFrame.

    Parameters:
    df(pd.DataFrame): A DataFrame containing 'quantity' and 'side' column.

    Returns:
    float: The total sum of the 'buy_volume' column.
    """
    #Check if the DataFrame is empty 
    if df is None or df.empty:
        print('Warning: Dataframe is empty or None')
        return 0.0 
    else:
        #Filtering the buy side 
        df = df[df["side"] == side_variable] 
        #calculating the total of buy volume and returning as float 
        return float(df["quantity"].sum())

def compute_total_sell_volume(side_variable,df: pd.DataFrame) -> float:
    """
    Computes the total sell volume from a DataFrame.

    Parameters:
    df (pd.DataFrame): A DataFrame containing  'quantity' and 'side' column.

    Returns:
    float: The total sum of the 'sell_volume' column.
    """

    #Check if the DataFrame is empty 
    if df is None or df.empty:
        print('Warning: Dataframe is empty or None')
        return 0.0 
    else:
        #Filtering the sell side 
        df = df[df["side"] == side_variable]
        #calculating the total of buy volume and returning as float 
        return float(df["quantity"].sum())

################ Task 1.2 ###############################
def compute_pnl(strategy_id: str, df: pd.DataFrame) -> float:
    """
    Computes the Profit and Loss (PnL) for a given strategy ID.

    PnL is calculated as:
        - If selling: income = quantity * price (positive)
        - If buying: income = -quantity * price (negative)

    Parameters:
    strategy_id (str): The strategy ID to filter trades.
    df_ (pd.DataFrame): The DataFrame containing trade data.

    Returns:
    float: The total PnL for the strategy. Returns 0.0 if no trades match the strategy ID.
    """
    #Check if the DataFrame is empty 
    if df is None or df.empty:
        print('Warning: Dataframe is empty or None')
        return 0.0  


    # Filter trades for the given strategy_id
    strategy_df = df.loc[df["strategy"] == strategy_id].copy()  # Create a copy to avoid modifying the slice  

    if strategy_df.empty:
        return 0.0  
     
    # Compute PnL: Sell (+quantity * price), Buy (-quantity * price)
    strategy_df.loc[:, "income"] = strategy_df.apply(
        lambda row: row["quantity"] * row["price"] if row["side"] == "sell" 
                    else -row["quantity"] * row["price"], axis=1
    )


    # Sum up total PnL for the strategy
    total_pnl = strategy_df["income"].sum()

    return float(total_pnl)





if __name__ == "__main__": 

    df = load_data_as_dataframe()
    print('################ Task 1.1 #######################')
    buy_volume = compute_total_buy_volume('buy',df) 
    sell_volume = compute_total_sell_volume('sell',df) 
    print(f"Total buy volume:{buy_volume}") 
    print(f"Total sell volume:{sell_volume}") 

    print('################ Task 1.2 #######################')
    unique_strategies = df["strategy"].unique() #filtering all strategy in the dataframe
    for strategy in unique_strategies:
        # Calculate PnL for each strategy
        pnl = compute_pnl(strategy, df)
        print(f"Strategy {strategy}: PnL = {pnl}")
