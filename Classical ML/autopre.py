import os 
import pandas as pd 

# Function to read data based on file extension
def read_data(file_path):
    _ , file_ext = os.path.splitext(file_path)
    if file_ext == '.csv':
        return pd.read_csv(file_path)
    elif file_ext == '.json':
        return pd.read_json(file_path)
    elif file_ext in ['.xls', '.xlsx']:
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unknown file format")
    

# Function to find outliers using IQR
def find_outliers_IQR(df):
    outlier_indices = []
    df = df.select_dtypes(include=['number'])
    for column in df.columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Get the indices of outliers for feature column
        outlier_list_col = df[(df[column] < lower_bound) | (df[column] > upper_bound)].index
        outlier_indices.extend(outlier_list_col)
    
    outlier_indices = list(set(outlier_indices))  # Get unique indices
    return outlier_indices

def check_missing_data(df:pd.DataFrame):
    porportion_null_rows = 100*round(df.isnull().sum(axis=0).sum()/df.shape[0],2)
    if porportion_null_rows <= 5:
        print(f"There are {porportion_null_rows}% rows with a null value. All of them are erased!")
        df = df.dropna()
    else:
        print("Too many null values, we need to check columns by columns further.")
        print(df.isnull().sum())
    return df
            

# Check if there are duplicates
def drop_duplicates(df, columns=None): 
    # first report if there are any duplicates
    print(f"Number of duplicates: {df.duplicated().sum()}")
    if columns is not None:
        df = df.drop_duplicates(subset=columns)
    else:
        df = df.drop_duplicates()
    return df
