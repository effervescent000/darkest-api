import pytest
import tests.shapes as shapes


# GET endpoint tests

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
                    shapes.stat_record_factory(id=5, field="crit", value=2, hero_id=3),
                    shapes.stat_record_factory(
                        id=6, field="acc_mod", value=3, hero_id=3
                    ),
                ],
            ),
            shapes.hero_response_factory(
                id=3,
                hero_class="arbalest",
                roster_id=2,
                stats=[
                    shapes.stat_record_factory(id=5, field="crit", value=2, hero_id=3),
                    shapes.stat_record_factory(
                        id=6, field="acc_mod", value=3, hero_id=3
                    ),
                ],
            ),
            "Return a hero with stats.",
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
