import pandas as pd

def clean_and_transform_data(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    missing_values = df.isnull().sum()
    print("Missing values per column:")
    print(missing_values)

    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    df = df[df['quantity_sold'] > 0]  
    df = df[df['revenue'] > 0] 

    duplicate_columns = [col for col in df.columns if col not in ['order_id', 'store_id']]
    df = df.drop_duplicates(subset=duplicate_columns)

    df = df.reset_index(drop=True)
    df['store_id'] = df.index + 1  
    df['order_id'] = range(1, len(df) + 1)  

    df['revenue_per_unit'] = df['revenue'] / df['quantity_sold']

    
    df['month'] = df['date'].dt.strftime('%B')
    df['year'] = df['date'].dt.year
    
    df['day_of_year'] = df['date'].dt.dayofyear
    df['week'] = ((df['day_of_year'] - 1) // 7) + 1

    def categorize_revenue(revenue):
        if 1000 <= revenue <= 10000:
            return 'low'
        elif 10100 <= revenue <= 50000:
            return 'medium'
        elif revenue > 50100:
            return 'high'
        else:
            return 'unknown'

    df['revenue_group'] = df['revenue'].apply(categorize_revenue)

    df.to_csv(output_csv, index=False)
    print(f"Cleaned and transformed dataset saved to {output_csv}")

clean_and_transform_data(r'C:\Users\New-user\Downloads\Bumpa Stores analysis\Dataset_bumpa.csv', r'C:\Users\New-user\Downloads\Bumpa Stores analysis\Cleaned_dataset_bumpa.csv')
