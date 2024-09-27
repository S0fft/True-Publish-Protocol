from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask('True-Publish-Protocol')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///true-publish-protocol.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)


class ArticleModel(db.Model):
    __tablename__ = 'articles'

    ar_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {'id': self.ar_id, 'title': self.title, 'text': self.text}


class Article(Resource):
    def get(self, article_id=None):
        if article_id:
            article = ArticleModel.query.get(article_id)

            if article:
                return article.to_dict(), 200
            return {'message': 'Article not found!'}, 404

        articles = ArticleModel.query.all()

        return [article.to_dict() for article in articles], 200

    def post(self):
        args = request.get_json()

        if not args or 'title' not in args or 'text' not in args:
            return {'message': 'Title and text are required'}, 400

        new_article = ArticleModel(title=args['title'], text=args['text'])
        db.session.add(new_article)
        db.session.commit()

        return new_article.to_dict(), 201

    def put(self, article_id=None):
        if article_id is None:
            return {'message': 'Article ID is required'}, 400

        article = ArticleModel.query.get(article_id)

        if not article:
            return {'message': 'Article not found!'}, 404

        args = request.get_json()

        if not args or 'title' not in args or 'text' not in args:
            return {'message': 'Title and text are required'}, 400

        article.title = args['title']
        article.text = args['text']
        db.session.commit()

        return article.to_dict(), 200

    def patch(self, article_id=None):
        if article_id is None:
            return {'message': 'Article ID is required'}, 400

        article = ArticleModel.query.get(article_id)

        if not article:
            return {'message': 'Article not found!'}, 404

        args = request.get_json()

        if 'title' in args:
            article.title = args['title']

        if 'text' in args:
            article.text = args['text']

        db.session.commit()

        return article.to_dict(), 200

    def delete(self, article_id=None):
        article = ArticleModel.query.get(article_id)

        if not article:
            return {'message': 'Article not found!'}, 404

        db.session.delete(article)
        db.session.commit()

        return {'message': f'Article {article_id} has been removed'}, 204


api.add_resource(Article, '/articles/', endpoint='article_list')
api.add_resource(Article, '/articles/<int:article_id>/', endpoint='article_detail')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
