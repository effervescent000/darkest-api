import pytest


def test_get_rosters(client, user_header):
    response = client.get("/roster/", headers=user_header)
    data = response.json
    assert len(data) == 1
    assert data[0]["id"] == 2

    heroes = data[0]["heroes"]
    assert len(heroes) == 1
    assert heroes[0]["id"] == 2
