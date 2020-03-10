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
    count = collection_contacts.count()
    items = collection_contacts.find()
    companies = collection_companies.find()
    return render_template('contact.html', count=count, items=items, value=companies)


@app.route("/company")
def company():
    count = collection_companies.count()
    items = collection_companies.find()
    docs = list(items)
    result = []
    for doc in docs:
        item = {'name': doc['name'], 'email': doc['email']}
        if doc['Сотрудники']:
            for data in doc['Сотрудники']:
                emp = collection_contacts.find_one({'_id': data['_id']})
                if emp:
                    item['staff'].append({'name_user': emp['name_user']})
        result.append(item)
    return render_template('company.html', count=count, items=result)


@app.route("/remove")
def remove_id():
    key = request.values.get("_id")
    collection_contacts.remove({"_id": ObjectId(key)})
    return redirect("/")


@app.route("/add_to_company")
def add_to_company():
    # Remove by Id
    key = request.values.get("_id")
    find = collection_contacts.find({"_id": ObjectId(key)})
    collection_companies.insert(find)
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


# Finish tomorrow
@app.route("/edit")
def edit_contact():
    name = request.values.get('name')
    email = request.values.get('email')
    position = request.values.get('position')
    id = request.values.get("_id")
    update = collection_contacts.update({"_id": ObjectId(id)},
                                        {'$set': {"name": name, "email": email, "position": position}})
    return render_template('result.html', update=update)


if __name__ == '__main__':
    app.run(debug=True)
