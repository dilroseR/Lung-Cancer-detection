from flask import Flask, render_template, request, redirect, url_for, session
from sqlite3 import *
from flask_mail import Mail, Message
import pickle

app = Flask(__name__)
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'dreji1234@gmail.com'
app.config['MAIL_PASSWORD'] = 'Abc45678*'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
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
        ls=[]
        age = int(request.form['age'])
        ls.append(age)

        r2 = request.form['r2']
        if r2 == 'yes':
            smoke = '1'
            ls.append("Yes")
        else:
            smoke = '0'
            ls.append("No")

        r3 = request.form['r3']
        if r3 == 'yes':
            yf = '1'
            ls.append("Yes")
        else:
            yf = '0'
            ls.append("No")
        
        r4 = request.form['r4']
        if r4 == 'yes':
            a = '1'
            ls.append("Yes")
        else:
            a = '0'
            ls.append("No")

        r5 = request.form['r5']
        if r5 == 'yes':
            pp = '1'
            ls.append("Yes")
        else:
            pp = '0'
            ls.append("No")

        r6 = request.form['r6']
        if r6 == 'yes':
            cd = '1'
            ls.append("Yes")
        else:
            cd = '0'
            ls.append("No")
        
        r7 = request.form['r7']
        if r7 =="yes":
            f = '1'
            ls.append("Yes")
        else:
            f = '0'
            ls.append("No")
        
        r8 = request.form['r8']
        if r8 =='yes':
            allergy = '1'
            ls.append("Yes")
        else:
            allergy = '0'
            ls.append("No")
        
        r9 = request.form['r9']
        if r9 == 'yes':
            wheezing = '1'
            ls.append("Yes")
        else:
            wheezing = '0'
            ls.append("No")

        r10 = request.form['r10']
        if r10 == 'yes':
            alch = '1'
            ls.append("Yes")
        else:
            alch = '0'
            ls.append("No")
        
        r11 = request.form['r11']
        if r11 == 'yes':
            cough = '1'
            ls.append("Yes")
        else:
            cough = '0'
            ls.append("No")

        r12 = request.form['r12']
        if r12 == 'yes':
            sob = '1'
            ls.append("Yes")
        else:
            sob = '0'
            ls.append("No")

        r13 = request.form['r13']
        if r13 == 'yes':
            swallow = '1'
            ls.append("Yes")
        else:
            swallow = '0'
            ls.append("No")

        r14 = request.form['r14']
        if r14 == 'yes':
            cp = '1'
            ls.append("Yes")
        else:
            cp = '0'
            ls.append("No")
        
        r15 = request.form['r15']
        if r15 == 'male':
            gender = '1'
            ls.append("Male")
        else:
            gender = '0'
            ls.append("Female")

        em = request.form['em']
        print(ls)
        d = [[age,smoke,yf,a,pp,cd,f,allergy,wheezing,alch,cough,sob,swallow,cp,gender]]
        with open('db.model', 'rb') as f:
            model = pickle.load(f)
        res = model.predict(d)
        msg = Message('RESULTS!', sender='dreji1234@gmail.com', recipients=[em])
        if res[0] == 'NO':
            msg.html = "<h2 style='color:red;'>You don't have any symptoms of lung cancer.</h2><h4>Stay Healthy!</h4>"
                 
        else:
            msg.html = "<h2 style='color:red;'>You are likely to have lung cancer.</h2><br><h4>Kindly visit a doctor soon!</h4>"
        
        mail.send(msg)
        return render_template('main.html', msg=1)

    else:
        return render_template('main.html')






        
if __name__ == '__main__':
	app.run(debug=True)