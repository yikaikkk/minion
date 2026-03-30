#!/usr/bin/env python3
"""
Dynamic CSV Processor
This script can handle various CSV processing operations based on command line arguments.
"""

import pandas as pd
import sys
import os
import argparse
import ast

def apply_operations(df, operations_config):
    """
    Apply various operations to the DataFrame based on the configuration.
    
    operations_config should be a dictionary with operation types as keys:
    - 'add_column': {'name': 'new_col', 'formula': 'col1 * col2'}
    - 'filter': {'condition': 'column == value'}
    - 'sort': {'columns': ['col1', 'col2'], 'ascending': True}
    - 'select_columns': ['col1', 'col2']
    - 'rename_columns': {'old_name': 'new_name'}
    """
    
    # Apply column selection first (if specified)
    if 'select_columns' in operations_config:
        df = df[operations_config['select_columns']]
    
    # Rename columns
    if 'rename_columns' in operations_config:
        df = df.rename(columns=operations_config['rename_columns'])
    
    # Add new columns
    if 'add_column' in operations_config:
        add_ops = operations_config['add_column']
        if isinstance(add_ops, list):
            for op in add_ops:
                col_name = op['name']
                formula = op['formula']
                # Safe evaluation of formula using existing columns
                df[col_name] = df.eval(formula)
        else:
            col_name = add_ops['name']
            formula = add_ops['formula']
            df[col_name] = df.eval(formula)
    
    # Filter rows
    if 'filter' in operations_config:
        condition = operations_config['filter']['condition']
        df = df.query(condition)
    
    # Sort data
    if 'sort' in operations_config:
        sort_config = operations_config['sort']
        df = df.sort_values(
            by=sort_config['columns'],
            ascending=sort_config.get('ascending', True)
        )
    
    return df

def main():
    parser = argparse.ArgumentParser(description='Dynamic CSV Processor')
    parser.add_argument('input_file', help='Path to input CSV file')
    parser.add_argument('output_file', help='Path to output CSV file')
    parser.add_argument('--operations', help='Operations configuration as JSON string', default='{}')
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"Error: Input file {args.input_file} does not exist")
        sys.exit(1)
    
    try:
        # Read CSV
        df = pd.read_csv(args.input_file)
        print(f"Loaded {len(df)} rows from {args.input_file}")
        
        # Parse operations
        operations = {}
        if args.operations.strip():
            import json
            try:
                operations = json.loads(args.operations)
            except json.JSONDecodeError as e:
                print(f"Warning: Invalid JSON operations: {e}. Proceeding without operations.")
        
        # Apply operations
        if operations:
            df = apply_operations(df, operations)
            print(f"Applied operations. Result has {len(df)} rows")
        
        # Save output
        df.to_csv(args.output_file, index=False)
        print(f"Saved processed data to {args.output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
