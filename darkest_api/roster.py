from flask import Blueprint, request, jsonify, current_app

from .models import Roster
from .schema import RosterSchema
from . import db

bp = Blueprint("roster", __name__, url_prefix="/roster")
one_roster_schema = RosterSchema()

# GET endpoints

# POST endpoints

# PUT endpoints

# DELETE endpoints
