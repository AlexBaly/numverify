import requests
import pytest
from numverify.sorter.api.api import API


def test_send_request():
    api = API()
    assert api._send_request("qwerty") == False, "Number not False"

    api = API("http://qwerewtwtw")
    try:
        api._send_request("+71234567890")
        assert  False, "Must fail with this url"
    except requests.exceptions.ConnectionError:
        assert True

def test_search_country():
    texts = ["Russian Federation","United States of America"]
    api = API()
    api.search_country(texts)
    assert  len(api.phone) == len(texts), "Eroor Len"
    phone_backup = api.phone.copy()
    api.search_country(texts)
    assert api.phone == phone_backup, "Erro Backup"

    api = API()
    api.search_country(texts[0])
    assert len(api.phone) == 1, "not changed"
    api.search_country(texts[1])
    assert len(api.phone) == 2, "not changed"
    phone_backup = api.phone.copy()
    api.search_country(texts[0])
    assert api.phone == phone_backup, "Changed BackUp"

@pytest.fixture()
def prepare_get_country():
    api = API()
    api.search_country(["United States of America"])
    return api


def test_get_country(prepare_get_country):
    assert prepare_get_country.get_country("Russian Federation") is None, "Text1"
    assert prepare_get_country.get_country("United States of America") is not None, "Text123"
