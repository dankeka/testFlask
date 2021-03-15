from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager

a = "a"
db = SQLAlchemy()
login_manager = LoginManager()


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(16), nullable=False)
    password = db.Column(db.Unicode(100), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    articles = db.relationship('Article', backref='author_article')
    comments = db.relationship('Comment', backref='author_comment')

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def __repr__(self):
        return str(self.name)


@login_manager.user_loader
def user_loader(user_id):
    user = db.session.query(User).get(user_id)
    return user


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='article_link')

    def __repr__(self):
        return str(self.title)


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return str(self.id)

# RenderComment - тот же Comment, только не для db
# вместо user_id user_name


class RenderComment:
    def __init__(self, id, article_id, username, text, date):
        self.id = id
        self.article_id = article_id
        self.username = username
        self.text = text
        self.date = date
