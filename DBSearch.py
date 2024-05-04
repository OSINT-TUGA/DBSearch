#!/usr/bin/env python3

import sqlite3
import os
import json
import sys
import signal
from tabulate import tabulate

# Store the last search terms for reuse within the session.
last_search_terms = []

# Load and return the configuration from a JSON file.
def load_config():
    with open('db_config.json', 'r') as file:
        return json.load(file)

# Ensure all databases listed in the configuration exist and retrieve row counts.
def verify_databases_exist(config):
    for db in config['databases']:
        if not os.path.exists(db['path']):
            print(f"Error: Database file {db['path']} not found.")
            sys.exit(1)
        else:
				
            conn = sqlite3.connect(db['path'])
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {db['table_name']}")
            row_count = cursor.fetchone()[0]
            db['row_count'] = f"{row_count:,}"  # format the number with commas
            cursor.close()
            conn.close()

#Clear the console screen to ensure a clean display of information.
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def search_client(db_path, table_name, search_fields, search_results_fields, field_conversions):
    global last_search_terms
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    while True:
        clear_screen()
        if not last_search_terms:
            print("Enter search terms or type 'exit' to return:")
            search_term = input("Search term: ")
            if search_term.lower() == 'exit':
                cursor.close()
                conn.close()
                return

            terms = [term.strip() for term in search_term.split() if len(term.strip()) >= 4]
            if not terms:
                print("Each term must have at least 4 characters.")
                input("Press Enter to continue...")
                continue

            last_search_terms = terms
        else:
            print(f"Searching for: {' '.join(last_search_terms)}")

        query = f"SELECT rowid, {', '.join(search_results_fields)} FROM {table_name} WHERE " + \
                " AND ".join(f"({' OR '.join(f'{field} LIKE ?' for field in search_fields)})" for _ in terms)
        params = [f'%{term}%' for term in last_search_terms for _ in search_fields]

        cursor.execute(query, params)
        results = cursor.fetchall()

        if results:
            headers = ["#"] + [col.title().replace('_', ' ') for col in search_results_fields]
            table = [[idx] + list(row[1:]) for idx, row in enumerate(results, 1)]
            print(tabulate(table, headers=headers, tablefmt='psql'))

            choice = input("Choose a result to view or 0 to return: ")
            if choice == '0':
                last_search_terms = []
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(results):
                selected_row = results[int(choice) - 1]
                clear_screen()
                print("Result details:")
                cursor.execute(f"SELECT * FROM {table_name} WHERE rowid=?", (selected_row[0],))
                row = cursor.fetchone()
                if row:
                    details = [[cursor.description[i][0].title().replace('_', ' '), value] for i, value in enumerate(row)]
                    print(tabulate(details, tablefmt='grid'))
                    input("Press Enter to return...")
                else:
                    print("No details available.")
                    input("Press Enter to return...")
        else:
            print("No results found.")
            last_search_terms = []
            input("Press Enter to return to search...")
				 

    cursor.close()
    conn.close()

# Display the main menu in tabular format and handle user interactions for database selection.
def main_menu(config):
    while True:
																										  
        clear_screen()
        print("Select the database or type '0' to exit:")
        menu_data = [
            [idx + 1, db['source'], db['desc'], db['row_count']]
            for idx, db in enumerate(config['databases'])
        ]
        headers = ["ID", "Source", "Description", "Rows"]
        print(tabulate(menu_data, headers=headers, tablefmt='psql'))
        print("0. Exit")

        choice = input("Choose an option: ")
        if choice == '0':
            sys.exit("Program closed.")
        elif choice.isdigit() and 1 <= int(choice) <= len(config['databases']):
            db_index = int(choice) - 1
            db_choice = config['databases'][db_index]
            search_client(db_choice['path'], db_choice['table_name'], db_choice['search_fields'], db_choice['search_results_fields'], db_choice.get('field_conversions', {}))

# Handle exit upon receiving the SIGINT signal.
def signal_handler(sig, frame):
    sys.exit("Exiting...")

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    config = load_config()
    verify_databases_exist(config)
    main_menu(config)
