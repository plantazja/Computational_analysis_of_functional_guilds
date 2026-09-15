import pandas as pd

def preprocess_data(filepath):
    df = pd.read_csv(filepath, sep='\t')
    df = df.T
    functions_name = df.iloc[0].tolist()
    df = df.drop(df.index[0])
    df.columns = functions_name
    return df

def filter_prevalence(df, threshold=0.1):
    """Filter functions/columns based on their prevalence in samples"""
    df_binary = (df > 0).astype(int)
    prevalence = df_binary.mean(axis=0)
    return df.loc[:, prevalence > threshold]

def normalize(df):
    """Normalize rows while handling zero-sum rows"""
    row_sums = df.sum(axis=1)
    return df.div(row_sums, axis=0)

def filter_samples(df, quantile_threshold=0.1):
    """Filter samples based on number of features present"""
    feature_counts = df.astype(bool).sum(axis=1)
    threshold = feature_counts.quantile(quantile_threshold)
    return df.loc[feature_counts > threshold]

def remove_empty(df):
    # Remove columns with all zeros OR all NA
    original_cols = df.shape[1]
    df = df.loc[:, (df != 0).any(axis=0) & (~df.isna().all(axis=0))]
    removed_cols = original_cols - df.shape[1]
    #print(f"Original features: {original_cols}")
    #print(f"Features (columns) removed (all zeros or all NA): {removed_cols}")
    #print(f"Remaining columns: {df.shape[1]}")

    # Remove rows with all zeros OR all NA
    original_rows = df.shape[0]
    df = df.loc[(df != 0).any(axis=1) & (~df.isna().all(axis=1))]
    removed_rows = original_rows - df.shape[0]
    #print(f"Original samples: {original_rows}")
    #print(f"Samples (rows) removed (all zeros or all NA): {removed_rows}")
    #print(f"Remaining samples: {df.shape[0]}")
    return df