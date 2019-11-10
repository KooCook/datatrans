"""

References:
    https://fdc.nal.usda.gov/api-guide.html
"""
import json

import decouple
import requests

from datatrans import utils
from datatrans.fooddata import search


def send_food_search_api_request(
        criteria: search.request.FoodSearchCriteria,
        *, api_key: str = decouple.config('DATA_GOV_API_KEY', 'MY_API_KEY')
) -> requests.Response:
    """Send a Food Search Endpoint request.

    Args:
        criteria: FoodData Central search criteria
            general_search_input (str): Search query (general text)
            included_data_types (Dict[str, bool]): Specific data types to include in search
            ingredients: The list of ingredients (as it appears on the product label)
            brand_owner (str): Brand owner for the food
            require_all_words (bool): When True, the search will only return foods
            contain all of the words that were entered in the search field
            page_number (int): The page of results to return
            sort_field (SortField): The name of the field by which to sort
            sort_direction (SortDirection): The direction of the sorting
        api_key: Required. Must be a data.gov registered API key.
    """
    url = 'https://api.nal.usda.gov/fdc/v1/search'
    data = {utils.snake_to_camel(k): v for k, v in criteria.items() if v is not None}

    if not data:
        raise ValueError('No criteria to search')
    if api_key == 'MY_API_KEY':
        raise UserWarning('Invalid API key, configure API key in .env first')

    return requests.post(url, params={'api_key': api_key},
                         data=json.dumps(data, cls=utils.JSONEncoder),
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
