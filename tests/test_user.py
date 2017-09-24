from bottery.user import User


def test_user_instance():
    user = User(123, 'Jon', 'Snow', 'jon.snow', 'pt')
    assert user.id == 123
    assert user.first_name == 'Jon'
    assert user.last_name == 'Snow'
    assert user.username == 'jon.snow'
    assert user.language == 'pt'
