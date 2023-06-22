from flask import Flask, render_template, jsonify, request, url_for
import sqlalchemy as db


engine = db.create_engine('sqlite:///grade.sqlite', echo=True)
connection = engine.connect()
metadata = db.MetaData()
students = db.Table(
    'students', metadata,
    db.Column('name', db.String),
    db.Column('grade', db.Integer)
)

metadata.create_all(engine)

query = students.select()
data = connection.execute(query)
result = data.fetchall()
print(students.columns.keys())
print(result)

app = Flask(__name__, template_folder='templates', static_folder='static')
# flask modules and functions for web app, json response, handling http request and generating URLs


@app.route('/')
def index():
    return render_template('index.html') # render index.html template

# Decorator for handling get requests for names
@app.route('/grades/<string:name>/', methods=['GET'])
def searchGrade(name):
    query = students.select().where(students.c.name == name)
    result = connection.execute(query)
    data = result.fetchall()
    if data: #run if student is in database
        data = [tuple(row) for row in data]
        data = dict(data)
        return jsonify(data), 200
    else:
        return "error", 400


@app.route('/grades/', methods=['GET'])  # Get request for all student grades
def listGrade():
    query = students.select()
    result = connection.execute(query)
    data = result.fetchall()
    data = [tuple(row) for row in data]
    data = dict(data)
    return jsonify(data)  # Returns all names


# Decorator handling post requests for creating new student and grade
@app.route('/grades/', methods=['POST'])
def createGrade():  # Create grade based on JSON data in body
    name = request.get_json().get('name')
    query = students.select().where(students.c.name == name)
    result = connection.execute(query)
    data = result.fetchall()
    if not data: # run if student is not in database
        grade = request.get_json().get('grade')
        query = students.insert().values(name=(name), grade=(grade))
        connection.execute(query)
        connection.commit()
        return jsonify({name: grade}), 200
    else:
        return "error", 400


@app.route('/grades/<string:name>/', methods=['PUT'])  # Handles put requests
def editGrade(name):  # Edit based on JSON data
    query = students.select().where(students.c.name == name)
    result = connection.execute(query)
    data = result.fetchall()
    if data: #run if student is in database
        grade = request.get_json().get('grade')
        query = students.update().values(grade=(grade)).where(students.c.name == name)
        connection.execute(query)
        connection.commit()
        return jsonify({name: grade}), 200
    else:
        return "error", 400


# Handles delete requests
@app.route('/grades/<string:name>/', methods=['DELETE'])
def deleteGrade(name):  # Delete based on JSON data
    query = students.select().where(students.c.name == name)
    result = connection.execute(query)
    data = result.fetchall()
    if data: #run if student is in database
        query = students.delete().where(students.c.name == name)
        connection.execute(query)
        connection.commit()
        return jsonify({name: name}), 200
    else:
        return "error", 400


if __name__ == '__main__':
    app.run()  # Executes script directly to run Flask app
