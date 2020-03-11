import flask
import pymongo
from bson import ObjectId
from flask import render_template, Flask, redirect, request, session

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["CRUD"]
collection_contacts = db["Contacts"]
collection_companies = db["Companies"]


@app.route("/")
def contact():
    items = collection_contacts.find()
    companies = collection_companies.find({})

    return render_template('contact.html', items=items, value=companies)


@app.route("/company")
def company():
    items = collection_companies.find()
    docs = list(items)
    result = []
    for doc in docs:
        item = {'name': doc['name'], 'email': doc['email']}

        result.append(item)
    return render_template('company.html', items=result)


@app.route("/remove", methods=['GET', 'POST'])
def remove_id():
    key = request.values.get("_id")
    cmp = collection_companies.find_one({'_id': key})
    if cmp:
        collection_companies.remove({"_id": ObjectId(key)})
        return redirect("/company")
    collection_contacts.remove({"_id": ObjectId(key)})
    return redirect("/")


@app.route('/add_new_user', methods=['POST'])
def add_new_user():
    contacts = collection_contacts
    name_user = request.values.get('name_user')
    email = request.values.get('email')
    position = request.values.get('position')
    contacts.insert({"name_user": name_user, "email": email, "position": position})
    return redirect('/')


@app.route('/add_new_company', methods=['POST'])
def add_new_company():
    companies = collection_companies
    name_user = request.values.get('name')
    email = request.values.get('email')
    companies.insert({"name": name_user, "email": email, "Сотрудники": {}})
    return redirect('/company')


@app.route("/add")
def add_user_to_company():
    key = request.values.get("_id")
    print(collection_companies.find_one({'Сотрудники': {'_id': key}}))
    return redirect('/company')


@app.route("/update")
def update():
    id = request.values.get("_id")
    task = collection_contacts.find({"_id": ObjectId(id)})
    return render_template('result.html', tasks=task)


@app.route("/action3", methods=['POST'])
def update_contact():
    # Updating a Task with various references
    id = request.values.get("_id")
    name = request.values.get('name_user')
    email = request.values.get('email')
    position = request.values.get('position')
    collection_contacts.update({"_id": ObjectId(id)}, {'$set': {"name_user": name, "email": email, "position": position}})
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
