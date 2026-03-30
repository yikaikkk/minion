# CSV Processor Skill

This skill enables Claude to process CSV files by reading them, applying user-specified transformations, and saving the results to new CSV files.

## Features

- **Dependency Management**: Automatically installs required Python packages (pandas, numpy)
- **Flexible Processing**: Supports various data operations including:
  - Adding calculated columns
  - Filtering rows based on conditions
  - Sorting data
  - Selecting specific columns
  - Renaming columns
- **Error Handling**: Validates input files and provides clear error messages
- **Dynamic Operations**: Uses JSON configuration to specify processing operations

## Usage

When a user provides:
1. A CSV file path
2. Processing instructions
3. Output filename

The skill will:
1. Install dependencies if needed
2. Create and execute a Python script to process the data
3. Save the result to the specified output file

## File Structure

```
csv-processor/
├── SKILL.md                 # Main skill definition
├── README.md               # This documentation
├── scripts/
│   ├── process_csv.py      # Basic CSV processor
│   └── dynamic_csv_processor.py  # Advanced processor with JSON config
└── evals/
    └── evals.json          # Test cases
```

## Example Workflows

### Add Calculated Column
**User request**: "Add a total column (quantity * price) to /path/data.csv and save as processed.csv"

**Skill action**: 
- Installs pandas/numpy
- Creates script that reads data.csv, adds total column, saves as processed.csv

### Filter Data
**User request**: "Filter /path/sales.csv to only include North region and save as north_sales.csv"

**Skill action**:
- Uses dynamic processor with filter condition: `region == "North"`

### Sort and Select Columns
**User request**: "Sort /path/inventory.csv by product_name and keep only product_name and quantity columns, save as sorted_inventory.csv"

**Skill action**:
- Uses dynamic processor with sort and select_columns operations

## Dependencies

- Python 3.x
- pandas
- numpy

## Testing

The skill includes test cases in the `evals/` directory that verify core functionality.
