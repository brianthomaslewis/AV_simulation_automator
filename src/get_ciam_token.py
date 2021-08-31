from urllib.parse import urlencode
import requests


def get_CIAM_token(client_id, client_secret, ciam_url, proxy_dict):
    query_params = {'client_id': client_id,
                    'client_secret': client_secret,
                    'grant_type': 'client_credentials'}

    query_params = urlencode(query_params, encoding='UTF-8')

    url = f'{ciam_url}?{query_params}'

    headers = {'cache-control': 'no-cache', 'content-type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, headers=headers, proxies=proxy_dict)

    access_token = response.json().get('access_token')

    if not access_token:
        raise ValueError("Missing access token. "
                         "Check CIAM 'client_id' and 'client_secret' credentials and try again.")

    return access_token
