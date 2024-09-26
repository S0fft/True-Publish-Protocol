from flask import Flask
from flask_restful import Api, Resource

app = Flask('True-Publish-Protocol')
api = Api(app)

articles = {
    'article1': {
        'title': 'Hello World on Python',
        'text': 'Lorem Lorem Lorem'
    },
    'article2': {
        'title': 'Hello World on Python 2',
        'text': 'Lorem  Lorem Lorem'
    }
}


class Article(Resource):
    def get(self):
        return articles


api.add_resource(Article, '/')


if __name__ == '__main__':
    app.run()
