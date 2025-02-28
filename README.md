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
1. **Start the Flask server**:  
   ```bash
   python app.py
   ```

2. **Test the API**:  
   - Use `curl` to test the endpoint:  
     ```bash
     curl http://127.0.0.1:5000/your-endpoint
     ```  
   - Open your browser and navigate to:  
     ```
     http://127.0.0.1:5000/your-endpoint
     ```  

3. **Stop the Flask server**:  
   - Press `CTRL+C` in the terminal to stop the server.  

**Example API Test**:  
![Sample Image](ref.png)  
*FIG: Example of testing the API endpoint*  