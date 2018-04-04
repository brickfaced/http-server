import requests


def test_server_sends_200_response():
    response = requests.get('http://127.0.0.1:3000')
    assert response.status_code == 200


def test_server_sends_404_response():
    response = requests.get('http://127.0.0.1:3000/pig')
    assert response.status_code == 404
    assert response.text == 'Not Found'


def test_server_sends_qs_back():
    response = requests.get('http://127.0.0.1:3000/cow?msg="sup"')
    assert response.status_code == 200


def test_server_post():
    response = requests.post('http://127.0.0.1:3000/cow?msg="sup"')
    assert response.status_code == 200
