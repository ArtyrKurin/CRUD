import flask
import pymongo
from flask import render_template, Flask, redirect, request

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["CRUD"]
collection = db["Contacts"]
collection_companies = db["Companies"]


@app.route("/")
def home():
    count = collection_companies.count()

    return render_template('main.html', count=count)


@app.route('/result', methods=['POST', 'GET'])
def result():
    name_company = request.get.args('keys')
    email_company = request.get.args('email')
    test = collection_companies.insert('Name company' + name_company, 'email company' + email_company)
    print(test)
    return render_template("main.html", result=result)


# @app.route('/contact')
# def contacts():
#     cursor = collection.find({})
#
#     return render_template('contacts.html', cursor=cursor)


# @app.route('/del')
# def delete():
#     collection.delete_one()
#     collection_companies.delete_one()
#     redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
