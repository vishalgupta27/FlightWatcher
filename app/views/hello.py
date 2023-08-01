from app import app


@app.route('/hello')
def hello():
    return '<h1 style="text-align:center">ॐ नमः शिवाय!</h1>'