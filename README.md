# Installation and Running the Tasks

## 1. Install Dependencies  
Install dependencies using the `requirements.txt` file:  
```bash
pip install -r requirements.txt
```

## 2. Running Task 1  
Run the script below in your terminal:  
```bash
cd task_1
python execute_task_1.py
```

This will execute:  
- **Task 1.1** (`pnl_calculations.py`): Calculate total buy/sell volume.  
- **Task 1.2** (`pnl_calculations.py`): Calculate Profit and Loss (PnL).  
- **Task 1.3** (`app.py`): Start the Flask API endpoint.  

## 2.1 Testing the API (Task 1.3)  
After running Task 1.3:  
1. The Flask server starts.  
2. Test the API endpoint (e.g., with `curl`, Postman, or a browser).  
3. Press `CTRL+C` to stop the server.  

### How to Access the API Endpoint:  
1. **The Flask server starts**:  
   ```bash
   python app.py
   ```

2. **Test the API**:  
   - Open browser and navigate to:  
     ```
     http://127.0.0.1:5000/pnl/<string:strategy_id>
     ```  

3. **Stop the Flask server**:  
   - Press `CTRL+C` in the terminal to stop the server.  

**Example API Test**:  
![Sample Image](ref.png)  
*FIG: Example of testing the API endpoint*   

## Running Task 2
Run the script below in your terminal:  
```bash
cd task_2
python execute_task_2.py
```

This will execute:  
- (`analysis.py`): Solves whole questions from 2.1 to 2.6.  
- (`trade_strategy.py`): Trading strategy question number 2.7. 

## Trading Conditions for 2.7

For each hour of the day, check whether the conditions meet the following, idea: More renewable day ahead forecast so less DA price and low renewable intraday forecast more the intraday price :

- **Buy Condition (Day Ahead market)**:  
  If the forecasted renewable production day ahead (Wind + PV) is above average for the day, and the Day Ahead price is below its average for the day, **buy the energy**.

- **Sell Condition (Intraday market)**:  
  If the forecasted renewable production intraday (Wind + PV) is below average for the day, and the Intraday price is above its average for the day, **sell the energy**.

  
