import requests

from app import app, cur, conn
from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify
from datetime import datetime
import mariadb

from config import config


@app.route('/get_data_from_api', methods=['GET'])
def get_data_from_api():
    apiKey = "HORQ0GSNlyxzjfB9j1wjakVGlJTeBA0q"
    apiUrl = "https://aeroapi.flightaware.com/aeroapi/"

    airport = 'KSFO'
    auth_header = {'x-apikey': apiKey}

    response = requests.get(apiUrl + f"airports/{airport}/flights", headers=auth_header)

    if response.status_code == 200:
        api_data = response.json()
        print(api_data, "dataAPI")  # Optionally print the API data
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


@app.route('/dashboard_view', methods=['GET'])
def dashboard():
    if not session.get('logged_in'):
        # Return an error response if the user is not logged in
        return redirect(url_for('login'))

    try:
        get_data_from_api()
        # Establish the database connection
        conn = get_db_connection()

        # Use a context manager to create a cursor and automatically close it
        with conn.cursor() as cur:
            # SQL query to get the total number of flights
            count_flights_sql = "SELECT COUNT(*) FROM flightdetails"
            cur.execute(count_flights_sql)
            total_flights = cur.fetchone()[0]

            # SQL query to get the total number of airlines
            count_airlines_sql = "SELECT COUNT(DISTINCT airlineName) FROM flightdetails"
            cur.execute(count_airlines_sql)
            total_airlines = cur.fetchone()[0]

        # Close the database connection
        conn.close()

        return render_template('dashboard.html', total_flights=total_flights, total_airlines=total_airlines)

    except Exception as e:
        print("Error occurred while fetching data:", str(e))
        return "An error occurred while fetching data."



@app.route('/graphical-analysis')
def graphicalAnalysisView():
    return render_template("graphical-analysis.html")


def delete_table():
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


def get_db_connection():
    return mariadb.connect(**config)


# @app.route('/check-flight')
# def checkFlightView():
#     if not session.get('logged_in'):
#         # User is not logged in, redirect to the login page
#         return redirect(url_for('login'))
#
#     try:
#         # Get the 'page' and 'search' query parameters from the URL
#         page = request.args.get('page', default=1, type=int)
#         search_query = request.args.get('search', default='', type=str)
#
#         # Define the number of flights to display per page
#         flights_per_page = 10
#
#         # Calculate the offset based on the current page number
#         offset = (page - 1) * flights_per_page
#
#         # Establish the database connection
#         conn = get_db_connection()
#
#         # Use a context manager to create a cursor and automatically close it
#         with conn.cursor() as cur:
#             # SQL query to fetch data from the database with pagination and search filter
#             sql = f"SELECT id, flightName, airlineName, arrivalTime, departureTime, status, futurePrediction " \
#                   f"FROM flightdetails"
#
#             # Apply search filter if a search_query is provided
#             if search_query:
#                 sql += (f" WHERE airlineName LIKE '%{search_query}%' OR flightName LIKE '%{search_query}%' "
#                         f"OR status LIKE '%{search_query}%'")
#
#             # Add LIMIT and OFFSET for pagination
#             sql += f" LIMIT {flights_per_page} OFFSET {offset}"
#
#             # Execute the query to fetch the current page of flight data
#             cur.execute(sql)
#             flights_data = cur.fetchall()
#
#             # Get the IDs of flights already in watchlistdetails table
#             watchlist_ids_query = "SELECT flight_id FROM watchlistdetails"
#             cur.execute(watchlist_ids_query)
#             watchlist_ids = [row[0] for row in cur.fetchall()]
#
#             # SQL query to get the total number of flights with the search filter applied
#             count_sql = f"SELECT COUNT(*) FROM flightdetails"
#
#             # Apply search filter if a search_query is provided
#             if search_query:
#                 count_sql += f" WHERE airlineName LIKE '%{search_query}%'"
#
#             cur.execute(count_sql)
#             total_flights = cur.fetchone()[0]
#
#         # Calculate the total number of pages
#         total_pages = (total_flights + flights_per_page - 1) // flights_per_page
#
#         # Define the number of pagination links to display
#         max_pagination_links = 3
#
#         # Calculate the start and end page numbers for the pagination links
#         start_page = max(1, page - max_pagination_links // 2)
#         end_page = min(total_pages, start_page + max_pagination_links - 1)
#
#         # Close the database connection
#         conn.close()
#
#         return render_template('check-flight.html', flights=flights_data, current_page=page,
#                                total_pages=total_pages, start_page=start_page, end_page=end_page,
#                                search_query=search_query, flights_per_page=flights_per_page,
#                                total_flights=total_flights, watchlist_ids=watchlist_ids)
#
#     except Exception as e:
#         print("Error occurred while fetching data:", str(e))
#         return "An error occurred while fetching data."

@app.route('/check-flight', methods=['GET'])
def checkFlightView():
    if not session.get('logged_in'):
        # User is not logged in, redirect to the login page
        return redirect(url_for('login'))

    try:
        # Get the 'page', 'search', and 'status' query parameters from the URL
        page = request.args.get('page', default=1, type=int)
        search_query = request.args.get('search', default='', type=str)
        status = request.args.get('status', default='', type=str)

        # Define the number of flights to display per page
        flights_per_page = 10

        # Calculate the offset based on the current page number
        offset = (page - 1) * flights_per_page

        # Establish the database connection
        conn = get_db_connection()

        # Use a context manager to create a cursor and automatically close it
        with conn.cursor() as cur:
            # SQL query to fetch data from the database with pagination and search filter
            sql = f"SELECT id, flightName, airlineName, arrivalTime, departureTime, status, futurePrediction " \
                  f"FROM flightdetails WHERE 1=1"

            # Apply search filter if a search_query is provided
            if search_query:
                sql += f" AND (airlineName LIKE '%{search_query}%' OR flightName LIKE '%{search_query}%')"

            # Apply status filter if a status is selected
            if status:
                sql += f" AND status = '{status}'"

            # Add LIMIT and OFFSET for pagination
            sql += f" LIMIT {flights_per_page} OFFSET {offset}"

            # Execute the query to fetch the current page of flight data
            cur.execute(sql)
            flights_data = cur.fetchall()

            # Get the IDs of flights already in watchlistdetails table
            watchlist_ids_query = "SELECT flight_id FROM watchlistdetails"
            cur.execute(watchlist_ids_query)
            watchlist_ids = [row[0] for row in cur.fetchall()]

            # SQL query to get the total number of flights with the search filter applied
            count_sql = f"SELECT COUNT(*) FROM flightdetails WHERE 1=1"

            # Apply search filter if a search_query is provided
            if search_query:
                count_sql += f" AND (airlineName LIKE '%{search_query}%' OR flightName LIKE '%{search_query}%')"

            cur.execute(count_sql)
            total_flights = cur.fetchone()[0]

        # Calculate the total number of pages
        total_pages = (total_flights + flights_per_page - 1) // flights_per_page

        # Define the number of pagination links to display
        max_pagination_links = 3

        # Calculate the start and end page numbers for the pagination links
        start_page = max(1, page - max_pagination_links // 2)
        end_page = min(total_pages, start_page + max_pagination_links - 1)

        # Close the database connection
        conn.close()

        return render_template('check-flight.html', flights=flights_data, current_page=page,
                               total_pages=total_pages, start_page=start_page, end_page=end_page,
                               search_query=search_query, flights_per_page=flights_per_page,
                               total_flights=total_flights,watchlist_ids=watchlist_ids,
                               selected_status=status)

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


def insert_or_update_data(data_list):
    if not session.get('logged_in'):
        # Return an error response if the user is not logged in
        return redirect(url_for('login'))
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
                update_sql = (
                    "UPDATE flightdetails SET airlineName = %s, arrivalTime = %s, departureTime = %s, status = %s "
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


@app.route('/toggle-watchlist', methods=['POST'])
def toggleWatchlist():
    if not session.get('logged_in'):
        return redirect('login')

    try:
        data = request.get_json()
        flight_id = data.get('flightId')
        is_checked = data.get('isChecked')

        # Establish the database connection
        conn = get_db_connection()

        with conn.cursor() as cur:
            if is_checked:
                insert_query = "INSERT INTO watchlistdetails (flight_id) VALUES (%s)"
                print(insert_query,"bbkb")
                cur.execute(insert_query, (flight_id,))
            else:
                delete_query = "DELETE FROM watchlistdetails WHERE flight_id = %s"
                cur.execute(delete_query, (flight_id,))
            conn.commit()

        conn.close()

        return redirect('check-flight')

    except Exception as e:
        return "An error occurred while processing the request", 500


@app.route('/add-all-to-watchlist', methods=['POST'])
def addAllToWatchlist():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    try:
        data = request.get_json()
        flight_ids = data.get('flightIds')
        print(flight_ids, "ids")

        # Establish the database connection
        conn = get_db_connection()

        with conn.cursor() as cur:
            for flight_id in flight_ids:
                # Check if the flight_id already exists in watchlistdetails table
                check_query = "SELECT flight_id FROM watchlistdetails WHERE flight_id = %s"
                cur.execute(check_query, (flight_id,))
                existing_entry = cur.fetchone()

                if existing_entry is None:
                    # If the entry doesn't exist, insert it
                    insert_query = "INSERT INTO watchlistdetails (flight_id) VALUES (%s)"
                    cur.execute(insert_query, (flight_id,))
                # else :
                #     delete_query = "DELETE FROM watchlistdetails WHERE flight_id = %s"
                #     cur.execute(delete_query, (flight_id,))

            conn.commit()

        conn.close()

        return "Flights added to watchlist successfully", 200

    except Exception as e:
        return "An error occurred while processing the request", 500


@app.route('/watchlist')
def watchlist():
    if not session.get('logged_in'):
        # User is not logged in, redirect to the login page
        return redirect(url_for('login'))

    try:
        # Establish the database connection
        conn = get_db_connection()

        # Use a context manager to create a cursor and automatically close it
        with conn.cursor() as cur:
            # SQL query to fetch flight details from watchlistdetails table and flightdetails table
            sql = """
            SELECT wd.id, fd.flightName, fd.airlineName, fd.arrivalTime, fd.departureTime, fd.status
            FROM watchlistdetails wd
            JOIN flightdetails fd ON wd.flight_id = fd.id
            """
            cur.execute(sql)
            watchlist_data = cur.fetchall()
            print(watchlist_data, "jbkjb")

        # Close the database connection
        conn.close()

        return render_template('watchlist.html', watchlist_data=watchlist_data)

    except Exception as e:
        # Return an error response if there's an exception
        return "An error occurred while fetching data", 500




@app.route('/remove-from-watchlist/<int:id>', methods=['POST'])
def removeFromWatchlist(id):
    if not session.get('logged_in'):
        # Return an error response if the user is not logged in
        return redirect(url_for('login'))

    try:
        # Establish the database connection
        conn = get_db_connection()

        # Use a context manager to create a cursor and automatically close it
        with conn.cursor() as cur:
            # SQL query to remove the watchlist data with the given id
            sql = "DELETE FROM watchlistdetails WHERE id = %s"
            cur.execute(sql, (id,))

            # Commit the changes to the database
            conn.commit()

        # Close the database connection
        conn.close()

        # Redirect back to the Watchlist page after successful removal
        return redirect(url_for('watchlist'))

    except Exception as e:
        # Return an error response if there's an exception
        return "An error occurred while processing the request", 500


@app.route('/watchlist_search', methods=['GET'])
def watchlist_search():
    # Get search parameters from the form
    flight_name = request.args.get('flight_name', default='', type=str)
    airline_name = request.args.get('airline_name', default='', type=str)
    arrival_time = request.args.get('arrival_time', default='', type=str)
    departure_time = request.args.get('departure_time', default='', type=str)
    status = request.args.get('status', default='')

    # Establish the database connection
    conn = get_db_connection()

    try:
        # Use a context manager to create a cursor and automatically close it
        with conn.cursor() as cur:
            # SQL query to fetch data based on search parameters, joining with flightdetails table
            sql = """
            SELECT wd.id, fd.flightName, fd.airlineName, fd.arrivalTime, fd.departureTime, fd.status
            FROM watchlistdetails wd
            JOIN flightdetails fd ON wd.flight_id = fd.id
            WHERE (fd.airlineName LIKE %s AND fd.flightName LIKE %s) OR
                  fd.arrivalTime LIKE %s OR fd.departureTime LIKE %s OR fd.status = %s
            """
            cur.execute(sql, (f'%{airline_name}%', f'%{flight_name}%', f'%{arrival_time}%', f'%{departure_time}%', status))

            search_results = cur.fetchall()


    except Exception as e:
        error_message = "An error occurred while processing the request"
        print("An error occurred:", str(e))
        return render_template('search_watchlist.html', error_message=error_message)

    finally:
        # Close the database connection
        conn.close()
    return render_template('search_watchlist.html', searched_flights=search_results,
                           flight_name=flight_name, airline_name=airline_name,
                           arrival_time=arrival_time, departure_time=departure_time,
                           status=status)








