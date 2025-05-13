import pandas as pd
from sqlalchemy import create_engine


db_user = "postgres"
db_password = "07012025"
db_host = "localhost"
db_name = "credit_card_db"


engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}")
 

csv_files = {
    "cc_detail": r"C:\Users\New-user\Documents\Data Analysis PowerBI\credit_card.csv",
    "cust_detail": r"C:\Users\New-user\Documents\Data Analysis PowerBI\customer.csv"
}


def read_csv_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {e}")
        return None

def load_to_table(df, table_name):
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Data loaded into {table_name}")

if __name__ == "__main__":
    for table_name, file_path in csv_files.items():
        df = read_csv_data(file_path)

        if df is not None:
            load_to_table(df, table_name)

