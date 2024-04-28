from db import db
from flask import Flask, request
from flask import json
from db import User, Review

app = Flask(__name__)
db_filename = "ithacuts.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data,code=200):
    return json.dumps(data), code

def failure_response(message,code = 404):
    return json.dumps({"error":message}),code


# your routes here

@app.route("/api/users/")
def get_all_users():
    """
    Endpoint for getting all courses
    """
    user = [user.serialize() for user in User.query.all()]
    return success_response({"Users":user})

@app.route("/api/users/", methods = ["POST"])
def create_user():
    """
    Endpoint for creating a course
    """
    body = json.loads(request.data)
    username2 = body.get("username")
    bio2 = body.get("bio")
    contacts2 = body.get("contacts")
    checkusername = User.query.filter_by(username = username2).first()
    if checkusername is not None:
        return json.dumps({"error":"Username already exists"}), 400
    if username2 is None:
        return json.dumps({"error":"Missing Username"}),400
    if bio2 is None:
        return json.dumps({"error":"Missing Bio"}),400
    if contacts2 is None:
        return json.dumps({"error":"Missing contacts"})
    new_user = User(username = username2,bio=bio2,contacts=contacts2)

    if new_user is None:
        return failure_response("Invalid code and name for course")
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for geting a course by id
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("Course not found")
    return success_response(user.serialize())

@app.route("/api/users/<int:user_id>/",methods = ["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting a course by id
    """
    user = User.query.filter_by(id=user_id).first()
    if User is None:
        return failure_response("Course not found")
    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize())

@app.route("/api/reviews/",methods = ["POST"])
def create_review():
    """
    Endpoint for creating a user
    """
    body = json.loads(request.data)
    the_sender_id = body.get("sender_id")
    the_receiver_id = body.get("receiver_id")
    description2 = body.get("description")
    sender = User.query.filter_by(id = the_sender_id).first()
    receiver = User.query.filter_by(id = the_receiver_id).first()
    if body.get("description") is None:
        return json.dumps({"error":"Missing Description"}),400
    if body.get("sender_id") is None:
        return json.dumps({"error":"User not found"}),400
    new_review = Review(
        sender_id = the_sender_id,
        receiver_id = the_receiver_id,
        description = description2
    )
    if receiver is None:
        return failure_response("Receiver not found"),400
    if new_review is None:
        return failure_response("Review not made"),400
    sender.reviews_written_by_user.append(new_review)
    receiver.reviews_written_for_user.append(new_review)
    db.session.add(new_review)
    db.session.commit()
    return success_response(new_review.simple_serialize(),201)

@app.route("/api/review/<int:review_id>/")
def get_review(review_id):
    """
    Endpoint for getting a specific user
    """
    review = Review.query.filter_by(id=review_id).first()
    if review is None:
        return failure_response("Review not found")
    return success_response(review.simple_serialize())


@app.route("/api/review/<int:review_id>/", methods = ["DELETE"])
def delete_review(review_id):
    """
    Endpoint for getting a specific user
    """
    review = Review.query.filter_by(id=review_id).first()
    if review is None:
        return failure_response("Review not found"),400
    db.session.delete(review)
    db.session.commit()
    return success_response(review.simple_serialize())

    




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
