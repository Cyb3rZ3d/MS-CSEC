#Ruben_Valdez_CSEC5311_SP25_Assignment_2_Q2.py
import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    return pd.read_csv(file_path)

def clean_data(df):
    drop_cols = ["UID", "iso2", "iso3", "code3", "FIPS", "Admin2", "Country_Region", "Lat", "Long_", "Combined_Key"]
    return df.drop(columns=drop_cols)

def aggregate_data(df):
    return df.groupby("Province_State").sum().reset_index()

def reshape_data(df):
    df_melted = df.melt(id_vars=["Province_State"], var_name="Date", value_name="Cases")
    df_melted.rename(columns={"Province_State": "State"}, inplace=True)
    df_melted["Date"] = pd.to_datetime(df_melted["Date"], format="%m/%d/%y", errors='coerce')
    return df_melted

def sum_cases(df, start_date, end_date):
    df_filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    df_summed = df_filtered.groupby("State")["Cases"].sum().reset_index()
    df_summed.insert(1, "Start Date", start_date)
    df_summed.insert(2, "End Date", end_date)
    return df_summed

def plot_top_states(df):
    top_states = df.groupby("State")["Cases"].sum().nlargest(5).index
    df_top = df[df["State"].isin(top_states)]
    
    plt.figure(figsize=(12, 6))
    for state in top_states:
        state_data = df_top[df_top["State"] == state]
        plt.plot(state_data["Date"], state_data["Cases"], label=state)
    
    plt.title("Cumulative COVID-19 Cases Over Time for Top 5 States")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Cases")
    plt.legend(title="States")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()
    
    top_states_df = df.groupby("State")["Cases"].sum().nlargest(5).reset_index()
    print("\nTop 5 States with COVID-19 Cases:\n")
    print(top_states_df.to_string(index=False))

def main():
    data_path = "5. Fall 2025 (5th Semester)/CSEC 5311 _ Big Data Analysis and Security/Assignments/Assignment 2/time_series_covid19_confirmed_US.csv"
    df = load_data(data_path)
    df = clean_data(df)
    df = aggregate_data(df)
    df = reshape_data(df)
    
    start_date = "2020-01-22"
    end_date = "2023-03-09"
    df_final = sum_cases(df, start_date, end_date)
    
    print(df_final.head(10))
    
    plot_top_states(df)
    print(f"\n End of Program.\n")
    
if __name__ == "__main__":
    main()
