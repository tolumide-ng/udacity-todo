from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jdotdkzm:aft7jIHUKOOUT6wCdtMMWQoH7E0Vn1Sa@salt.db.elephantsql.com:5432/jdotdkzm'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todo(db.Model):

	__tablename__ = 'todos'

	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(), nullable=False)

	def __repr__(self):
		return f'<Todo description={self.description} id={self.id}>'



@app.route('/')
def index():
	return render_template('index.html', data = Todo.query.all())
