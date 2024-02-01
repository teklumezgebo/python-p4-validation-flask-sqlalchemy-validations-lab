from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def name_present(self, key, name):
        if len(name) == 0:
            raise ValueError("Name must be present")
        elif Author.query.filter_by(name=name).first():
            raise ValueError("Name already exists")
        return name
    
    @validates('phone_number')
    def phone_number_length(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError("Phone number must be 10 digits long")
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def content_length(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters long")
    
    @validates('summary')
    def summary_length(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary must be less than 250 characters")
    
    @validates('category')
    def category_type(self, key, category):
        if category != 'Fiction' or category != 'Non-Fiction':
            raise ValueError("Category must be Fiction or Non-Fiction")
        
    @validates('title')
    def title_sufficiency(self, key, title):
        if ("Won't Believe" or "Secret" or "Top" or "Guess") not in title:
            raise ValueError("Title not sufficiently clickbait-y")
    
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
