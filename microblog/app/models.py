from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
from sqlalchemy import Index

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

promotion_products = db.Table(
    'promotion_products',
    db.Column('promotion_id', db.Integer, db.ForeignKey('promotion.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)

Index('promo_items', promotion_products.c.promotion_id, promotion_products.c.product_id, unique=True)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithm=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(500))
    endpoint = db.Column(db.String(500))
    products = db.relationship('Product',
                               secondary=promotion_products,
                               backref=db.backref('promotion', lazy='dynamic'))

    def __repr__(self):
        return "{{ url_for('{}') }}".format(self.endpoint)


class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.String(140))
    url = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Feature {}>'.format(self.title)


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(50), unique=True, index=True)
    districts = db.relationship('District', backref='region', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.region)


class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    district = db.Column(db.String(50), unique=True, index=True)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    stores = db.relationship('Store', backref='district', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.district)


class CompanyBrand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companybrand = db.Column(db.String(50), unique=True, index=True)
    photourl = db.Column(db.String(500))
    stores = db.relationship('Store', backref='companybrand', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.companybrand)


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store = db.Column(db.String(500), unique=True, index=True)
    address = db.Column(db.String(500))
    tel = db.Column(db.String(500))
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
    companybrand_id = db.Column(db.Integer, db.ForeignKey('company_brand.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Store {}>'.format(self.store)


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categories = db.Column(db.String(500), unique=True, index=True)
    sub_categoriess = db.relationship('SubCategories', backref='categories', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.categories)


class SubCategories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subcategories = db.Column(db.String(500), unique=True, index=True)
    categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    products = db.relationship('Product', backref='subcategories', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.subcategories)


class ProductBrand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productbrand = db.Column(db.String(500), unique=True, index=True)
    imgurl = db.Column(db.String(500))
    products = db.relationship('Product', backref='productbrand', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.productbrand)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(500))
    volumn = db.Column(db.String(500))
    price = db.Column(db.String(500))
    pricedown = db.Column(db.String(500))
    details = db.Column(db.String(500))
    origin = db.Column(db.String(500))
    productimage = db.Column(db.String(500))
    categories_id = db.Column(db.Integer, db.ForeignKey('sub_categories.id'))
    productbrand_id = db.Column(db.Integer, db.ForeignKey('product_brand.id'))
    reviews = db.relationship('Review', backref='product', lazy='dynamic')
    promotions = db.relationship('Promotion',
                                 secondary=promotion_products,
                                 backref=db.backref('product', lazy='dynamic'))


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating1 = db.Column(db.Float)
    rating2 = db.Column(db.Float)
    rating3 = db.Column(db.Float)
    rating4 = db.Column(db.Float)
    comment = db.Column(db.Text)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class Banner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    banner = db.Column(db.String(500))

    def __repr__(self):
        return '{}'.format(self.banner)
