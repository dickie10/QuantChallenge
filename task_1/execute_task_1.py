import os
import subprocess

# Path to the tasks folder
tasks_folder = '.'

# Manually specify the order of the Python files
task_order = [
    'pnl_calculations.py',   # First task to run
    'app.py',   # Second task to run
    
]

# Run each Python file in the specified order
for file in task_order:
    # Generate the full path to the script
    file_path = os.path.join(tasks_folder, file)
    
    # Check if the file exists in the folder
    if os.path.exists(file_path):
        print(f"Running {file}...")
        subprocess.run(['python', file_path], check=True)  # 'check=True' ensures an error stops the script
    else:
        print(f"Error: {file} not found in the {tasks_folder} directory.")

print("All tasks completed!")
