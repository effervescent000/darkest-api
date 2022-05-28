from typing import Union
from random import randint
from darkest_api.models import Ability, User, Roster, Hero, Stat

HERO_ONE_ID = 1
HERO_TWO_ID = 2

factory_dict = dict[str, Union[str, int]]


def user_record_factory(
    id: int, *, username: str = None, role: str = None
) -> factory_dict:
    return {"id": id, "username": username or f"abcd-{id}", "role": role}


def roster_record_factory(id: int, *, name: str = None) -> factory_dict:
    return {"id": id, "name": name}


def hero_record_factory(
    id: int,
    *,
    name: str = None,
    hero_class: str = None,
    resolve: int = None,
    stats: list = None,
    abilities: list = None,
) -> factory_dict:
    return {
        "id": id,
        "name": name,
        "hero_class": hero_class,
        "resolve": resolve or 1,
        "stats": stats or [],
        "abilities": abilities or [],
    }


def stat_record_factory(
    *, id: int = None, field: str = None, value: int = None, hero_id: int
) -> factory_dict:
    return {
        "id": id or randint(1, 100000),
        "field": field or "crit",
        "value": value or 1,
        "hero_id": hero_id,
    }


def ability_record_factory(
    *,
    id: int = None,
    slot: int = None,
    level: int = None,
    enabled: bool = None,
    hero_id: int = None,
) -> factory_dict:
    return {
        "id": id or randint(1, 100000),
        "slot": slot or 0,
        "level": level or 0,
        "enabled": False if enabled is True else False,
        "hero_id": hero_id,
    }


def hero_graph(
    hero_id: int,
    *,
    name: str = None,
    hero_class: str = None,
    resolve: int = None,
    user_id: int = None,
    username: str = None,
    user_role: str = None,
) -> tuple:
    """Creates a hero, complete with roster, user, and some dummy stats and abilities"""
    u_id = user_id or randint(1, 10000)

    user = user_record_factory(u_id, username=username, role=user_role)
    roster = roster_record_factory(id=u_id)
    hero = hero_record_factory(
        hero_id,
        name=name,
        hero_class=hero_class,
        resolve=resolve,
    )
    stats = [
        stat_record_factory(hero_id=hero["id"]),
        stat_record_factory(field="acc", value=2, hero_id=hero["id"]),
    ]
    abilities = [
        ability_record_factory(slot=0, level=1, hero_id=hero["id"]),
        ability_record_factory(slot=2, level=1, hero_id=hero["id"]),
    ]

    return (
        User(**user),
        Roster(**roster, user_id=user["id"]),
        Hero(**hero, roster_id=roster["id"]),
        *[Stat(**stat) for stat in stats],
        *[Ability(**ability) for ability in abilities],
    )


def hero_response_factory(
    id: int,
    *,
    name: str = None,
    hero_class: str,
    resolve: int = None,
    roster_id: int,
    stats: list = None,
    abilities: list = None,
) -> factory_dict:
    return {
        "id": id,
        "name": name or "Unnamed Hero",
        "hero_class": hero_class,
        "resolve": resolve or 1,
        "roster_id": roster_id,
        "stats": stats or [],
        "abilities": abilities or [],
    }
