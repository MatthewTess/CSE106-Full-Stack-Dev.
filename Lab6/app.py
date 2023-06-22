from flask import Flask, render_template, jsonify, request, url_for

app = Flask(__name__, template_folder='templates', static_folder='static')
# flask modules and functions for web app, json response, handling http request and generating URLs
# create argument name and sets path to static

students = {"amy": 90, "bob": 80, "caty": 70, "dan": 60}


# student name and grades

@app.route('/')
def index():
    return render_template('index.html')


# render index.html template

@app.route('/grades/<string:name>/', methods=['GET'])  # Decorator for handling get requests for names
def searchGrade(name):
    if name in students:
        return jsonify({name: students.get(name)}), 200
    else:
        return "error", 400


@app.route('/grades/', methods=['GET'])  # Get request for all student grades
def listGrade():
    return jsonify(students)  # Returns all names


@app.route('/grades/', methods=['POST'])  # Decorator handling post requests for creating new student and grade
def createGrade():  # Create grade based on JSON data in body
    name = request.get_json().get('name')
    if name not in students:
        grade = request.get_json().get('grade')
        students[name] = grade
        return jsonify({name: grade}), 200
    else:
        return "error", 400


@app.route('/grades/<string:name>/', methods=['PUT'])  # Handles put requests
def editGrade(name):  # Edit based on JSON data
    if name in students:
        grade = request.get_json().get('grade')
        students[name] = grade
        return jsonify({name: grade}), 200
    else:
        return "error", 400


@app.route('/grades/<string:name>/', methods=['DELETE'])  # Handles delete requests
def deleteGrade(name):  # Delete based on JSON data
    if name in students:
        del students[name]
        return jsonify({name: students.get(name)}), 200
    else:
        return "error", 400


if __name__ == '__main__':
    app.run()  # Executes script directly to run Flask app
