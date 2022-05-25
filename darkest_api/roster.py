from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user

from .models import Roster
from .schema import RosterSchema
from . import db

bp = Blueprint("roster", __name__, url_prefix="/roster")
one_roster_schema = RosterSchema()

# GET endpoints

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
