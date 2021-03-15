#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, make_response, jsonify
from flask import json as flaskJSON
from sqlalchemy import desc
from flask_migrate import Migrate
import models as mod
from models import db
from forms import csrf, RegisterForm, LoginForm, AddArticleForm, AddCommentForm
from flask_login import current_user, login_user, login_required, logout_user
from flask_cors import CORS
from datetime import datetime
import copy 

app = Flask(__name__)
CORS(app)

SECRET_KEY: bytes = "Dvso3bdMiueD31fdw0eb9hPgid43sgs3".encode()
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'

db.init_app(app)
migrate = Migrate(app, db)

csrf.init_app(app)
mod.login_manager.init_app(app)

# with app.app_context():
#   db.create_all()

@app.route('/')
def index():
  auth = current_user.is_authenticated
  try:
    articles = db.session.query(mod.Article).order_by(desc(mod.Article.date)).all()
    for a in articles:
      a.date = a.date.strftime("%d/%m/%Y")
  except:
    return render_template('index.html', auth=auth, articles=False)
  
  return render_template('index.html', auth=auth, articles=articles)

@app.route('/register/', methods=["GET"])
def register():
  auth = current_user.is_authenticated
  form = RegisterForm()
  return render_template('register.html', form=form, auth=auth)
  
@app.route('/registerPOST/', methods=["POST"])
def registerPOST():
  newUser = mod.User(
    name = request.form["username"],
    password = request.form["password2"],
  )
  print(newUser.name, newUser.password)
  
  try:
    db.session.add(newUser)
    db.session.commit()
    return redirect("/login/", code=302)
  except:
    return "ERROR 404 =((("
 
@app.route('/login/') 
def login():
  form = LoginForm()
  auth = current_user.is_authenticated
  return render_template("login.html", form=form, auth=auth)
  
@app.route('/loginPOST/', methods=["POST"]) 
def loginPOST():
  try:
    username = request.form["username"]
    password = request.form["password"]
    
    user_id = db.session.query(mod.User.id).filter(
      mod.User.name == username
      and
      mod.User.password == password
    ).first()
    
    
    user = mod.user_loader(user_id[0])
    login_user(user)
    return redirect("/")
  except:
    return "ERROR 404 =(((("
  
@app.route("/logout/")
@login_required
def logout():
  logout_user()
  return redirect("/")

@app.route("/addArticleForm/")
def addArticleForm():
  if current_user.is_authenticated:
    form = AddArticleForm()
    return render_template("addArticle.html", form=form, auth=True, user=current_user.name)
  else:
    return redirect("/login/")
  
@app.route("/addArticlePOST/", methods=["POST"])
def addArticlePost():
  checkUser = request.form["username"]
  print(checkUser, current_user.name)
  if current_user.name == checkUser:
    articleTitle = request.form["title"]
    articleText = request.form["text"]
    articleIntro = request.form["intro"]
    
    newArticle: mod.Article = mod.Article(
      title = articleTitle,
      text = articleText,
      intro = articleIntro,
      date = datetime.utcnow()
    )
    try:
      db.session.add(newArticle)
      db.session.commit()
      return redirect("/")
    except:
      return "ERROR =((("
  else:
    return "ERROR =((("
  
@app.route("/article/<int:id>/")
def article(id):
  if True:
    article_sql = db.session.query(mod.Article).filter(mod.Article.id==id).first()
    article = copy.copy(article_sql)
    article.date = article.date.strftime("%d/%m/%Y %H:%M")
    
    form = AddCommentForm()
    auth = current_user.is_authenticated
    if auth:
      userID = current_user.id
      
    comments_sql = db.session.query(
      mod.Comment
    ).filter(
      mod.Comment.article_id==id
    ).order_by(
      desc(mod.Comment.date)
    ).all()
    
    comments = []
    
    if comments_sql:
      for c in comments_sql:
        date = c.date.strftime("%d/%m/%Y %H:%M")
        username = db.session.query(mod.User.name).filter(
          mod.User.id == c.user_id
        ).first()
        
        if not username:
          username = ("<em style=\"color: #333;\">аноним</em>", True)
          
          comment = mod.RenderComment(
            id = c.id,
            article_id = c.article_id,
            username = username,
            text = c.text,
            date = date
          )
        else:
          comment = mod.RenderComment(
            id = c.id,
            article_id = c.article_id,
            username = (username[0], False),
            text = c.text,
            date = date
          )
          
        comments.append(comment)
      
    return render_template("article.html", article=article, auth=auth, userID=userID, form=form, comments=comments)
  # except:
  #   return "ERROR 404"
  
@app.route("/addComment/", methods=["POST"])
def addComment():
  try:
    userID = request.form["userID"]
    
    assert userID == str(current_user.id)
    
    commentText = request.form["commentText"]
    articleID = request.form["articleID"]
    
    newComment = mod.Comment(
      text=commentText,
      article_id=articleID,
      user_id=userID
    )
    
    db.session.add(newComment)
    
    for c in db.session.query(mod.Comment).all():
      print(c)
      
    db.session.commit()
    
    return ('', 204) # ('', 204) = 204 No Content
  except:
    return "ERROR =((("


if __name__ == '__main__':
  app.run(debug=True)