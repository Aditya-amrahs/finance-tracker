from cProfile import label
from queue import PriorityQueue
from random import choice
from traceback import print_tb
from turtle import color
from warnings import warn_explicit
from xml.dom.pulldom import START_DOCUMENT
from eel import start
from matplotlib import category, figure
from numpy import true_divide
import pandas as pd
import csv
from datetime import date, datetime
from data_entry import get_amount, get_description, get_category, get_date
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "financial_records.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["date", "amount", "category", "description"])
            df.to_csv(cls.CSV_FILE, index=False)

    
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transaction(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)
        
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filter_df = df.loc[mask]

        if filter_df.empty:
            print("No transaction found in the given date range")
        else:
            print(f"Transaction from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(
                filter_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                    )
                )
            
            total_income = filter_df[filter_df["category"] == "Income"]["amount"].sum()
            total_expense = filter_df[filter_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: Rs {total_income:.2f}")
            print(f"Total Expense: Rs {total_expense:.2f}")
            print(f"Net Savings: Rs {(total_income - total_expense):.2f}")

        return filter_df

    @classmethod
    def get_fulltransaction(cls):
        try:
            df = pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            print("CSV not found!")
            return None

        if df.empty:
            print("No Transaction Found!")
        else:
            print("Transactions:")
            print(df.to_string(index=False))
            total_income = df[df["category"] == "Income"]["amount"].sum()
            total_expense = df[df["category"] == "Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: Rs {total_income:.2f}")
            print(f"Total Expense: Rs {total_expense:.2f}")
            print(f"Net Savings: Rs {(total_income - total_expense):.2f}")

        return df


def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyy) or enter for today's date: ", allow_default=True,)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transaction(df):
    df['date']= pd.to_datetime(df['date'], format='%d-%m-%Y')
    df.set_index("date", inplace=True)
    df.sort_index(ascending=True, inplace=True)  # Sort the dates in ascending order

    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(15,5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1. Add a New Transaction")
        print("2. View All Transactions and Summary")
        print("3. View Transaction and Summary within a Date-Range")
        print("4. Exit")
        choice = input("Enter your Choice (1-4): ")

        if choice == "1":
            add()
        elif choice == "2":
            df = CSV.get_fulltransaction()
            if input("Do you want to see the plot? (y/n) ").lower() == "y":
                plot_transaction(df)
        elif choice == "3":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date  = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transaction(start_date, end_date)
            if input("Do you want to see the plot? (y/n) ").lower() == "y":
                plot_transaction(df)
        elif choice == "4":
            print("\nExiting...\n")
            break
        else:
            print("Invalid Choice. Select from 1-4")

if __name__ == "__main__":
    main()