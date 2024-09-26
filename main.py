from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///true-publish-protocol.db'
db = SQLAlchemy(app)


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)


@app.route('/')
def posts():
    posts = Post.query.all()

    return render_template('posts.html', posts=posts)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        post = Post(title=title, text=text)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error adding the article'

    else:
        return render_template('create.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
