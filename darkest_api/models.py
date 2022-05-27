from . import db
from passlib.hash import pbkdf2_sha256 as hash


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(200))

    roster = db.relationship(
        "Roster", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    @staticmethod
    def hash_password(password):
        return hash.hash(password)

    def check_password(self, input):
        return hash.verify(input, self.password)


class Roster(db.Model):
    __tablename__ = "rosters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    heroes = db.relationship(
        "Hero", backref="roster", lazy=True, cascade="all, delete-orphan"
    )


class Hero(db.Model):
    __tablename__ = "heroes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    hero_class = db.Column(db.String(20), nullable=False)
    resolve = db.Column(db.Integer, nullable=False, default=0)
    roster_id = db.Column(db.Integer, db.ForeignKey("rosters.id"))

    stats = db.relationship(
        "Stat", backref="hero", lazy=True, cascade="all, delete-orphan"
    )
    abilities = db.relationship(
        "Ability", backref="hero", lazy=True, cascade="all, delete-orphan"
    )


class Stat(db.Model):
    __tablename__ = "stats"
    id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Float, nullable=False)

    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"))


class Ability(db.Model):
    __tablename__ = "abilities"
    id = db.Column(db.Integer, primary_key=True)
    slot = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False, default=0)
    enabled = db.Column(db.Boolean, nullable=False)

    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"))
