from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user

from .models import Roster
from .schema import RosterSchema
from . import db

bp = Blueprint("roster", __name__, url_prefix="/roster")
one_roster_schema = RosterSchema()
multi_roster_schema = RosterSchema(many=True)

# GET endpoints


@bp.route("/", methods=["GET"])
@jwt_required()
def get_rosters():
    """For now there's only 1 roster per user, but I want to leave room for this to change in the future"""
    rosters = Roster.query.filter_by(user_id=current_user.id).all()
    return jsonify(multi_roster_schema.dump(rosters))


# POST endpoints


@bp.route("/", methods=["POST"])
@jwt_required()
def add_roster():
    data = request.get_json()
    name = data.get("name")
    roster = Roster(name=name, user_id=current_user.id)
    db.session.add(roster)
    db.session.commit()
    return jsonify(one_roster_schema.dump(roster)), 201


# PUT endpoints

# DELETE endpoints
