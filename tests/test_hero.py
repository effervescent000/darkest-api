import pytest
import tests.shapes as shapes
from darkest_api.hero import validate_abilities


# GET endpoint tests


def test_get_heroes(client, user_header):
    response = client.get("/hero/", headers=user_header)
    assert response.status_code == 200

    data = response.json
    assert len(data) == 1
    assert data[0]["id"] == 2


@pytest.mark.parametrize(
    "given, expected, should",
    [
        (
            1,
            {"status_code": 401, "assertion": lambda x: "error" in x},
            "Return a 401 for trying to access another user's hero.",
        )
    ],
)
def test_get_hero(client, user_header, given, expected, should):
    response = client.get(f"/hero/{given}", headers=user_header)
    assert response.status_code == expected["status_code"]

    data = response.json
    assert expected["assertion"](data)


# POST endpoint tests


@pytest.mark.parametrize(
    "given, expected, should",
    [
        (
            shapes.hero_record_factory(id=3, hero_class="arbalest"),
            shapes.hero_response_factory(id=3, hero_class="arbalest", roster_id=2),
            "Return a hero w/ a default name, w/o stats or abilities.",
        ),
        (
            shapes.hero_record_factory(
                id=3, hero_class="crusader", name="Some Crusader"
            ),
            shapes.hero_response_factory(
                id=3, hero_class="crusader", name="Some Crusader", roster_id=2
            ),
            "Return a hero with the correct name",
        ),
        (
            shapes.hero_record_factory(
                id=3,
                hero_class="arbalest",
                stats=[
                    shapes.stat_record_factory(field="crit", value=2, hero_id=3),
                    shapes.stat_record_factory(field="acc_mod", value=3, hero_id=3),
                ],
                abilities=[
                    shapes.ability_record_factory(slot=0, level=1, hero_id=3),
                    shapes.ability_record_factory(slot=1, level=2, hero_id=3),
                ],
            ),
            shapes.hero_response_factory(
                id=3,
                hero_class="arbalest",
                roster_id=2,
                stats=[
                    shapes.stat_record_factory(field="crit", value=2, hero_id=3),
                    shapes.stat_record_factory(field="acc_mod", value=3, hero_id=3),
                ],
                abilities=[
                    shapes.ability_record_factory(slot=0, level=1, hero_id=3),
                    shapes.ability_record_factory(slot=1, level=2, hero_id=3),
                ],
            ),
            "Return a hero with stats and abilities.",
        ),
    ],
)
def test_add_hero_valid(
    client, user_header, clean_hero_response, given, expected, should
):
    response = client.post("/hero/", json=given, headers=user_header)
    assert response.status_code == 201

    data = clean_hero_response(response.json)
    assert data == clean_hero_response(expected)


@pytest.mark.parametrize(
    "given, expected, should",
    [
        (
            shapes.hero_record_factory(id=3),
            {"error": "no hero class specified"},
            "Return error if no hero class is specified.",
        )
    ],
)
def test_add_hero_invalid(client, user_header, given, expected, should):
    response = client.post("/hero/", json=given, headers=user_header)
    assert response.status_code == 400

    data = response.json
    assert data == expected


# PUT endpoint tests

# DELETE endpoint tests

# utils tests


@pytest.mark.parametrize(
    "given, expected, should",
    [
        (
            [
                shapes.ability_record_factory(slot=0),
                shapes.ability_record_factory(slot=1),
                shapes.ability_record_factory(slot=2),
                shapes.ability_record_factory(slot=3),
                shapes.ability_record_factory(slot=4, enabled=False),
                shapes.ability_record_factory(slot=5, enabled=False),
                shapes.ability_record_factory(slot=6, enabled=False),
            ],
            [
                shapes.ability_record_factory(slot=0),
                shapes.ability_record_factory(slot=1),
                shapes.ability_record_factory(slot=2),
                shapes.ability_record_factory(slot=3),
                shapes.ability_record_factory(slot=4, enabled=False),
                shapes.ability_record_factory(slot=5, enabled=False),
                shapes.ability_record_factory(slot=6, enabled=False),
            ],
            "Return the ability list unaltered.",
        )
    ],
)
def test_validate_abilities_valid(clean_ability_response, given, expected, should):
    response = validate_abilities(given)
    assert clean_ability_response(response) == clean_ability_response(expected)


@pytest.mark.parametrize(
    "given, expected, should",
    [
        (
            [
                shapes.ability_record_factory(slot=0),
                shapes.ability_record_factory(slot=0),
            ],
            False,
            "Return False if there are >1 ability in the same slot.",
        ),
        (
            [
                shapes.ability_record_factory(slot=0),
                shapes.ability_record_factory(slot=1),
                shapes.ability_record_factory(slot=2),
                shapes.ability_record_factory(slot=3),
                shapes.ability_record_factory(slot=4),
                shapes.ability_record_factory(slot=5, enabled=False),
                shapes.ability_record_factory(slot=6, enabled=False),
            ],
            False,
            "Return False if >4 abilities are enabled",
        ),
    ],
)
def test_validate_abilities_invalid(given, expected, should):
    response = validate_abilities(given)
    assert response == expected
