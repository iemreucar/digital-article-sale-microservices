from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from models import Article, Sales, Base
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


@app.route('/search_article', methods=['POST'])
def search_article():

    params = request.form
    print(params)
    name = params.get("name")
    year = params.get("year")   
    author = params.get("author")

    db = next(get_db())
    query = db.query(Article)

    if name:
        query = query.filter(Article.name.ilike(f"%{name}%"))
    if year:
        query = query.filter(Article.year == year)
    if author:
        query = query.filter(Article.author.ilike(f"%{author}%"))
    
    result = query.all()
    articles=[]
    for article in result:
        items={"id": article.id,"name": article.name, "year": article.year, "author": article.author}
        articles.append(items)

    return jsonify(articles), 200
    


@app.route('/select_article', methods=['POST'])
def select_article():
    article_id = request.form.get('article_id')
    app.logger.info(request.form.get(article_id))   
    app.logger.info(request.form)
    db = next(get_db())
    selected_article = db.query(Article).filter(Article.id == article_id).first()
    app.logger.info(type(article_id))
    app.logger.info(selected_article)

    if selected_article:
        article_data = {
            "id": selected_article.id,
            "name": selected_article.name,
            "year": selected_article.year,
            "author": selected_article.author,
            "price": selected_article.price
        }
        return jsonify(article_data), 200
    else:
        return jsonify({"error": "Article not found"}), 404

    

@app.route('/place_order', methods=['POST'])
def place_order():
    article_id = request.form.get('article_id')
    user_id = request.form.get('user_id')

    db = next(get_db())
    article = db.query(Article).filter(Article.id == article_id).first()

    if article:
        total_price = float(article.price)

        sale = Sales(
            article_id=article_id,
            user_id=user_id
        )
        try:
            db.add(sale)
            db.commit()
            message = f"Order placed successfully for '{article.name}'. Total price: {total_price:.2f}"
            return jsonify({"success": True, "message": message}), 201
        except Exception as e:
            db.rollback()
            return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500
    else:
        return jsonify({"success": False, "message": "Article not found"}), 404


if __name__=="__main__":
    app.run(debug=True)
