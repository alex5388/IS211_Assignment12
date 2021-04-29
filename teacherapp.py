from flask import *
import os, re, sqlite3

app = Flask(__name__)
app.secret_key = ('pass')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin':
            error = 'Invalid Username or Password.'
            return render_template('login.html', error=error)
        elif request.form['password'] != 'password':
            error = 'Invalid Username of Password.'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True      #start a session
            if session.get('logged_in') != None:
                print('session started')
            return redirect('/dashboard')
    else:
        return render_template('login.html', error=error)



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/teacher.db')
    c = conn.cursor()
    c.execute("SELECT * FROM studentinfo, quizinfo")
    info = c.fetchall()   #introduce argument in render_template
    conn.commit()
    return render_template('/dashboard.html', info=info)

@app.route('/student_add', methods=['GET','POST'])
def student_add():
    fname = request.form["fname"]
    lname = request.form["lname"]

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/teacher.db')
    c = conn.cursor()
    c.execute("INSERT INTO studentinfo (fname,lname) VALUES (?,?)",(fname,lname))
    conn.commit()


    return render_template('/student_add.html')




if __name__=="__main__":
    app.run(debug=True)


