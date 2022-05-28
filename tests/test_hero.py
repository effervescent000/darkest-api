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
    ],
)
def test_add_hero_valid(client, user_header, given, expected, should):
    response = client.post("/hero/", json=given, headers=user_header)
    assert response.status_code == 201

    data = response.json
    assert data == expected


# PUT endpoint tests

# DELETE endpoint tests
