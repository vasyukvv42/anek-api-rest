from flask import Blueprint, request
from flask_restful import Api, Resource, abort
from sqlalchemy import func

from anek import models as models
from anek.models import db
from anek.schemas import aneks_schema, anek_schema

bp = Blueprint('api', __name__, url_prefix='/api')

errors = {
    'ValidationError': {
        'message': 'Validation failed.',
        'status': 400
    }
}

api = Api(bp, errors=errors)


@api.resource('/aneks/<int:anek_id>')
class Anek(Resource):

    def get(self, anek_id):
        anek = models.Anek.query.filter_by(id=anek_id).first_or_404()
        return anek_schema.jsonify(anek)

    def put(self, anek_id):
        if request.json is None:
            abort(400)

        anek_from_db = models.Anek.query.filter_by(id=anek_id).first_or_404()
        anek = anek_schema.load(request.json, session=db.session, instance=anek_from_db, partial=True)

        db.session.commit()

        return anek_schema.jsonify(anek)

    def delete(self, anek_id):
        anek = models.Anek.query.filter_by(id=anek_id).first_or_404()

        db.session.delete(anek)
        db.session.commit()

        return anek_schema.jsonify(anek)


@api.resource('/aneks')
class AnekList(Resource):

    def get(self):
        aneks = models.Anek.query.all()
        return aneks_schema.jsonify(aneks)

    def post(self):
        if request.json is None:
            abort(400)

        anek = anek_schema.load(request.json, session=db.session)

        db.session.add(anek)
        db.session.commit()

        return anek_schema.jsonify(anek)


@api.resource('/aneks/random')
class RandomAnek(Resource):
    def get(self):
        anek = models.Anek.query.order_by(func.random()).first_or_404()
        return anek_schema.jsonify(anek)
