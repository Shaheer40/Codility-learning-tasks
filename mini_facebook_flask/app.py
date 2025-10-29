from flask import Flask, request, jsonify, render_template
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



# ------------------------- #
#    COMMENTS / LIKES /     #
#        FRIENDS MODULE     #
# ------------------------- #

# ---------- MODELS ----------

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    post = db.relationship('Post', backref=db.backref('comments', lazy=True, cascade="all, delete-orphan"))

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='_post_user_like_uc'),)

    user = db.relationship('User', backref=db.backref('likes', lazy=True))
    post = db.relationship('Post', backref=db.backref('likes', lazy=True, cascade="all, delete-orphan"))

    def to_dict(self):
        return {'id': self.id, 'post_id': self.post_id, 'user_id': self.user_id, 'created_at': self.created_at.isoformat()}


class FriendRequest(db.Model):
    __tablename__ = 'friend_requests'
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    __table_args__ = (db.UniqueConstraint('from_user_id', 'to_user_id', name='_unique_friend_request_uc'),)

    from_user = db.relationship('User', foreign_keys=[from_user_id], backref=db.backref('sent_requests', lazy=True))
    to_user = db.relationship('User', foreign_keys=[to_user_id], backref=db.backref('received_requests', lazy=True))

    def to_dict(self):
        return {'id': self.id, 'from_user_id': self.from_user_id, 'to_user_id': self.to_user_id, 'status': self.status, 'created_at': self.created_at.isoformat()}


class Friendship(db.Model):
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    __table_args__ = (db.UniqueConstraint('user_id', 'friend_id', name='_user_friend_uc'),)

    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('friend_rows', lazy=True))
    friend = db.relationship('User', foreign_keys=[friend_id])

    def to_dict(self):
        return {'id': self.id, 'user_id': self.user_id, 'friend_id': self.friend_id, 'created_at': self.created_at.isoformat()}


# ensure new tables exist
with app.app_context():
    db.create_all()


# ---------- COMMENTS ROUTES ----------

# 2.1 Add a comment on Post
@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    data = request.get_json() or {}
    user_id = data.get('user_id')
    content = data.get('content', '').strip()
    if not user_id or not content:
        return jsonify({'error': 'user_id and content are required'}), 400

    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    comment = Comment(post_id=post_id, user_id=user_id, content=content)
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment added', 'comment': comment.to_dict()}), 201


# 2.2 Edit comment on Post
@app.route('/comments/<int:comment_id>', methods=['PUT'])
def edit_comment(comment_id):
    data = request.get_json() or {}
    new_content = data.get('content', '').strip()
    user_id = data.get('user_id')
    if not user_id or not new_content:
        return jsonify({'error': 'user_id and content are required'}), 400

    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    if comment.user_id != user_id:
        return jsonify({'error': 'Only the comment author can edit the comment'}), 403

    comment.content = new_content
    db.session.commit()
    return jsonify({'message': 'Comment updated', 'comment': comment.to_dict()})


# 2.3 Delete a comment on Post
@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    data = request.get_json() or {}
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400

    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    # allow deletion by author or by post owner (optionally)
    post_owner_id = comment.post.user_id
    if comment.user_id != user_id and post_owner_id != user_id:
        return jsonify({'error': 'Only the comment author or post owner can delete the comment'}), 403

    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted'})


# 2.4 Get the post's comments
@app.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.asc()).all()
    return jsonify([c.to_dict() for c in comments])


# ---------- LIKES ROUTES ----------

# 3.1 Like a post
@app.route('/posts/<int:post_id>/likes', methods=['POST'])
def like_post(post_id):
    data = request.get_json() or {}
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400

    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    # prevent duplicate like (UniqueConstraint helps too)
    existing = Like.query.filter_by(post_id=post_id, user_id=user_id).first()
    if existing:
        return jsonify({'error': 'Already liked'}), 400

    like = Like(post_id=post_id, user_id=user_id)
    db.session.add(like)
    db.session.commit()
    return jsonify({'message': 'Post liked', 'like': like.to_dict()}), 201


# 3.2 Unlike a post
@app.route('/posts/<int:post_id>/likes', methods=['DELETE'])
def unlike_post(post_id):
    data = request.get_json() or {}
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400

    like = Like.query.filter_by(post_id=post_id, user_id=user_id).first()
    if not like:
        return jsonify({'error': 'Like not found'}), 404

    db.session.delete(like)
    db.session.commit()
    return jsonify({'message': 'Post unliked'})


# 3.3 Get like count on a post
@app.route('/posts/<int:post_id>/likes/count', methods=['GET'])
def get_like_count(post_id):
    count = Like.query.filter_by(post_id=post_id).count()
    return jsonify({'post_id': post_id, 'likes_count': count})


# optional: get list of users who liked a post
@app.route('/posts/<int:post_id>/likes', methods=['GET'])
def get_post_likes(post_id):
    likes = Like.query.filter_by(post_id=post_id).all()
    return jsonify([l.to_dict() for l in likes])


# ---------- FRIENDS ROUTES ----------

# 4.1 Send a friend request
@app.route('/friends/requests', methods=['POST'])
def send_friend_request():
    data = request.get_json() or {}
    from_user_id = data.get('from_user_id')
    to_user_id = data.get('to_user_id')
    if not from_user_id or not to_user_id:
        return jsonify({'error': 'from_user_id and to_user_id required'}), 400
    if from_user_id == to_user_id:
        return jsonify({'error': 'Cannot send friend request to yourself'}), 400

    # check users exist
    from_user = User.query.get(from_user_id)
    to_user = User.query.get(to_user_id)
    if not from_user or not to_user:
        return jsonify({'error': 'User(s) not found'}), 404

    # check if already friends
    existing_friendship = Friendship.query.filter_by(user_id=from_user_id, friend_id=to_user_id).first()
    if existing_friendship:
        return jsonify({'error': 'Already friends'}), 400

    # check if request exists (either direction)
    existing_request = FriendRequest.query.filter(
        ((FriendRequest.from_user_id == from_user_id) & (FriendRequest.to_user_id == to_user_id)) |
        ((FriendRequest.from_user_id == to_user_id) & (FriendRequest.to_user_id == from_user_id))
    ).first()
    if existing_request:
        return jsonify({'error': 'Friend request already exists'}), 400

    fr = FriendRequest(from_user_id=from_user_id, to_user_id=to_user_id)
    db.session.add(fr)
    db.session.commit()
    return jsonify({'message': 'Friend request sent', 'request': fr.to_dict()}), 201


# 4.2 Accept a friend request
@app.route('/friends/requests/<int:request_id>/accept', methods=['PUT'])
def accept_friend_request(request_id):
    fr = FriendRequest.query.get(request_id)
    if not fr:
        return jsonify({'error': 'Friend request not found'}), 404
    if fr.status != 'pending':
        return jsonify({'error': 'Friend request already handled'}), 400

    # create mutual friendships (two rows for quick queries)
    try:
        fr.status = 'accepted'
        f1 = Friendship(user_id=fr.from_user_id, friend_id=fr.to_user_id)
        f2 = Friendship(user_id=fr.to_user_id, friend_id=fr.from_user_id)
        db.session.add_all([f1, f2])
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Could not accept friend request', 'details': str(e)}), 500

    return jsonify({'message': 'Friend request accepted', 'request': fr.to_dict()})


# optional: reject friend request
@app.route('/friends/requests/<int:request_id>/reject', methods=['PUT'])
def reject_friend_request(request_id):
    fr = FriendRequest.query.get(request_id)
    if not fr:
        return jsonify({'error': 'Friend request not found'}), 404
    if fr.status != 'pending':
        return jsonify({'error': 'Friend request already handled'}), 400

    fr.status = 'rejected'
    db.session.commit()
    return jsonify({'message': 'Friend request rejected', 'request': fr.to_dict()})


# 4.3 Show friends list
@app.route('/users/<int:user_id>/friends', methods=['GET'])
def show_friends(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    # return friend objects (friend rows)
    rows = Friendship.query.filter_by(user_id=user_id).all()
    friends = []
    for r in rows:
        f = User.query.get(r.friend_id)
        if f:
            friends.append({'id': f.id, 'name': f.name, 'email': f.email, 'bio': f.bio})
    return jsonify({'user_id': user_id, 'friends': friends})


# 4.4 Unfriend
@app.route('/users/<int:user_id>/unfriend/<int:other_id>', methods=['DELETE'])
def unfriend(user_id, other_id):
    # remove both friendship rows
    f1 = Friendship.query.filter_by(user_id=user_id, friend_id=other_id).first()
    f2 = Friendship.query.filter_by(user_id=other_id, friend_id=user_id).first()
    if not f1 and not f2:
        return jsonify({'error': 'Friendship not found'}), 404
    if f1:
        db.session.delete(f1)
    if f2:
        db.session.delete(f2)
    db.session.commit()
    return jsonify({'message': 'Unfriended successfully'})


# (Optional) List pending friend requests for a user
@app.route('/users/<int:user_id>/friend-requests', methods=['GET'])
def list_friend_requests(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    incoming = FriendRequest.query.filter_by(to_user_id=user_id, status='pending').all()
    outgoing = FriendRequest.query.filter_by(from_user_id=user_id, status='pending').all()
    return jsonify({
        'incoming': [r.to_dict() for r in incoming],
        'outgoing': [r.to_dict() for r in outgoing]
    })



@app.route('/')
def home():
    return render_template('index.html')


# ✅ Run App
if __name__ == '__main__':
    app.run(debug=True)
