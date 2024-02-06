import pandas as pd

def convert_to_integer(dataset, columns):
        for column in columns:
            dataset[column] = pd.to_numeric(dataset[column], errors='coerce', downcast='integer')
            dataset[column] = dataset[column].fillna(-1).astype(int)

def select_columns_and_save_csv(input_file_path, output_file_path, columns_to_select, columns_to_convert=''):

    # Read the CSV file into a DataFrame with explicit delimiter
    dataset = pd.read_csv(input_file_path, delimiter=',')

    # Remove leading and trailing whitespaces from column names
    dataset.columns = dataset.columns.str.strip()
 
    # Select columns
    dataset = dataset[columns_to_select]

    # Remove leading and trailing whitespaces from column names
    dataset.columns = dataset.columns.str.strip().str.replace(' ', '_').str.lower().str.replace('(', '').str.replace(')', '').str.replace('%', '')

    # Remove any whitespace in all the values of the column
    for col in dataset.columns:
        if dataset[col].dtype == object:
            dataset[col] = dataset[col].str.strip().str.replace(',', '.')
         
    convert_to_integer(dataset, columns_to_convert)

    # Save the new DataFrame to the same CSV file, overwriting the existing file
    dataset.to_csv(output_file_path, index=False)

# just save to the same
def select_2_columns_and_save_csv(input_fie_path_1, input_file_path_2, columns_to_select_1, columns_to_select_2, output_file_path_1, output_file_path_2):
    # Read the CSV file into a DataFrame with explicit delimiter
    dataset_1 = pd.read_csv(input_fie_path_1, delimiter=',')
    dataset_2 = pd.read_csv(input_file_path_2, delimiter=',')

    # Remove leading and trailing whitespaces from column names
    dataset_1.columns = dataset_1.columns.str.strip()
    dataset_2.columns = dataset_2.columns.str.strip()
 
    dataset_1 = dataset_1[columns_to_select_1]
    dataset_2 = dataset_2[columns_to_select_2]

    # Remove leading and trailing whitespaces from column names
    dataset_1.columns = dataset_1.columns.str.strip().str.replace(' ', '_').str.lower().str.replace('(', '').str.replace(')', '').str.replace('%', '')
    dataset_2.columns = dataset_2.columns.str.strip().str.replace(' ', '_').str.lower().str.replace('(', '').str.replace(')', '').str.replace('%', '')

    # Remove any whitespace in all the values of the column
    for col in dataset_1.columns:
        if dataset_1[col].dtype == object:
            dataset_1[col] = dataset_1[col].str.strip().str.replace(',', '.')
    for col in dataset_2.columns:
        if dataset_2[col].dtype == object:
            dataset_2[col] = dataset_2[col].str.strip().str.replace(',', '.')

    # Merge the two datasets, and save to the same CSV file, 
    # dataset = pd.concat([dataset_1, dataset_2], axis=1)
    # print(dataset)
    # dataset.to_csv(output_file_path, index=False)
    dataset_1.to_csv(output_file_path_1, index=False)
    dataset_2.to_csv(output_file_path_2, index=False)

