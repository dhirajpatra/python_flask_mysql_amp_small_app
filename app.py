from flask import Flask, escape, render_template, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your password'
app.config['MYSQL_DB'] = 'test'

conn = mysql.connector.connect(host=app.config['MYSQL_HOST'],
database=app.config['MYSQL_DB'],
user=app.config['MYSQL_USER'],
password=app.config['MYSQL_PASSWORD']);


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        title = details['title']
        content = details['content']
        try:
            cur = conn.cursor();
            cur.execute("Insert into cms (title, content) values (%s, %s)", (title, content))
            conn.commit()
            id = cur.lastrowid
            cur.close()
        except:
            return 'this was an error on saving into the db'
        
        return "id is %s <a href='/'>Go to Home</a>" % id
    else:
        data = []
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("select * from cms")
            data = cur.fetchall()
            print("Total number of rows in CMS is: ", cur.rowcount)
            cur.close()
            
        except:
            return 'this was an error on fetching data from db'
        
        return render_template('index.html', data=data)

@app.route('/cms/<int:id>')
def cms(id):
    return 'Hellow World'   

@app.route('/user/<username>')
def show_user(username):
    return 'User %s' % escape(username)

if __name__ == "__main__":
    app.run(debug=True)
