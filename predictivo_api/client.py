import requests

from predictivo_api import exception
from predictivo_api.enumerator import ErrorEnum


class Client(object):
    def __init__(self, host=None, access_token=None):
        if access_token and host:
            self.access_token = access_token
            self.base_url = host
        else:
            raise exception.CredentialRequired("You must provide either access_token and hostname")

    def _get(self, endpoint, auth):
        response = requests.get(self.base_url + endpoint, auth=auth)
        return self._parse(response).json()

    def _post(self, endpoint, auth, data):
        response = requests.post(self.base_url + endpoint, auth=auth, json=data)
        return self._parse(response).json()

    def _parse(self, response):
        if not response.ok:
            data = response.json()
            if 'detail' in data and 'status' in data:
                code = data['status']
                message = data['detail']
                try:
                    error_enum = ErrorEnum(code)
                except Exception:
                    raise exception.UnexpectedError('Error: {}. Message {}'.format(code, message))
                if error_enum == ErrorEnum.BadRequest:
                    raise exception.BadRequest(message)
                if error_enum == ErrorEnum.APIKeyMissing:
                    raise exception.APIKeyMissing(message)
                if error_enum == ErrorEnum.Forbidden:
                    raise exception.Forbidden(message)
                if error_enum == ErrorEnum.ResourceNotFound:
                    raise exception.ResourceNotFound(message)
                if error_enum == ErrorEnum.MethodNotAllowed:
                    raise exception.MethodNotAllowed(message)
                if error_enum == ErrorEnum.ResourceNestingTooDeep:
                    raise exception.ResourceNestingTooDeep(message)
                if error_enum == ErrorEnum.InvalidMethodOverride:
                    raise exception.InvalidMethodOverride(message)
                if error_enum == ErrorEnum.TooManyRequests:
                    raise exception.TooManyRequests(message)
                if error_enum == ErrorEnum.InternalServerError:
                    raise exception.InternalServerError(message)
                if error_enum == ErrorEnum.ComplianceRelated:
                    raise exception.ComplianceRelated(message)
                else:
                    raise exception.BaseError('Error: {}. Message {}'.format(code, message))
            return data
        else:
            return response

    def _request(self, method, endpoint, params=None, data=None):
        headers = {'Authorization': 'Basic {}'.format(self.creds)}
        try:
            url = self.base_url + endpoint
            response = requests.request(method=method, url=url, params=params, data=data, headers=headers)
            return self._parse(response)
        except Exception as e:
            print("Error while request: ", e)
            return False

    def describe_sugarcontacts(self):
        endpoint = ''
        return self._request('GET', endpoint)

    def describe_agenda(self):
        endpoint = ''
        return self._request('GET', endpoint)

    def insert_sugarcontacts(self):
        endpoint = ''
        return self._request('POST', endpoint)

    def insert_agenda(self):
        endpoint = ''
        return self._request('POST', endpoint)
