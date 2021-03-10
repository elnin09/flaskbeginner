from flask import Flask ,render_template ,url_for, request, redirect ,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app);



#this is our object for tasks
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return "<Task %r>" % self.id


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            try:
                db.session.add(new_task)
            except:
                return "this issue is here"
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"
    else: 
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/')
    except:
        return redirect('There was a problem deleting that task')

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "there was an issue updating task"
    else:
        return render_template('update.html',task=task_update)


@app.route('/delete/',methods=['GET'])
def deleterest():
    print("this is new",file=sys.stderr)
    id = request.args.get('id')
    print(id,file=sys.stderr)
    task_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/')
    except:
        return redirect('There was a problem deleting that task')



if __name__ == "__main__":
    app.run(debug=True)
    #app.run(debug=True)
