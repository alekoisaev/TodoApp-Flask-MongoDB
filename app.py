from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://<user>:<password>@cluster0.qjwu5.mongodb.net/<database>?retryWrites=true&w=majority'
mongo = PyMongo(app)

todos = mongo.db.todos


@app.route('/')
def index():
    db_todo = todos.find()
    return render_template('index.html', todos=db_todo)


@app.route('/add', methods=['POST'])
def add_todo():
    new_todo = request.form.get('new-todo')
    todos.insert_one({'text': new_todo, 'complete': 'No'})
    return redirect(url_for('index'))


@app.route('/complete/<oid>')
def complete_todo(oid):
    td = todos.find_one({'_id': ObjectId(oid)})
    td['complete'] = 'Completed'
    todos.save(td)
    return redirect(url_for('index'))


@app.route('/delete/<oid>')
def delete_todo(oid):
    td = todos.find_one({'_id': ObjectId(oid)})
    todos.remove(td)
    return redirect(url_for('index'))
