from app import app


@app.route('/hello')
def hello():
    return '<h1 style="text-align:center">ॐ नमः शिवाय!</h1>'


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
#         # SQL query to fetch data from the database with pagination and search filter
#         sql = f"SELECT flightName, airlineName, arrivalTime, departureTime, status, futurePrediction, isWatchlist " \
#               f"FROM flightdetails WHERE airlineName LIKE '%{search_query}%' " \
#               f"LIMIT {flights_per_page} OFFSET {offset}"
#         print("SQL Query:", sql)
#
#         # Execute the query to fetch the current page of flight data
#         cur.execute(sql)
#         flights_data = cur.fetchall()
#         print("Fetched Data:", flights_data)
#
#         # SQL query to get the total number of flights with the search filter applied
#         count_sql = f"SELECT COUNT(*) FROM flightdetails WHERE airlineName LIKE '%{search_query}%'"
#         cur.execute(count_sql)
#         total_flights = cur.fetchone()[0]
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
#         return render_template('check-flight.html', flights=flights_data, current_page=page,
#                                total_pages=total_pages, start_page=start_page, end_page=end_page,
#                                search_query=search_query)
#
#     except Exception as e:
#         print("Error occurred while fetching data:", str(e))
#         return "An error occurred while fetching data."
# Create table watchlistDetails(
#    id INT NOT NULL AUTO_INCREMENT,
#    airlineName VARCHAR(100) NOT NULL,
#    flightName VARCHAR(100) NOT NULL,
#    arrivalTime DATETIME,
#    status VARCHAR(40),
#    PRIMARY KEY ( id )
# );



# <div class="col-lg-3 col-md-4 text-center">
#     <form action="{{ url_for('add_to_watchlist') }}" method="POST">
#         <label class="form-label">
#             Add all to watchlist
#         </label><br />
#         <span class="form-check form-switch">
#             <input type="checkbox" name="flightCheckboxs"
#                    value="{% for flight in flights %}
#                            {{ flight[1] }},{{ flight[0] }},{{ flight[2] }},{{ flight[3] }},{{ flight[4] }}
#                            {% if not loop.last %};{% endif %}
#                            {% endfor %}"
#                    class="form-check-input" />
#         </span>
#     </form>
# </div>



# def create_tables():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#
#         # Create the flightdetails table if it doesn't exist
#         flightdetails = """
#             CREATE TABLE IF NOT EXISTS flightdetails (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 flightName VARCHAR(255),
#                 airlineName VARCHAR(255),
#                 arrivalTime DATETIME,
#                 departureTime DATETIME,
#                 status VARCHAR(255)
#             )
#         """
#         cursor.execute(flightdetails)
#
#         # Create the watchlistdetails table with a foreign key reference to flightdetails
#         watchlistdetails = """
#             CREATE TABLE IF NOT EXISTS watchlistdetails (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 flight_id INT,
#                 FOREIGN KEY (flight_id) REFERENCES flightdetails(id),
#                 airlineName VARCHAR(255),
#                 flightName VARCHAR(255),
#                 arrivalTime DATETIME,
#                 departureTime DATETIME,
#                 status VARCHAR(255)
#             )
#         """
#         cursor.execute(watchlistdetails)
#
#         conn.commit()
#         cursor.close()
#         conn.close()
#
#         print("Tables created successfully!")
#
#     except Exception as e:
#         print("Error:", e)
#         return "An error occurred while processing the request", 500


# # Get the 'search' and 'status' query parameters from the URL
# search_query = request.args.get('search', default='', type=str)
# status = request.args.get('status', default='', type=str)
#
# # ...
#
# # SQL query to fetch data from the database with pagination and search filter
# sql = f"SELECT id, flightName, airlineName, arrivalTime, departureTime, status, futurePrediction " \
#       f"FROM flightdetails"
#
# # Apply combined search filter for airlineName/flightName and status
# if search_query and status:
#     sql += f" WHERE (airlineName LIKE '%{search_query}%' OR flightName LIKE '%{search_query}%') " \
#            f"AND status = '{status}'"
# elif search_query:
#     sql += f" WHERE airlineName LIKE '%{search_query}%' OR flightName LIKE '%{search_query}%'"
# elif status:
#     sql += f" WHERE status = '{status}'"
#
# # Add LIMIT and OFFSET for pagination
# sql += f" LIMIT {flights_per_page} OFFSET {offset}"

# import requests
#
# apiKey = input("API Key: ")
# apiUrl = "https://aeroapi.flightaware.com/aeroapi/"
#
# airport = 'KSFO'
# payload = {'max_pages': 2}
# auth_header = {'x-apikey':apiKey}
#
# response = requests.get(apiUrl + f"airports/{airport}/flights",
#     params=payload, headers=auth_header)
#
# if response.status_code == 200:
#     print(response.json())
# else:
#     print("Error executing request")



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



# def update_data():
#     try:
#         # SQL query to update data in the database
#         sql = "UPDATE flightdetails SET airlineName = %s, status = %s, futurePrediction = %s WHERE flightName = %s"
#
#         # New data to be updated
#         new_airline_name = 'AirAsia'
#         new_status = 'Delayed'
#         new_prediction = 'WithDelay'
#         flight_name_to_update = 'Flight1'
#
#         # Execute the update query with the new values
#         cur.execute(sql, (new_airline_name, new_status, new_prediction, flight_name_to_update))
#
#         # Commit the changes after updating the data
#         conn.commit()
#
#         print("Data updated successfully! The number of rows affected is:", cur.rowcount)
#
#     except Exception as e:
#         # Rollback changes in case of an error
#         conn.rollback()
#         print("Error occurred while updating data:", str(e))


# Call the function to update data in the database
# update_data()


# def remove_duplicates():
#     try:
#         # SQL query to remove duplicate data from the database based on selected columns
#         sql = "DELETE t1 FROM flightdetails t1 INNER JOIN flightdetails t2 " \
#               "WHERE t1.id < t2.id AND t1.flightName = t2.flightName AND t1.airlineName = t2.airlineName"
#
#         # Execute the DELETE query to remove duplicates
#         cur.execute(sql)
#
#         # Commit the changes after removing duplicates
#         conn.commit()
#
#         print("Duplicate data removed successfully! The number of duplicate rows removed is:", cur.rowcount)
#
#     except Exception as e:
#         # Rollback changes in case of an error
#         conn.rollback()
#         print("Error occurred while removing duplicate data:", str(e))


# Call the function to remove duplicate data from the database
# remove_duplicates()


# def delete_table():
#     try:
#         # SQL query to delete all data from the table
#         sql = "DELETE FROM flightdetails"
#
#         # Execute the query to clear the table
#         cur.execute(sql)
#
#         # Commit the changes
#         conn.commit()
#
#     except Exception as e:
#         # Rollback changes in case of an error
#         conn.rollback()
#         print("Error occurred while clearing the table:", str(e))

# @app.route('/watchlist')
# def watchlist():
#     if not session.get('logged_in'):
#         # User is not logged in, redirect to the login page
#         return redirect(url_for('login'))
#
#     try:
#         # Establish the database connection
#         conn = get_db_connection()
#
#         # Use a context manager to create a cursor and automatically close it
#         with conn.cursor() as cur:
#             # SQL query to fetch flight details from watchlistdetails table and flightdetails table
#             sql = """
#             SELECT wd.id, fd.flightName, fd.airlineName, fd.arrivalTime, fd.departureTime, fd.status
#             FROM watchlistdetails wd
#             JOIN flightdetails fd ON wd.flight_id = fd.id
#             """
#             cur.execute(sql)
#             watchlist_data = cur.fetchall()
#             print(watchlist_data, "jbkjb")
#
#         # Close the database connection
#         conn.close()
#
#         return render_template('watchlist.html', watchlist_data=watchlist_data)
#
#     except Exception as e:
#         # Return an error response if there's an exception
#         return "An error occurred while fetching data", 500