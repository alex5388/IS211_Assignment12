from flask import *
import os, re, sqlite3

app = Flask(__name__)
app.secret_key = ('pass')

@app.route('/', methods=['GET','POST'])
def index():
    return redirect(url_for('login'))

#login form
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
            #start session
            session['logged_in'] = True
            if session.get('logged_in') != None:
                print('session started')
            return redirect('/dashboard')
    else:
        return render_template('login.html', error=error)

#function to view roster,quizes,grades
@app.route('/dashboard', methods=['GET'])
def dashboard():
#check for session first otherwise login
    if not session.get('logged_in'):
        return redirect(url_for('login'))
#db connection
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/teacher.db')
    c = conn.cursor()

#select statements to retrieve table data
    c.execute("SELECT * FROM studentinfo")
    student = c.fetchall()     #fetch student info to display
    c.execute("SELECT * FROM quizinfo")
    quiz = c.fetchall()     #fetch quiz info to display
    conn.commit()
    c.execute("SELECT * FROM grades")
    grades = c.fetchall()     #fetch grades
    return render_template('/dashboard.html', student=student, quiz=quiz, grades=grades)

#function to add students to roster
@app.route('/student_add', methods=['GET','POST'])
def student_add():
#check for session first otherwise login
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    fname = request.form["fname"]
    lname = request.form["lname"]

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/teacher.db')
    c = conn.cursor()
    c.execute("INSERT INTO studentinfo (fname,lname) VALUES (?,?)",(fname,lname))
    conn.commit()


    return redirect(url_for('dashboard'))

#function to add quizes
@app.route('/quiz_add', methods=['GET','POST'])
def quiz_add():
#check for session first otherwise login
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    quizid = request.form["quizid"]
    subject = request.form["subject"]
    questions = request.form['questions']
    date = request.form['date']

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/teacher.db')
    c = conn.cursor()
    c.execute("INSERT INTO quizinfo (quizid,subject,questions,date) VALUES (?,?,?,?)",(quizid,subject,questions,date))
    conn.commit()

    return redirect(url_for('dashboard'))

#function to add test results
@app.route('/result_add', methods=['GET','POST'])
def result_add():
#check for session first otherwise login
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    s_id = request.form['student#']
    q_id = request.form['quiz#']
    q_score = request.form['score']

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/teacher.db')
    c = conn.cursor()
    c.execute("INSERT INTO grades (studentid, quizid, score) VALUES (?,?,?)",(s_id, q_id, q_score))
    conn.commit()

    return  redirect(url_for('dashboard'))

#function to delete last row
@app.route('/student_delete', methods=['GET','POST'])
def student_delete():
#check for session first otherwise login
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/teacher.db')
    c = conn.cursor()
    c.execute("DELETE FROM studentinfo where studentid=(select max(studentid) from studentinfo)")
    conn.commit()

    return  redirect(url_for('dashboard'))

#function to delete last row
@app.route('/quiz_delete', methods=['GET','POST'])
def quiz_delete():
#check for session first otherwise login
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/teacher.db')
    c = conn.cursor()
    c.execute("DELETE FROM quizinfo where quizid=(select max(quizid) from quizinfo)")
    conn.commit()

    return  redirect(url_for('dashboard'))

#function to delete last row
@app.route('/grade_delete', methods=['GET','POST'])
def grade_delete():
#check for session first otherwise login
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/teacher.db')
    c = conn.cursor()
    c.execute("DELETE FROM grades where studentid=(select max(studentid) from grades)")
    conn.commit()

    return  redirect(url_for('dashboard'))


if __name__=="__main__":
    app.run(debug=True)


