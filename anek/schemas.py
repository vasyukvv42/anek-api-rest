from flask_marshmallow import Marshmallow

from marshmallow_sqlalchemy.fields import Related
from anek.models import Anek, Source

ma = Marshmallow()


class SourceSchema(ma.ModelSchema):
    class Meta:
        model = Source
        exclude = ('id', )

    url = ma.Url(required=True)


class AnekSchema(ma.ModelSchema):
    class Meta:
        model = Anek
        dump_only = ('id', 'created_at')

    source = Related(column=('name', 'url'))


anek_schema = AnekSchema()
aneks_schema = AnekSchema(many=True)
source_schema = SourceSchema()
