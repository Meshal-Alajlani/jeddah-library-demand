from pathlib import Path
from data_processing import clean_data


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT_DIR / "data" / "raw" / "jeddah_library_rentals.csv"
OUTPUT_PATH = ROOT_DIR / "data" / "processed" / "cleaned_library_rentals.csv"


def main():
    df = clean_data(RAW_PATH)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Cleaned data saved to: {OUTPUT_PATH}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")


if __name__ == "__main__":
    main()
