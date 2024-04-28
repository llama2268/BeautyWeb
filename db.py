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
            "received_reviews":[a.simple_serialize() for a in self.reviews_written_for_user]
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


