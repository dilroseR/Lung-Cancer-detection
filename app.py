from flask import Flask, render_template, request, redirect, url_for, session
from sqlite3 import *

app = Flask(__name__)
@app.route('/', methods=['POST','GET'])
def home():
    return render_template('home.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        uname = request.form['uname']
        pw1 = request.form['pw1']
        pw2 = request.form['pw2']
        if pw1 == pw2:
            con=None
            try:
                con = connect('lung_cancer.db')
                sql = "insert into users values('%s','%s','%s')"
                cursor = con.cursor()  
                cursor.execute(sql % (name,uname,pw1))
                con.commit()
                #print(name,uname,pw1)
                return redirect(url_for('login'))

            except Exception as e:
                con.rollback()
                print("Issue: " ,e)
                return render_template('signup.html',msg='user already registered')

            finally:
                if con is not None:
                    con.close()
        else:
            return render_template('signup.html',msg="Passwords didn't match")
    else:
        return render_template('signup.html')

@app.route('/login', methods=['POST','GET'])
def login():
    return render_template("login.html")


        
if __name__ == '__main__':
	app.run(debug=True)