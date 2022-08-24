import numpy as np
import pandas as pd
def missing_percent(df):

    '''
        how many missing values exist or better still what is the % of missing values in the dataset?
    
        args:
            df: DataFrame - the data frame
    '''
        
    # Calculate total number of cells in dataframe
    totalCells = np.product(df.shape)

    # Count number of missing values per column
    missingCount = df.isnull().sum()

    # Calculate total number of missing values
    totalMissing = missingCount.sum()

    # Calculate percentage of missing values
    print("The dataset contains", round(((totalMissing/totalCells) * 100), 2), "%", "missing values.")
    
def fill_using_median(df, cols):

    '''
        this function fill a missing data using median
    
        args:
            df: DataFrame - the data frame
            
            cols: list - contains a list of column name to be filled
            
        return:

            returns the filled Dataframe  
    '''
        
    for name in cols:
        df.loc[pd.isnull(df[name]), [name]] = df[name].quantile(0.75) - df[name].quantile(0.25)
        
    return df

def fill_using_mode(df, cols):

    '''
        this function fill a missing data using mode
    
        args:
            df: DataFrame - the data frame
            
            cols: list - contains a list of column name to be filled
            
        return:

            returns the filled Dataframe  
    '''
        
    for name in cols:
        df[name].fillna(value=df[name].mode().iloc[0], inplace=True)
        
    return df
