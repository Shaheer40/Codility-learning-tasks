from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ✅ Database Configuration
# (Remember: %40 = @ symbol in your password)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:aabb%401122@localhost/mini_facebook_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    bio = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'bio': self.bio
        }

# ✅ Create tables (if not exist)
with app.app_context():
    db.create_all()


# ------------------------- #
#         ROUTES            #
# ------------------------- #

@app.route('/')
def home():
    return "Mini Facebook API is running 🚀"


# 1️⃣ Create User
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and Email are required'}), 400

    user = User(name=data['name'], email=data['email'], bio=data.get('bio', ''))
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', 'user': user.to_dict()}), 201


# 2️⃣ Edit User
@app.route('/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.bio = data.get('bio', user.bio)
    db.session.commit()

    return jsonify({'message': 'User updated successfully', 'user': user.to_dict()})


# 3️⃣ Get User by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())


# 4️⃣ Get All Users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


# 5️⃣ Delete User
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})


# ------------------------- #
#        POSTS MODULE        #
# ------------------------- #

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content
        }

# ✅ Create table if not exists
with app.app_context():
    db.create_all()


# 2.1️⃣ Create Post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    user_id = data.get('user_id')
    title = data.get('title')
    content = data.get('content')

    if not user_id or not title or not content:
        return jsonify({'error': 'user_id, title, and content are required'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    post = Post(user_id=user_id, title=title, content=content)
    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully', 'post': post.to_dict()}), 201


# 2.2️⃣ Edit Post
@app.route('/posts/<int:post_id>', methods=['PUT'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    db.session.commit()

    return jsonify({'message': 'Post updated successfully', 'post': post.to_dict()})


# 2.3️⃣ Delete Post
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'})


# 2.4️⃣ Get All Posts
@app.route('/posts', methods=['GET'])
def get_all_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])


# 2.5️⃣ Get Post by ID
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post_by_id(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    return jsonify(post.to_dict())


# 2.6️⃣ Get Posts by User ID
@app.route('/users/<int:user_id>/posts', methods=['GET'])
def get_posts_by_user(user_id):
    posts = Post.query.filter_by(user_id=user_id).all()
    return jsonify([p.to_dict() for p in posts])




# ✅ Run App
if __name__ == '__main__':
    app.run(debug=True)
