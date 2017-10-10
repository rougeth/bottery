from bottery.user import User


def test_user():
    user = User(1, "firstname", "lastname", "username", "en")

    assert user.id == 1
    assert user.first_name == "firstname"
    assert user.last_name == "lastname"
    assert user.username == "username"
    assert user.language == "en"
