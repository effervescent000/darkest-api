from random import randint
from darkest_api.models import User, Roster, Hero, Stat


def user_record_factory(id, *, username=None, role=None):
    return {"id": id, "username": username or f"abcd-{id}", "role": role}


def roster_record_factory(id, *, name=None, user_id):
    return {"id": id, "name": name, "user_id": user_id}


def hero_record_factory(id, *, name=None, hero_class=None, resolve=None, roster_id):
    return {
        "id": id,
        "name": name or f"hero-{id}",
        "hero_class": hero_class or "hellion",
        "resolve": resolve or 1,
        "roster_id": roster_id,
    }


def stat_record_factory(id, *, field=None, value=None, hero_id):
    return {"id": id, "field": field or "crit", "value": value or 1, "hero_id": hero_id}


def hero_graph(
    hero_id,
    *,
    name=None,
    hero_class=None,
    resolve=None,
    user_id=None,
    username=None,
    user_role=None,
):
    """Creates a hero, complete with roster, user, and some dummy stats"""
    u_id = user_id or randint(1, 10000)

    user = user_record_factory(u_id, username=username, role=user_role)
    roster = roster_record_factory(id=u_id, user_id=u_id)
    hero = hero_record_factory(
        hero_id,
        name=name,
        hero_class=hero_class,
        resolve=resolve,
        roster_id=roster["id"],
    )
    stats = [
        stat_record_factory(1, hero_id=hero["id"]),
        stat_record_factory(2, field="acc", value=2, hero_id=hero["id"]),
    ]

    return (
        User(**user),
        Roster(**roster),
        Hero(**hero),
        *[Stat(**stat) for stat in stats],
    )
