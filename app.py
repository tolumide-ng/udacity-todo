import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# 'postgres://udacitystudios@localhost:5432/todoapp'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://jdotdkzm:aft7jIHUKOOUT6wCdtMMWQoH7E0Vn1Sa@salt.db.elephantsql.com:5432/jdotdkzm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mac@localhost:5432/todoapp'


# todo=# \conninfo
# You are connected to database "secret" as user "secret" via socket in "/secret" at port "5432".

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo description={self.description} id={self.id}'


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return
    # return redirect(url_for('index'))


@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})


@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    # description=request.form.get('description', '')
    description = request.get_json()['description']
    try:
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        db.session.rollback()
        error = True
        print(sys.exec_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.order_by('id').all())
