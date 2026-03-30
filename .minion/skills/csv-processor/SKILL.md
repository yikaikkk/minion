---
name: csv-processor
description: Process CSV files by reading, transforming data based on user requirements, and saving to new CSV files. Use this skill whenever the user provides a CSV file path and wants to process or transform the data in any way, including filtering, sorting, calculating new columns, or any other data manipulation tasks.
---

# CSV Processor Skill

This skill handles CSV file processing tasks. It can read CSV files, perform various data transformations based on user requirements, and save the results to new CSV files.

## Workflow

When the user provides a CSV file path and requests data processing:

1. **Install Dependencies**: First, install the required Python packages (pandas, numpy)
2. **Read CSV**: Load the CSV file into a pandas DataFrame
3. **Process Data**: Apply the user's requested transformations
4. **Save Output**: Write the processed data to a new CSV file with the user-specified name

## Usage Instructions

### Step 1: Install Dependencies
Always install the required dependencies before processing:
```bash
pip install pandas numpy
```

### Step 2: Create Processing Script
Create a Python script that:
- Reads the input CSV file
- Applies the user's requested transformations
- Saves the output to the specified filename in the same directory

### Step 3: Execute the Script
Run the Python script to process the data.

## Supported Operations

This skill can handle various data processing operations including but not limited to:
- Filtering rows based on conditions
- Sorting data by columns
- Adding new calculated columns
- Removing or renaming columns
- Aggregating data
- Handling missing values
- Data type conversions
- String operations on text columns

## Input Requirements

The user must provide:
- **Input CSV file path**: Full path to the source CSV file
- **Processing instructions**: Clear description of what transformations to apply
- **Output filename**: Name for the new CSV file (will be saved in the same directory as input)

## Output Format

The processed data will be saved as a CSV file in the same directory as the input file, with the filename specified by the user.

## Example Usage

**User request**: "Process the CSV file at /path/to/data.csv by adding a new column that calculates the total price (quantity * unit_price) and save it as processed_data.csv"

**Skill execution**:
1. Install pandas and numpy
2. Create a Python script that reads data.csv, adds the total_price column, and saves as processed_data.csv
3. Execute the script

## Error Handling

If the CSV file doesn't exist or is malformed, report the error to the user. If the user's processing instructions are unclear, ask for clarification before proceeding.

## Python Script Template

Use this template for creating processing scripts:

```python
import pandas as pd
import sys
import os

def process_csv(input_path, output_path, operations):
    """
    Process CSV file according to specified operations
    """
    # Read the CSV file
    df = pd.read_csv(input_path)
    
    # Apply user-specified operations here
    # [OPERATIONS WILL BE INSERTED BASED ON USER REQUEST]
    
    # Save to output path
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Process the file
    process_csv(input_file, output_file, None)
```
