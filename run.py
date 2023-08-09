from app import app
from app.views.tables import create_tables

app.secret_key = "your_secret_key"

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=7000)
