from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from models import User, Article, Base
from sqlalchemy.sql import func

DATABASE_URL = "sqlite:///./test.db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = Flask(__name__)
bcrypt = Bcrypt(app)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.route('/register', methods=['POST'])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    next_user = User(email=email, password=hashed_password)

    db = next(get_db())
    try:
        db.add(next_user)
        db.commit()
        return "User registered successfully", 201
    except IntegrityError:
        db.rollback()
        return "Email already exists or incorrect email", 400
    finally:
        db.close()



@app.route('/add_article', methods=['POST'])
def add_article():
    name = request.form.get("name")
    year = request.form.get("year")
    author = request.form.get("author")
    price = request.form.get("price")
    next_article = Article(name=name, year=year, author=author, price=price)

    db = next(get_db())
    try:
        db.add(next_article)
        db.commit()
        return "Article has been added successfully",201
    except IntegrityError:
        db.rollback()
        return "An article with this name already exists",400
    finally:
        db.close()


if __name__=="__main__":
    app.run(debug=True)
