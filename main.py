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
    items = collection_companies.find({})
    docs = list(items)
    result = []
    for doc in docs:
        item = {'name': doc['name'], 'email': doc['email'], 'Сотрудники': [doc['_id']]}
        if doc['Сотрудники']:
            for data in doc['Сотрудники']:
                emp = collection_contacts.find_one({'_id': data['_id']})
                if emp:
                    item['staff'].append({'name': emp['name']})
            result.append(item)
        print(result)
    return render_template('company.html', items=result)


@app.route("/remove", methods=['GET', 'POST'])
def remove_contact():
    key = request.values.get("_id")
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


@app.route('/company/add_new_company', methods=['POST'])
def add_new_company():
    companies = collection_companies
    name_user = request.values.get('name')
    email = request.values.get('email')
    companies.insert({"name": name_user, "email": email, "Сотрудники": []})
    return redirect('/company')


@app.route("/company/update")
def update():
    id = request.values.get("_id")
    task = collection_contacts.find({"_id": ObjectId(id)})
    return render_template('result.html', tasks=task)


@app.route("/company/action3", methods=['POST'])
def update_contact():
    # Updating a Task with various references
    id = request.values.get("_id")
    name = request.values.get('name_user')
    email = request.values.get('email')
    position = request.values.get('position')
    collection_contacts.update({"_id": ObjectId(id)},
                               {'$set': {"name_user": name, "email": email, "position": position}})
    return redirect("/")


@app.route("/company/add")
def add_user_to_company():
    # key = request.values.get("_id")
    # name = request.values.get('name')
    # email = request.values.get('email')
    # find_in_contacts = collection_contacts.find_one({'Сотрудники': {'_id': key}})
    # find_in_company = collection_companies.find_one({'Сотрудники': {'_id': key}})
    # if find_in_company:
    #     print('В наличии')
    #     redirect('/company')
    # else:
    #     collection_companies.update({"_id": ObjectId(key)},
    #                                 {'$set': {"name": name, "email": email, 'Сотрудники': {'_id': find_in_contacts}}})
    return redirect('/company')


@app.route("/update", methods=['POST'])
def update_company():
    # Updating a Task with various references
    id = request.values.get("_id")
    name = request.values.get('name')
    email = request.values.get('email')
    collection_companies.update({"_id": ObjectId(id)}, {'$set': {"name": name, "email": email}})
    return redirect("/")


@app.route("/company/removing", methods=['GET', 'POST'])
def remove_company():
    key = request.values.get('_id')
    collection_companies.remove({"_id": ObjectId(key)})
    return redirect("/company")


if __name__ == '__main__':
    app.run(debug=True)
