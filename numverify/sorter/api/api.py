import requests
import json
from numverify.sorter.api.constants import BASE_URL, NO_PHONE

class API:
    def __init__(self, url=BASE_URL):
        self.phone = {}
        self.url = url
    def _send_request(self,text):
        param = {
            'number' : text,
            'country_code' : '',
            'format' : ''
        }
        response = requests.get(self.url, params=param)
        response.raise_for_status()
        response_dict = response.json()
        #print(response_dict)
        # if response_dict['success']:

        if ('success' in response_dict ):
            return response_dict['success']
        elif ('valid' in response_dict ):
            if response_dict['valid']:
                return response_dict['country_name']
            else:
                return response_dict['valid']

        return NO_PHONE

    def search_country(self,texts):
        if isinstance(texts, str):
            texts = [texts]
        for text in texts:
            if text not in self.phone:
                self.phone[text] = self._send_request(text)
        return self.phone[text]

    def get_country(self, text):
        return  self.phone.get(text)