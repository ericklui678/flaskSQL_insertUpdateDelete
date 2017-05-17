from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'friendsdb')
app.secret_key = 'ThisIsSecret'

@app.route('/')
def index():
    query = 'SELECT * FROM FRIENDS'
    friends = mysql.query_db(query)
    return render_template('index.html', all_friends=friends)

@app.route('/process', methods=['POST'])
def process():
    print 'Got Post Info'
    return redirect('/')

@app.route('/friends/<friend_id>')
def show(friend_id):
    # Write query to select specific user by id. At every point
    # where we want to insert ddata, we write ':' and var name
    query = "SELECT * FROM friends WHERE id = :specific_id"
    # Then define a dictinoary with key that matches            # :variable_name in query
    data = {'specific_id': friend_id}
    # Run query with inserted data
    friends = mysql.query_db(query, data)
    # Friends should be a list with a single object,
    # so we pass the value at [0] to our template under alias    # one_friend
    return render_template('index.html', one_friend=friends[0]['first_name'] + ' ' + friends[0]['last_name'])

@app.route('/friends', methods=['POST'])
def create():
    # Write query as a string. Notice how we have multiple values
    # we want to insert into our query
    query = 'INSERT INTO friends(first_name, last_name, occupation, created_at, updated_at) VALUES(:first_name, :last_name, :occupation, NOW(), NOW())'
    # We'll then create a dictionary of data from the POST data received
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'occupation': request.form['occupation']
    }
    mysql.query_db(query, data)
    # Run query, with dictionary values injected into query
    return redirect('/')

@app.route('/update_friend', methods=['POST'])
def update():
    query = 'UPDATE friends SET first_name = :first_name, last_name = :last_name, occupation = :occupation WHERE id = :id'
    data =  {
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'occupation': request.form['occupation'],
                'id': request.form['numID']
            }
    print mysql.query_db(query,data)
    return redirect('/')

@app.route('/remove_friend', methods=['POST'])
def delete():
    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': request.form['numID']}
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug = True)
