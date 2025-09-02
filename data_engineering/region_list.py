import pandas as pd

def get_distinct_subdivisions(csv_path: str) -> list[str]:
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Take first column (SUBDIVISION) and drop duplicates
    subdivisions = df.iloc[:, 0].dropna().unique().tolist()
    
    return subdivisions

# Example 
if __name__ == "__main__":
    unique_subdivisions = get_distinct_subdivisions("data_engineering/data/rainfall.csv")
    print(unique_subdivisions)
