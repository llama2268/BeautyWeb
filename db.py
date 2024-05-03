from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# your classes here

reviews_from_user_table = db.Table(
    "review_association",
    db.Model.metadata,
    db.Column("review_id",db.Integer,db.ForeignKey("review.id")),
    db.Column("user_id",db.Integer,db.ForeignKey("user.id"))
)
reviews_for_user_table = db.Table(
    "reviews_user_association",
    db.Model.metadata,
    db.Column("review_id",db.Integer,db.ForeignKey("review.id")),
    db.Column("user_id",db.Integer,db.ForeignKey("user.id"))
)

class Post(db.Model):
    """
    Post model
    """
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    image_path = db.Column(db.String, nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates = "posts")
    comments = db.relationship("Comment", back_populates = "comments")

    def __init__(self, **kwargs):
        """
        Initialize a post object
        """
        self.title = kwargs.get("title", "")
        self.description = kwargs.get("description", "")
        self.image_path = kwargs.get("image_path", "")
        self.user_id = kwargs.get("user_id", "")
    
    def serialize(self):
        """
        Serialize a post object
        """
        return {
            "id":self.id,
            "title":self.title,
            "description":self.description,
            "image_path":self.image_path,
            "user_id":self.user_id,
            "user":[u.simple_serialize() for u in self.user],
            "comments":[c.simple_post_serialize() for c in self.comments]

        }
    
    def new_serialize(self):
        """
        Serialize a new post object with no comments
        """
        return {
            "id":self.id,
            "title":self.title,
            "description":self.description,
            "image_path":self.image_path,
            "user_id":self.user_id,
            "user":[u.simple_serialize() for u in self.user],
            "comments":[]

        }
    
    def simple_serialize(self):
        """
        Simply serialize a post object
        """
        return {
            "id":self.id,
            "title":self.title,
            "description":self.description,
            "image_path":self.image_path,
            "user_id":self.user_id,
        }

class Comment(db.Model):
    """
    Comment model
    """
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    description = db.Column(db.String, nullable = False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", back_populates = "comments")
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    post = db.relationship("Post", back_populates = "comments")

    def __init__(self, **kwargs):
        """
        Initialize a comment object
        """
        self.description = kwargs.get("description", "")
        self.author_id = kwargs.get("author_id", "")
        self.post_id = kwargs.get("post_id", "")

    def serialize(self):
        """
        Serialize comment object
        """
        return {
            "id":self.id,
            "description":self.description,
            "author_id":self.author_id,
            "author":[u.simple_serialize() for u in self.author],
            "post_id":self.post_id,
            "post":[p.simple_serialize() for p in self.post]
        }
    
    def simple_post_serialize(self):
        """
        Simply serialize a comment object (no posts to start loop)
        """
        return {
            "id":self.id,
            "description":self.description,
            "author_id":self.author_id,
            "author":[u.simple_serialize() for u in self.author],
        }
    
    def simple_user_serialize(self):
        """
        Simply serialize a comment object (no users to start loop)
        """
        return {
            "id":self.id,
            "description":self.description,
            "user_id":self.author_id,
            "post_id":self.post_id,
            "post":[p.simple_serialize() for p in self.post]
        }
    



class User(db.Model):
    """
    User model
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String, nullable = False)
    bio = db.Column(db.String,nullable = False)
    contacts = db.Column(db.String,nullable = False)
    reviews_written_by_user = db.relationship("Review",secondary = reviews_from_user_table,back_populates = "users_reviews")
    reviews_written_for_user = db.relationship("Review",secondary = reviews_for_user_table,back_populates = "users_reviews_receive")
    posts = db.relationship("Post", back_populates = "user")
    comments = db.relationship("Comment", back_populates = "user")
    
    def __init__(self, **kwargs):
        """
        Initialize a user object
        """
        self.username = kwargs.get("username","")
        self.bio = kwargs.get("bio","")
        self.contacts = kwargs.get("contacts","")
    
    def serialize(self):
        """
        Serialize User object with reviews
        """
        return {
            "id":self.id,
            "username":self.username,
            "bio":self.bio,
            "contacts":self.contacts,
            "reviews":[r.simple_serialize() for r in self.reviews_written_by_user],
            "received_reviews":[a.simple_serialize() for a in self.reviews_written_for_user],
            "posts":[p.simple_serialize() for p in self.posts],
            "comments":[c.simple_user_serialize() for c in self.comments] 
        }
        
    
    def simple_serialize(self):
        """
        Serialize User object for a newly created user with no reviews
        """
        return {
            "id":self.id,
            "username":self.username,
            "bio":self.bio,
            "contacts":self.contacts

        }





class Review(db.Model):
    "Creates the Reviews Model"
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    sender_id = db.Column(db.Integer, nullable = False)
    receiver_id = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String, nullable = False)
    users_reviews= db.relationship("User",secondary=reviews_from_user_table,back_populates = "reviews_written_by_user")
    users_reviews_receive = db.relationship("User",secondary = reviews_for_user_table,back_populates = "reviews_written_for_user")
    
    def __init__(self, **kwargs):
        """
        Initialize a user object
        """
        self.sender_id = kwargs.get("sender_id","")
        self.receiver_id = kwargs.get("receiver_id","")
        self.description = kwargs.get("description","")

    def serialize(self):
        """
        Serialize review object with the user
        """
        return {
            "id":self.id,
            "users":[u.serialize() for u in self.users_reviews],
            "description":self.description,
        }
    
    def simple_serialize(self):
        """
        Serialize review object without the user
        """
        return {
            "id":self.id,
            "sender_id":self.sender_id,
            "receiver_id":self.receiver_id,
            "description":self.description
        }


