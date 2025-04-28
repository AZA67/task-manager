from app import db, User, app

#Queries user+password from db
with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"Username: {user.username}, Password: {user.password}")
    
