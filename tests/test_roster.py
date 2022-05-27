# GET endpoint tests


def test_get_rosters(client, user_header):
    response = client.get("/roster/", headers=user_header)
    assert response.status_code == 200
    data = response.json
    assert len(data) == 1
    assert data[0]["id"] == 2

    heroes = data[0]["heroes"]
    assert len(heroes) == 1
    assert heroes[0]["id"] == 2


# POST endpoint tests


def test_add_roster(client, user_header):
    response = client.post(
        "/roster/", json={"name": "A fake test roster"}, headers=user_header
    )
    assert response.status_code == 201
    data = response.json
    assert data["id"] == 3
    assert len(data["heroes"]) == 0
