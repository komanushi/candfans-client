import json
import os
from unittest.mock import MagicMock
from urllib.parse import quote_plus


def mock_session_request(method, url, *arg, **kwargs):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(f'{current_dir}/data/{method}_{quote_plus(url)}.json') as f:
        ret = f.read()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.cookies = {'XSRF-TOKEN': 'cookie'}
    mock_response.json.return_value = json.loads(ret) if ret else {}
    return mock_response
