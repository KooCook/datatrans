"""

References:
    https://fdc.nal.usda.gov/
"""

import json

import decouple
import requests

import utils
from fooddata.models.search import FoodSearchCriteria


def send_food_search_api_request(
        criteria: FoodSearchCriteria,
        *, api_key: str = decouple.config('DATA_GOV_API_KEY', 'MY_API_KEY')
) -> requests.Response:
    """Send a Food Search Endpoint request.

    Args:
        criteria: FoodData Central search criteria
        api_key: Required. Must be a data.gov registered API key.
    """
    url = 'https://api.nal.usda.gov/fdc/v1/search'
    data = {utils.snake_to_camel(k): v for k, v in criteria.items() if v is not None}

    if not data:
        raise ValueError('No criteria to search')
    if api_key == 'MY_API_KEY':
        raise UserWarning('Invalid API key, configure API key in .env first')

    return requests.post(url, params={'api_key': api_key}, data=json.dumps(data),
                         headers={'Content-Type': 'application/json'})


def send_food_detail_api_request(
        fdc_id: int,
        *, api_key: str = decouple.config('DATA_GOV_API_KEY', 'MY_API_KEY')
) -> requests.Response:
    """Send a Food Detail Endpoint request.

    Args:
        fdc_id: Required. Must be a data.gov registered API key.
        api_key: Required. Unique identifier for the food.
    """
    url = 'https://api.nal.usda.gov/fdc/v1/' + str(fdc_id)
    return requests.get(url, params={'api_key': api_key},
                        headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    pass
