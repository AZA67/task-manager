from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key" 

#db config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

#db models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Add hash method for passwords before save
    def set_password(self, password):
        self.password = generate_password_hash(password)

    #check hashed password during login
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#Home page Route
@app.route("/")
def home():
    return render_template("home.html")

#User regisration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "please enter both username and password"

        #check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists, choose another"
        
        #add hashed password
        hashed_password = generate_password_hash(password)

        # Save new user
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '''
            <h2>your registered!</h2>
            <br>
            <a href="/login" class="btn btn-primary">login</a>"
        '''
        pass

    return render_template("register.html")

# User Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            print("user logged in, session user_id:", session.get("user_id"))
            session["username"] = user.username
            return redirect("/dashboard")
        else:
            return "Invalid username or password"
        
        pass

    return render_template("login.html")

# Task Dashboard
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        print("You aren't logged in, redirecting to login")
        return redirect("/login")
    
    user_id = session["user_id"]
    tasks = Task.query.filter_by(user_id=user_id).all()

    #task_list = "<br>".join([f"{task.id}. {task.description}" for task in tasks])

    return render_template("dashboard.html", username=session["username"], tasks=tasks)


# add tasks
@app.route("/add_task", methods=["POST"])
def add_task():
    if "user_id" not in session:
        return redirect("/login")

    description = request.form.get("description")
    new_task = Task(description=description, user_id=session["user_id"])
    db.session.add(new_task)
    db.session.commit()

    return redirect("/dashboard")

#delete task
@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    if "user_id" not in session:
        return redirect("/login")
    
    task = Task.query.filter_by(id=task_id, user_id=session["user_id"]).first()

    if task:
        db.session.delete(task)
        db.session.commit()

    return redirect("/dashboard")

# logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)