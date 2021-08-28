from flask import Flask, render_template, request, redirect, url_for, session
from sqlite3 import *
import pickle

app = Flask(__name__)
app.secret_key = 'lungcancerdetection'

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
    if request.method == 'POST':
        uname = request.form['uname']
        pw = request.form['pw']
        con=None
        try:
            con = connect('lung_cancer.db')
            cursor = con.cursor()
            sql = "select * from users where uname ='%s' and pw = '%s'"
            cursor.execute(sql % (uname,pw))
            con.commit()
            data = cursor.fetchall()
            if len(data) == 0:
                return render_template('login.html', msg = 'invalid login')
            else:
                session['uname'] = uname
                return redirect(url_for('main'))

        except Exception as e:
            con.rollback()
            msg = "issue" + str(e)
            return render_template('login.html',msg=msg)
        
        finally:
            if con is not None:
                con.close()
    else:
        return render_template('login.html')

@app.route('/main', methods=['POST','GET'])
def main():
    if 'uname' in session:
        return render_template('main.html', name=session['uname'])
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=['POST','GET'])
def logout():
	session.pop('uname',None)
	return redirect(url_for('login'))

@app.route('/check', methods=["POST","GET"])
def check():
    if request.method == 'POST':
        age = request.form['age']
        r2 = request.form['r2']
        if r2 == 'yes':
            smoke = '1'
        else:
            smoke = '0'

        r3 = request.form['r3']
        if r3 == 'yes':
            yf = '1'
        else:
            yf = '0'
        
        r4 = request.form['r4']
        if r4 == 'yes':
            a = '1'
        else:
            a = '0'

        r5 = request.form['r5']
        if r5 == 'yes':
            pp = '1'
        else:
            pp = '0'

        r6 = request.form['r6']
        if r6 == 'yes':
            cd = '1'
        else:
            cd = '0'
        
        r7 = request.form['r7']
        if r7 =="yes":
            f = '1'
        else:
            f = '0'
        
        r8 = request.form['r8']
        if r8 =='yes':
            allergy = '1'
        else:
            allergy = '0'
        
        r9 = request.form['r9']
        if r9 == 'yes':
            wheezing = '1'
        else:
            wheezing = '0'

        r10 = request.form['r10']
        if r10 == 'yes':
            alch = '1'
        else:
            alch = '0'
        
        r11 = request.form['r11']
        if r11 == 'yes':
            cough = '1'
        else:
            cough = '0'

        r12 = request.form['r12']
        if r12 == 'yes':
            sob = '1'
        else:
            sob = '0'

        r13 = request.form['r13']
        if r13 == 'yes':
            swallow = '1'
        else:
            swallow = '0'

        r14 = request.form['r14']
        if r14 == 'yes':
            cp = '1'
        else:
            cp = '0'
        
        r15 = request.form['r15']
        if r15 == 'male':
            gender = '1'
        else:
            gender = '0'
        
        d = [[age,smoke,yf,a,pp,cd,f,allergy,wheezing,alch,cough,sob,swallow,cp,gender]]
        with open('db.model', 'rb') as f:
            model = pickle.load(f)
        res = model.predict(d)
        res = str(res)
        return render_template('main.html', msg=res)

    else:
        return render_template('main.html')






        
if __name__ == '__main__':
	app.run(debug=True)