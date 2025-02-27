# -*- coding: utf-8 -*-
"""Truckload Weight Calculator (SQL)

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TmqNb3-7tms2_dYnY6GKZy5rw2lY1tG-
"""

import sqlite3

# Constants
CUBIC_INCHES_PER_FOOT = 1728

# Function to get a valid integer input
def get_valid_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

# Function to get a valid yes or no input
def get_yes_or_no(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ['yes', 'no']:
            return response
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def calculate_volume(length, width, height):
    return length * width * height

def calculate_weight(volume_ft, foam_factor):
    return volume_ft * foam_factor

def export_to_sqlite(truckload_details):
    conn = sqlite3.connect('truckload.db')
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS truckloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            truck_name TEXT,
            delivery_date TEXT,
            truckload_weight REAL
        )
    ''')

    # Insert truckload details into the table
    cursor.execute('''
        INSERT INTO truckloads (truck_name, delivery_date, truckload_weight)
        VALUES (?, ?, ?)
    ''', (truckload_details['Truck Name'], truckload_details['Delivery Date'], truckload_details['Truckload Weight']))

    conn.commit()
    conn.close()

def main():
    # Get truck and delivery details
    truck_name = input("Enter the name of the truck: ")
    delivery_date = input("Enter the date of the delivery (MM/DD/YYYY): ")

    # Get user input for foam types
    point_eight_yes_or_no = get_yes_or_no("1.8 foam (yes or no): ")
    two_five_yes_or_no = get_yes_or_no("2.5 foam (yes or no): ")

    # Initialize variables
    point_eight_bun_length = point_eight_bun_width = point_eight_bun_height = point_eight_bun_quantity = 0
    two_five_bun_length = two_five_bun_width = two_five_bun_height = two_five_bun_quantity = 0

    if point_eight_yes_or_no == "yes":
        point_eight_bun_length = get_valid_int("\nInput length of 1.8 bun (inches): ")
        point_eight_bun_width = get_valid_int("Input width of 1.8 bun (inches): ")
        point_eight_bun_height = get_valid_int("Input height of 1.8 bun (inches): ")
        point_eight_bun_quantity = get_valid_int("Input quantity of 1.8 bun: ")

    if two_five_yes_or_no == "yes":
        two_five_bun_length = get_valid_int("\nInput length of 2.5 bun (inches): ")
        two_five_bun_width = get_valid_int("Input width of 2.5 bun (inches): ")
        two_five_bun_height = get_valid_int("Input height of 2.5 bun (inches): ")
        two_five_bun_quantity = get_valid_int("Input quantity of 2.5 bun: ")

    # Calculate volume of bun in cubic inches
    point_eight_volume_in = calculate_volume(point_eight_bun_length, point_eight_bun_width, point_eight_bun_height)
    two_five_volume_in = calculate_volume(two_five_bun_length, two_five_bun_width, two_five_bun_height)

    # Calculate volume of bun in cubic feet
    point_eight_volume_ft = point_eight_volume_in / CUBIC_INCHES_PER_FOOT
    two_five_volume_ft = two_five_volume_in / CUBIC_INCHES_PER_FOOT

    # Calculate weight of bun
    point_eight_weight = calculate_weight(point_eight_volume_ft, 1.8)
    two_five_weight = calculate_weight(two_five_volume_ft, 2.5)

    # Calculate weight of buns
    point_eight_buns_weight = point_eight_weight * point_eight_bun_quantity
    two_five_buns_weight = two_five_weight * two_five_bun_quantity

    # Calculate truckload weight
    truckload_weight = point_eight_buns_weight + two_five_buns_weight

    # Store truckload details in a dictionary
    truckload_details = {
        "Truck Name": truck_name,
        "Delivery Date": delivery_date,
        "Truckload Weight": round(truckload_weight, 2)
    }

    # Display results
    print("\n**Truckload Details**")
    for key, value in truckload_details.items():
        print(f"{key}: {value}")

    # Export to SQLite database
    export_to_sqlite(truckload_details)
    print(f"\nTruckload details have been exported to SQLite database.")

if __name__ == "__main__":
    main()