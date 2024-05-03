from db import db
from flask import Flask, request
from flask import json
from db import User, Review, Post, Comment

app = Flask(__name__)
db_filename = "ithacuts.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["UPLOAD_FOLDER"] = 'uploads'

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
        return failure_response("Username already exists")
    if username2 is None:
        return failure_response("Missing username")
    if bio2 is None:
        return failure_response("Missing bio")
    if contacts2 is None:
        return failure_response("Missing contact")
    new_user = User(username = username2,bio=bio2,contacts=contacts2)

    if new_user is None:
        return failure_response("Invalid user")
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
        return failure_response("Course not found", 404)
    return success_response(user.serialize())

@app.route("/api/users/<int:user_id>/",methods = ["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting a course by id
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("Course not found", 404)
    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize())

@app.route("/api/users/reviews/",methods = ["POST"])
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
        return failure_response("Missing description")
    if body.get("sender_id") is None:
        return failure_response("User not found", 404)
    new_review = Review(
        sender_id = the_sender_id,
        receiver_id = the_receiver_id,
        description = description2
    )
    if receiver is None:
        return failure_response("Receiver not found", 404)
    if new_review is None:
        return failure_response("Review not made")
    sender.reviews_written_by_user.append(new_review)
    receiver.reviews_written_for_user.append(new_review)
    db.session.add(new_review)
    db.session.commit()
    return success_response(new_review.simple_serialize(),201)

@app.route("/api/users/reviews/<int:review_id>/")
def get_review(review_id):
    """
    Endpoint for getting a specific user
    """
    review = Review.query.filter_by(id=review_id).first()
    if review is None:
        return failure_response("Review not found", 404)
    return success_response(review.simple_serialize())


@app.route("/api/users/<int:user_id>/reviews/<int:review_id>/", methods = ["DELETE"])
def delete_review(review_id):
    """
    Endpoint for getting a specific user
    """
    review = Review.query.filter_by(id=review_id).first()
    if review is None:
        return failure_response("Review not found", 404)
    db.session.delete(review)
    db.session.commit()
    return success_response(review.simple_serialize())


#posts
@app.route("/api/users/<int:user_id>/posts/", methods=["POST"])
def create_post(user_id):
    """
    Endpoint for creating a post by a user
    """
    body = json.loads(request.data)
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return failure_response("User not found", 404)
    title = body.get("title")
    description = body.get("description")
    image_path = body.get("image_path")

    
    new_post = Post(
        title = title,
        description = description,
        image_path = image_path,
        user_id = user_id
    )
    db.session.add(new_post)
    db.session.commit()
    return success_response(new_post.new_serialize())

@app.route("/api/users/<int:user_id>/posts/<int:post_id>/")
def get_post(user_id,post_id):
    """
    Endpoint for getting a specific post by a user
    """
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return failure_response("User not found",404)
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return failure_response("Post not found", 404)
    #if there are no comments under the post, return an empty list for 
    #comments instead
    return success_response(post.serialize())

    try:
        return success_response(post.serialize())
    except:
        return success_response(post.new_serialize())
    
@app.route("/api/users/<int:user_id>/posts/<int:post_id>/", methods=["POST"])
def update_post(user_id,post_id):
    body = json.loads(request.data)
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return failure_response("User not found",404)
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return failure_response("Post not found", 404)
    post.title = body.get("title", post.title)
    post.description = body.get("description", post.description)
    post.image_path = body.get("image_path", post.image_path)

    db.session.commit()
    try:
        return success_response(post.serialize())
    except:
        return success_response(post.new_serialize())

@app.route("/api/users/<int:user_id>/posts/<int:post_id>/", methods = ["DELETE"])
def delete_post(user_id,post_id):
    """
    Endpoint for getting a specific user
    """
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return failure_response("User not found")
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return failure_response("Post not found")
    db.session.delete(post)
    db.session.commit()
    
    try:
        return success_response(post.serialize())
    except:
        return success_response(post.new_serialize())
    
#comments
@app.route("/api/users/<int:user_id>/posts/<int:post_id>/comments/", methods=["POST"])
def create_comment(user_id,post_id):
    """
    Endpoint for creating a comment
    """
    body = json.loads(request.data)
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return failure_response("User not found", 404)
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return failure_response("Post not found", 404)
    description = body.get("description")
    author_id = body.get("author_id")
    if author_id is None:
        return failure_response("Author not provided")
    if description is None:
        return failure_response("Description not provided")
    new_comment = Comment(
        description = description,
        author_id = author_id,
        post_id = post_id
    )
    db.session.add(new_comment)
    db.session.commit()
    return success_response(new_comment.simple_post_serialize())

@app.route("/api/users/<int:user_id>/posts/<int:post_id>/comments/<int:comment_id>/")
def get_comment(user_id,post_id,comment_id):
    """
    Endpoint for getting a specific comment by a user
    """
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return failure_response("User not found",404)
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return failure_response("Post not found", 404)
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        return failure_response("Comment not found", 404)
    
    return success_response(comment.simple_post_serialize())

@app.route("/api/users/<int:user_id>/posts/<int:post_id>/comments/<int:comment_id>/", methods=["POST"])
def update_comment(user_id,post_id,comment_id):
    """
    Endpoint for updating a specific comment by a user
    """
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return failure_response("User not found",404)
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return failure_response("Post not found", 404)
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        return failure_response("Comment not found", 404)

    body = json.loads(request.data)
    comment.description = body.get("description", comment.description)

    db.session.commit()
    return success_response(comment.simple_post_serialize())

@app.route("/api/users/<int:user_id>/posts/<int:post_id>/comments/<int:comment_id>/", methods=["DELETE"])
def delete_comment(user_id,post_id,comment_id):
    """
    Endpoint for deleting a specific comment by a user
    """
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return failure_response("User not found",404)
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return failure_response("Post not found", 404)
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        return failure_response("Comment not found", 404)
    
    db.session.delete(comment)
    db.session.commit()
    return success_response(comment.simple_post_serialize())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
