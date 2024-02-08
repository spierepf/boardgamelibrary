from util.rest_client import RestClient


def test_rest_client_does_not_add_authorization_header_by_default():
    assert RestClient.AUTH_HEADER not in RestClient().headers().keys()


def test_rest_client_adds_authorization_header_when_provided_with_a_token():
    assert RestClient('some token').headers()[RestClient.AUTH_HEADER] == 'Bearer some token'


def test_rest_client_does_not_have_token_by_default():
    assert not RestClient().has_token()


def test_rest_client_has_token_when_given_one():
    assert RestClient('some token').has_token()


def test_rest_client_that_has_deauthenticated_has_no_token():
    rest_client = RestClient('some token')
    rest_client.deauthenticate()
    assert not rest_client.has_token()
