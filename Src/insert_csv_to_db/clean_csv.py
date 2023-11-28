import pandas as pd

def select_columns_and_save_csv(input_file_path, output_file_path, columns_to_select):
    # Read the CSV file into a DataFrame with explicit delimiter
    dataset = pd.read_csv(input_file_path, delimiter=',')

    # Remove leading and trailing whitespaces from column names
    dataset.columns = dataset.columns.str.strip()

    # Select columns
    dataset = dataset[columns_to_select]

    # Remove leading and trailing whitespaces from column names
    dataset.columns = dataset.columns.str.strip()
    dataset.columns = dataset.columns.str.replace(' ', '_')
    dataset.columns = dataset.columns.str.lower()
    dataset.columns = dataset.columns.str.replace('(', '')
    dataset.columns = dataset.columns.str.replace(')', '')
    dataset.columns = dataset.columns.str.replace('%', '')

    # Remove any whitespace in all the values of the column
    #for loop through all the columns
    for col in dataset.columns:
        #check if the column is a string
        if dataset[col].dtype == object:
            #if it is a string, remove all the whitespace
            dataset[col] = dataset[col].str.strip()
            dataset[col] = dataset[col].str.replace(',', '.')

    # Save the new DataFrame to the same CSV file, overwriting the existing file
    dataset.to_csv(output_file_path, index=False)