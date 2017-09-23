from bottery.plataform.telegram import TelegramUser


def test_telegram_user_with_last_name():
    sender = {
        'id': 1,
        'first_name': 'Andrew',
        'last_name': 'Martin',
    }

    user = TelegramUser(sender)
    assert str(user) == 'Andrew Martin (1)'


def test_telegram_user_without_last_name():
    sender = {
        'id': 1,
        'first_name': 'Andrew',
    }

    user = TelegramUser(sender)
    assert str(user) == 'Andrew (1)'
