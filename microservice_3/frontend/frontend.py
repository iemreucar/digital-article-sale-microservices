from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
import requests

app=Flask(__name__)

@app.route('/')
def navigation():
    return render_template('navigation.html')

@app.route('/register_get')
def register_page():
    return render_template("register.html")

@app.route('/add_article_get')
def add_article_page():
    return render_template("add_article.html")

@app.route('/search_article_get')
def search_article_page():
    return render_template('search_article.html')

@app.route('/register',methods=['POST'])
def call1():
    response=requests.post("http://user:5002/register",data=request.form)
    message=response
    return render_template('register.html', message=message)

@app.route('/add_article',methods=['POST'])
def call2():
    response=requests.post("http://user:5002/add_article",data=request.form)
    message=response.text
    return render_template('add_article.html',message=message)

@app.route('/search_article', methods=['POST'])
def call3():
    response = requests.post("http://customer:5001/search_article", data=request.form)
    app.logger.info(response)
    articles = response.json()
    app.logger.info(articles)
    if articles:
        return render_template("search_results.html", articles=articles)
    return render_template("search_results.html", error="No articles found.")


@app.route('/select_article', methods=['POST'])
def call4():
    response = requests.post("http://customer:5001/select_article", data=request.form)
    app.logger.info(response)
    article = response.json()
    app.logger.info(article)
    if article:
        return render_template("order_article.html", article=article)
    return render_template('search_article.html',error= "Article not found")


@app.route('/place_order', methods=['POST'])
def call5():
    response = requests.post("http://customer:5001/place_order", data=request.form)
    response_data = response.json()
    message = response_data.get("message", "Order failed")
    return render_template("order_confirmation.html", message=message)


if __name__=="__main__":
    app.run(debug=True,port=5000)
