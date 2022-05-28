from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user

from .models import Hero, Stat, Ability
from .schema import HeroSchema
from . import db

bp = Blueprint("hero", __name__, url_prefix="/hero")
one_hero_schema = HeroSchema()
multi_hero_schema = HeroSchema(many=True)

# GET endpoints

# POST endpoints


@bp.route("/", methods=["POST"])
@jwt_required()
def add_hero():
    data = request.get_json()
    hero_class = data.get("hero_class")
    if not hero_class:
        return {"error": "no hero class specified"}, 400
    # change this so it will default to like "Arbalest 2" or whatever
    # based on how many of X I have in the roster already
    name = data.get("name")
    if not name:
        name = "Unnamed Hero"
    resolve = data.get("resolve", 1)  # Do heroes start at 1 or 0? I don't remember
    stats = data.get("stats", [])
    abilities = data.get("abilities", [])

    hero = Hero(
        name=name,
        hero_class=hero_class,
        resolve=resolve,
        roster_id=current_user.roster[0].id,
    )
    for stat in stats:
        hero.stats.append(Stat(field=stat["field"], value=stat["value"]))
    for ability in abilities:
        hero.abilities.append(
            Ability(
                slot=ability["slot"], level=ability["level"], enabled=ability["enabled"]
            )
        )

    db.session.add(hero)
    db.session.commit()

    return jsonify(one_hero_schema.dump(hero)), 201


# PUT endpoints

# DELETE endpoints

# utils


def validate_abilities(abilities):
    abilities_lookup = {}
    enabled_count = 0
    for ability in abilities:
        if ability["slot"] not in abilities_lookup:
            abilities_lookup[ability["slot"]] = ability
        else:
            return False
        if ability["enabled"]:
            enabled_count += 1

    if enabled_count > 4:
        return False

    return abilities
