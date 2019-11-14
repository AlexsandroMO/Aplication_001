# https://maxcnunes.com/post/2012/12/24/desenvolvendo-pequena-aplicacao-web-python-flask/

# Created by:  Alexsandro Monteiro
# Date:        19/02/2019
# Site for Tests Python / Flask

# Python any Where
# https://www.pythonanywhere.com/user/AlexsandroMO/
# pip install flask

from flask import Flask, render_template, url_for, request, redirect, send_file, send_from_directory
import db
import os

# import xlrd

# ==================================
app = Flask(__name__)


class Var_State():
    def __init__(self, login_acess):
        self.login_acess = login_acess

Var_State.login_acess = False

@app.route("/")
@app.route("/home")
def home():
    status = Var_State.login_acess
    return render_template('home.html', status=status)

@app.route("/create")
def create():
    return render_template('create.html')

@app.route("/userarea_loged")
def userarea_loged():
    return render_template('userarea_loged.html')

@app.route("/fileform")
def fileform():
    return render_template('fileform.html')


@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/upload")
def upload():
    create_var = db.create_list()
    print(create_var)
    return render_template('upload.html')

@app.route("/logout")
def logout():
    Var_State.login_acess = False
    return render_template('home.html')

@app.route("/download")
def download():
    return redirect(url_for('static', filename='NCR_RAI_LIBERAR.xlsx'))

@app.route('/userarea', methods=['POST', 'GET'])
def userarea():
    if request.method == 'POST':
        resultuserarea = request.form
        email = resultuserarea['email']
        password = resultuserarea['password']

        convert_ = db.query_email_confere(email, password)

        email_ = convert_[0]['EMAIL']
        password_ = convert_[0]['PASSWORD']
        name_user = convert_[0]['FIRST_NAME']

        if email == '' or password == '':
            return f"""
        <p>Atenção, Todos os campos precisam ser preenchidos... :( </p>
        <br>
        <br>
        <br>
        <p><a href="/cotation"><img src="https://image.flaticon.com/icons/png/512/54/54906.png" alt="some text" width=40 height=40></p>

     """

        if email == email_.lower() and password == password_:
            Var_State.login_acess = True

            status = Var_State.login_acess

            if status == True:
                return render_template("userarea.html", title='Python_Flask', status=status,
                                       name_user=name_user.lower().capitalize())

            else:
                return render_template("login.html", email=email)

        else:
            return render_template("message.html", email=email)


'''@app.route('/createtable', methods = ['POST', 'GET'])
def createtable():
  print('=====================')
  if request.method == 'POST':
    resultupload = request.form
    print('>>>>>>> ', resultupload)
    result = resultupload['doc']
    print(result)

    create_var = db.create_list()
    print(create_var)

    return render_template('createtable.html')
'''


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/erro')
def erro():
    return render_template('erro.html')


@app.route('/dbname', methods=['POST', 'GET'])
def dbname():
    if request.method == 'POST':
        resultdbname = request.form
        # print(resultdbname)
        firstname = resultdbname['firstname']
        lastname = resultdbname['lastname']
        email1 = resultdbname['email1']
        email2 = resultdbname['email2']
        password1 = resultdbname['password1']
        password2 = resultdbname['password2']
        # print(resultdbname)
        # print('>>: ', email1)
        # print('>>: ', password1)
        # print('>>: ', email2)
        # print('>>: ', password2)
        # print('>>: ', firstname)
        # print('>>: ', lastname)

        if firstname and lastname and email1 and email2 and password1 and password2 != '':
            if email1 != email2:
                return f"""
          <p>Atenção! Senhas não São Identicas... :( </p>
          <br>
          <br>
          <br>
          <p><a href="/register"><img src="https://image.flaticon.com/icons/png/512/54/54906.png" alt="some text" width=40 height=40></p>

          """
            if password1 != password2:
                return f"""
          <p>Atenção! Senhas não São Identicas... :( </p>
          <br>
          <br>
          <br>
          <p><a href="/register"><img src="https://image.flaticon.com/icons/png/512/54/54906.png" alt="some text" width=40 height=40></p>

          """
            else:
                db.registerDB(firstname.upper(), lastname.upper(), email1.upper(), password1)
                return render_template('dbname.html', firstname=firstname)
        else:
            return f"""
          <p>Atenção, Todos os campos precisam ser preenchidos... :( </p>
          <br>
          <br>
          <br>
          <p><a href="/register"><img src="https://image.flaticon.com/icons/png/512/54/54906.png" alt="some text" width=40 height=40></p>

          """

@app.route('/handleUpload', methods=['POST'])
def handleFileUpload():
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            print('foi')
            photo.save(os.path.join('static/', photo.filename))
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
