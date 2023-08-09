
from app.views.dashboard import get_db_connection


def create_tables():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        watchlistdetails = """
             CREATE TABLE IF NOT EXISTS watchlistdetails (
                 id INT AUTO_INCREMENT PRIMARY KEY,
                 flight_id INT,
                 FOREIGN KEY (flight_id) REFERENCES flightdetails(id),
                 UNIQUE (flight_id)
             )                                      
             """
        # Execute the queries
        cursor.execute(watchlistdetails)
        conn.commit()

        print("Tables created successfully!")

    except Exception as e:
        print("Error:", e)
        return "An error occurred while processing the request", 500


