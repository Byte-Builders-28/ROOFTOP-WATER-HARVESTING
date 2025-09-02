import pandas as pd

# Load the dataset once
df = pd.read_csv("data_engineering/data/rainfall.csv")

# Compute mean rainfall for each SUBDIVISION (1901–2015)
mean_rainfall = df.groupby("SUBDIVISION").mean(numeric_only=True).mean(axis=1)

# Store as dictionary {region: mean_rainfall}
mean_rainfall_dict = mean_rainfall.to_dict()

def get_mean_rainfall(region: str) -> float:
    """
    Return mean rainfall for a given region (SUBDIVISION).
    If region not found, returns None.
    """
    return mean_rainfall_dict.get(region.upper(), None)


# Example
# if __name__ == "__main__":
#     region = "BIHAR"
#     avg = get_mean_rainfall(region)
#     if avg is not None:
#         print(f"Mean rainfall in {region} (1901–2015): {avg:.2f}")
#     else:
#         print(f"Region '{region}' not found.")
