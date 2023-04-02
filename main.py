from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Setting up app
app = Flask(__name__)

# Setting up sqlite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.init_app(app)

#Todo Database
class Todo(db.Model): # Defines item
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str: # Don't Touch
        return f"{self.sno} - {self.title}"

#Create db file (stores it in default 'instance folder')
with app.app_context():
    db.create_all()

@app.route("/", methods = ["GET", "POST"])
def hello_world():
    if request.method == "POST":
        print(request.form["title"])

        # Get data from html form
        title = request.form["title"]
        desc = request.form["desc"]

        # Add todo to db
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()

    # allTodo variable gives the list of todos. Send to html in `return render_temp`
    allTodos = Todo.query.all()

    return render_template("index.html", allTodos = allTodos)

# Func to delete a todo
@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first() # obtains the todo
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
