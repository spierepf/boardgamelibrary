from util.rest_client import RestClient


def test_rest_client_does_not_add_authorization_header_by_default():
    assert RestClient.AUTH_HEADER not in RestClient().headers().keys()


def test_rest_client_add_authorization_header_when_provided_with_a_token():
    assert RestClient('some token').headers()[RestClient.AUTH_HEADER] == 'Bearer some token'
