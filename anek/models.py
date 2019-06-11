from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class Anek(db.Model):
    __tablename__ = 'aneks'

    id = db.Column('anek_id', db.Integer(), primary_key=True)
    text = db.Column(db.Text(), nullable=False)
    like_count = db.Column(db.Integer())
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    source_id = db.Column(db.Integer(), db.ForeignKey('sources.source_id'), nullable=False)


class Source(db.Model):
    __tablename__ = 'sources'

    id = db.Column('source_id', db.Integer(), primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    url = db.Column(db.Text(), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('name', 'url', name='name_url_unique_constraint'),
    )

    aneks = db.relationship('Anek', backref=db.backref('source', lazy='joined', uselist=False))
