

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# @app.route('/login', methods=['POST', 'GET'])
# def userLogin():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username != "anand":
#             print("Please enter valid username")
#             return redirect('/login')
#         if password != "123456789":
#             print("Please enter valid password")
#             return redirect('/login')
#         username = "anand"
#         password = "123456789"
#         return redirect('/')
#     return render_template('auth/login.html')