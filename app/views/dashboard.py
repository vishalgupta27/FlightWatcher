import requests
from mariadb._mariadb import connection

from app import app, cur, conn
from flask import Flask, redirect, url_for, render_template, request, flash, session
from datetime import datetime
import mariadb


@app.route('/get_data_from_api', methods=['GET'])
def get_data_from_api():
    apiKey = "TMzHyydbypbUz2XUtWPrQC7pnBdnst7n"
    apiUrl = "https://aeroapi.flightaware.com/aeroapi/"

    airport = 'KSFO'
    auth_header = {'x-apikey': apiKey}

    response = requests.get(apiUrl + f"airports/{airport}/flights", headers=auth_header)

    if response.status_code == 200:
        api_data = response.json()
        print(api_data,"dataAPI")  # Optionally print the API data
        # Assuming you have a function to extract relevant data from api_data
        data_list = extract_data_from_api(api_data)
        insert_or_update_data(data_list)  # Call insert_data() with the extracted data
        return redirect('dashboard_view')

    else:
        print("Error executing request")


def extract_data_from_api(api_data):
    data_list = []
    for arrival in api_data['arrivals']:
        flight_number = arrival['flight_number']
        airline = arrival['operator']
        scheduled_departure_time_str = arrival.get('scheduled_off', '')  # Use an empty string as default
        scheduled_arrival_time_str = arrival.get('scheduled_on', '')  # Use an empty string as default
        status = arrival['status']

        if scheduled_departure_time_str and scheduled_arrival_time_str:
            # Convert date strings to datetime objects and format them correctly
            scheduled_departure_time = datetime.strptime(scheduled_departure_time_str, '%Y-%m-%dT%H:%M:%SZ')
            scheduled_arrival_time = datetime.strptime(scheduled_arrival_time_str, '%Y-%m-%dT%H:%M:%SZ')

            data_list.append((flight_number, airline, scheduled_departure_time, scheduled_arrival_time, status))
        else:
            print(f"Skipping arrival with flight number '{flight_number}' due to missing date information.")

    return data_list


@app.route('/dashboard_view')
def dashboard():
    return render_template('dashboard.html')


@app.route('/watchlist')
def watchListView():
    return render_template("watchlist.html")


@app.route('/graphical-analysis')
def graphicalAnalysisView():
    return render_template("graphical-analysis.html")


def clear_table():
    try:
        # SQL query to delete all data from the table
        sql = "DELETE FROM flightdetails"

        # Execute the query to clear the table
        cur.execute(sql)

        # Commit the changes
        conn.commit()

    except Exception as e:
        # Rollback changes in case of an error
        conn.rollback()
        print("Error occurred while clearing the table:", str(e))


# def insert_data(data_list):
#     # SQL query to insert data into the database
#     sql = ("INSERT INTO flightdetails (flightName, airlineName, arrivalTime, departureTime, status) "
#            "VALUES (%s, %s, %s, %s, %s)")
#
#     try:
#         for data in data_list:
#             cur.execute(sql, data)
#             conn.commit()
#             print("Data inserted successfully! The number of rows affected is:", cur.rowcount)
#
#     except Exception as e:
#         print("Error occurred while inserting data:", str(e))


# Call the function to insert data in the database
# insert_data()




@app.route('/check-flight')
def checkFlightView():
    if not session.get('logged_in'):
        # User is not logged in, redirect to the login page
        return redirect(url_for('login'))

    try:
        # Get the 'page' and 'search' query parameters from the URL
        page = request.args.get('page', default=1, type=int)
        search_query = request.args.get('search', default='', type=str)

        # Define the number of flights to display per page
        flights_per_page = 10

        # Calculate the offset based on the current page number
        offset = (page - 1) * flights_per_page

        # SQL query to fetch data from the database with pagination and search filter
        sql = f"SELECT flightName, airlineName, arrivalTime, departureTime, status, futurePrediction, isWatchlist " \
              f"FROM flightdetails WHERE airlineName LIKE '%{search_query}%' " \
              f"LIMIT {flights_per_page} OFFSET {offset}"
        print("SQL Query:", sql)

        # Execute the query to fetch the current page of flight data
        cur.execute(sql)
        flights_data = cur.fetchall()
        print("Fetched Data:", flights_data)

        # SQL query to get the total number of flights with the search filter applied
        count_sql = f"SELECT COUNT(*) FROM flightdetails WHERE airlineName LIKE '%{search_query}%'"
        cur.execute(count_sql)
        total_flights = cur.fetchone()[0]

        # Calculate the total number of pages
        total_pages = (total_flights + flights_per_page - 1) // flights_per_page

        # Define the number of pagination links to display
        max_pagination_links = 3

        # Calculate the start and end page numbers for the pagination links
        start_page = max(1, page - max_pagination_links // 2)
        end_page = min(total_pages, start_page + max_pagination_links - 1)

        return render_template('check-flight.html', flights=flights_data, current_page=page,
                               total_pages=total_pages, start_page=start_page, end_page=end_page,
                               search_query=search_query)

    except Exception as e:
        print("Error occurred while fetching data:", str(e))
        return "An error occurred while fetching data."


def update_data():
    try:
        # SQL query to update data in the database
        sql = "UPDATE flightdetails SET airlineName = %s, status = %s, futurePrediction = %s WHERE flightName = %s"

        # New data to be updated
        new_airline_name = 'AirAsia'
        new_status = 'Delayed'
        new_prediction = 'WithDelay'
        flight_name_to_update = 'Flight1'

        # Execute the update query with the new values
        cur.execute(sql, (new_airline_name, new_status, new_prediction, flight_name_to_update))

        # Commit the changes after updating the data
        conn.commit()

        print("Data updated successfully! The number of rows affected is:", cur.rowcount)

    except Exception as e:
        # Rollback changes in case of an error
        conn.rollback()
        print("Error occurred while updating data:", str(e))


# Call the function to update data in the database
# update_data()


def remove_duplicates():
    try:
        # SQL query to remove duplicate data from the database based on selected columns
        sql = "DELETE t1 FROM flightdetails t1 INNER JOIN flightdetails t2 " \
              "WHERE t1.id < t2.id AND t1.flightName = t2.flightName AND t1.airlineName = t2.airlineName"

        # Execute the DELETE query to remove duplicates
        cur.execute(sql)

        # Commit the changes after removing duplicates
        conn.commit()

        print("Duplicate data removed successfully! The number of duplicate rows removed is:", cur.rowcount)

    except Exception as e:
        # Rollback changes in case of an error
        conn.rollback()
        print("Error occurred while removing duplicate data:", str(e))


# Call the function to remove duplicate data from the database
# remove_duplicates()


def delete_data():
    try:
        # SQL query to delete data from the database based on specific conditions
        sql = "DELETE FROM flightdetails WHERE airlineName = %s AND status = %s"

        # Data to identify the rows to be deleted
        airline_to_delete = 'Indigo3'
        status_to_delete = 'OnTime'

        # Execute the DELETE query with the conditions
        cur.execute(sql, (airline_to_delete, status_to_delete))

        # Commit the changes after deleting data
        conn.commit()

        print("Data deleted successfully! The number of rows affected is:", cur.rowcount)

    except Exception as e:
        # Rollback changes in case of an error
        conn.rollback()
        print("Error occurred while deleting data:", str(e))


# # Call the function to delete data from the database
# delete_data()


def insert_or_update_data(data_list):
    try:
        for data in data_list:
            flight_number = data[0]

            # SQL query to check if data already exists
            select_sql = "SELECT flightName FROM flightdetails WHERE flightName = %s"

            # Execute the SELECT query with the flightName
            cur.execute(select_sql, (flight_number,))

            # Fetch one row, if any, to check if data exists
            existing_data = cur.fetchone()

            if existing_data is None:
                # Data does not exist, insert data into the database
                insert_sql = ("INSERT INTO flightdetails (flightName, airlineName, arrivalTime, departureTime, status) "
                              "VALUES (%s, %s, %s, %s, %s)")
                # Execute the INSERT query with the data
                cur.execute(insert_sql, data[:5])

                # Commit the changes after inserting data
                conn.commit()

                print("Data inserted successfully! The number of rows affected is:", cur.rowcount)
            else:
                # Data already exists, update data in the database
                update_sql = ("UPDATE flightdetails SET airlineName = %s, arrivalTime = %s, departureTime = %s, status = %s "
                              "WHERE flightName = %s")

                # Append the flightName to the data tuple for the UPDATE query
                data_for_update = data[1:5] + (flight_number,)

                # Execute the UPDATE query with the updated data
                cur.execute(update_sql, data_for_update)

                # Commit the changes after updating data
                conn.commit()

                print("Data updated successfully! The number of rows affected is:", cur.rowcount)

    except Exception as e:
        # Rollback changes in case of an error
        conn.rollback()
        print("Error occurred while inserting or updating data:", str(e))


from flask import request, redirect, url_for

@app.route('/add_all_to_watchlist', methods=['POST'])
def add_all_to_watchlist():
    try:
        # Retrieve all the flight data from the check-flight list
        all_flights = request.form.getlist('flight_checkbox')

        if not all_flights:
            # No flights selected, redirect back to check-flight page
            return redirect(url_for('check-flight'))

        # Loop through the list of flight IDs and update their isWatchlist status to True
        for flight_id in all_flights:
            # Assuming flight_id is the primary key of the flight in the database
            update_sql = "UPDATE flightdetails SET isWatchlist = %s WHERE flight_id = %s"

            # Execute the UPDATE query with isWatchlist set to True and the flight_id
            cur.execute(update_sql, (True, flight_id))

            # Commit the changes after updating data
            conn.commit()

        print("All selected flights added to the watchlist successfully!")
        return render_template("watchlist.html")  # Redirect back to check-flight page after the update

    except Exception as e:
        # Rollback changes in case of an error
        conn.rollback()
        print("Error occurred while adding flights to the watchlist:", str(e))
        return "Error occurred while adding flights to the watchlist."

