import pytest
from pytest import raises
from unittest.mock import MagicMock

from telegram_bot import TelegramBot


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_requests_get(*args, **kwargs):
    return MockResponse({"key1": "value1"}, 200)


def mocked_requests_get_failed(*args, **kwargs):
    return MockResponse(None, 400)


def mocked_requests_post(*args, **kwargs):
    return MockResponse({"ok": True}, 200)


@pytest.fixture()
def mock_open(monkeypatch):
    mock_file = MagicMock()
    mock_file.read = MagicMock(return_value="TOKEN")
    mock_open = MagicMock(return_value=mock_file)
    monkeypatch.setattr("builtins.open", mock_open)

    return mock_open


@pytest.fixture()
def mock_get(monkeypatch):
    mock_requests = MagicMock()
    mock_requests.get = MagicMock(return_value=mocked_requests_get)
    mock_get = MagicMock(return_value=mock_requests)
    monkeypatch.setattr("requests.get", mock_get)

    return mock_get


@pytest.fixture()
def mock_get_failed(monkeypatch):
    mock_requests = MagicMock()
    mock_requests.get = MagicMock(return_value=mocked_requests_get_failed)
    mock_get_failed = MagicMock(return_value=mock_requests)
    monkeypatch.setattr("requests.get", mock_get_failed)

    return mock_get


def test_returns_correct_request_updates(mock_open, mock_get, monkeypatch):
    mock_exists = MagicMock(return_value=True)
    monkeypatch.setattr("os.path.exists", mock_exists)
    bot = TelegramBot()
    print(bot.url)
    mock_open.assert_called_once_with("TELEGRAM_TOKEN.env", "r")

    result, status_code = bot.get_updates()
    mock_get.assert_called_once()



def test_returns_correct_request_updates_failed(mock_open, mock_get_failed, monkeypatch):
    mock_exists = MagicMock(return_value=True)
    monkeypatch.setattr("os.path.exists", mock_exists)
    bot = TelegramBot()
    mock_open.assert_called_once_with("TELEGRAM_TOKEN.env", "r")

    result, status_code = bot.get_updates()
    mock_get_failed.assert_called_once()


def test_throws_exception_with_bad_file_token(mock_open, monkeypatch):
    mock_exists = MagicMock(return_value=False)
    monkeypatch.setattr("os.path.exists", mock_exists)
    with raises(Exception):
        bot = TelegramBot()