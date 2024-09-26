from flask import Flask, request
from flask_restful import Api, Resource, reqparse

app = Flask('True-Publish-Protocol')
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('text', required=True)

articles = {
    'article1': {
        'title': 'Hello World on Python',
        'text': 'Lorem Lorem Lorem'
    },
    'article2': {
        'title': 'Hello World on Python 2',
        'text': 'Lorem Lorem Lorem'
    }
}


class Article(Resource):
    def get(self, article_id=None):
        if article_id:
            if article_id in articles:
                return articles[article_id], 200
            return {"message": "Article not found!"}, 404

        return articles, 200

    def post(self):
        args = request.get_json()

        if not args or 'title' not in args or 'text' not in args:
            return {"message": "Title and text are required"}, 400

        new_id = f"article{len(articles) + 1}"
        new_article = {
            'title': args['title'],
            'text': args['text'],
        }
        articles[new_id] = new_article

        return {new_id: new_article}, 201

    def put(self, article_id=None):
        if article_id is None:
            return {"message": "Article ID is required"}, 400

        args = request.get_json()

        if not args or 'title' not in args or 'text' not in args:
            return {"message": "Title and text are required"}, 400

        new_article = {
            'title': args['title'],
            'text': args['text'],
        }
        articles[article_id] = new_article
        return {article_id: new_article}, 201

    def delete(self, article_id=None):
        if article_id is None or article_id not in articles:
            return {'message': 'Article not found!'}, 404

        del articles[article_id]

        return {'message': f'Article №{article_id} has been removed'}, 204


api.add_resource(Article, '/articles', endpoint='article_list')
api.add_resource(Article, '/articles/<string:article_id>', endpoint='article_detail')


if __name__ == '__main__':
    app.run(debug=True)
