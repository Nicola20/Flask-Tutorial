from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'todo.db')

db = SQLAlchemy(app)


class Entry(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(300))
	# done = db.Column(db.Boolean)


@app.route('/')
def index():
    entries = Entry.query.all()
    return render_template('index.html', entries=entries)


@app.route('/add', methods=['POST'])
def add():
	entry = Entry(text= request.form['adding'])
	db.session.add(entry)
	db.session.commit()

	return redirect(url_for('index'))


@app.route('/delete' , methods=['POST'])
def delete():
	todo_ids = request.form.getlist('task')
	for todo_id in todo_ids:
		entry = Entry.query.filter_by(id=int(todo_id)).first()
		db.session.delete(entry)

	db.session.commit()

	return redirect(url_for('index'))


if __name__ == '__main__':
	app.run(debug=True)