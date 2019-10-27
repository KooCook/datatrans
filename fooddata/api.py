"""
https://fdc.nal.usda.gov/
"""
import enum
import json
from typing import Dict

import decouple
import requests

import utils


class SortField(enum.Enum):
    DESCRIPTION = 'lowercaseDescription.keyword'
    DATATYPE = 'dataType.keyword'
    PUBDATE = 'publishedDate'
    ID = 'fdcId'


class SortDirection(enum.Enum):
    ASC = 'asc'
    DESC = 'desc'


def send_food_search_api_request(
        general_search_input: str = None,
        included_data_types: Dict[str, bool] = None,
        ingredients: str = None,
        brand_owner: str = None,
        require_all_words: bool = None,
        page_number: int = None,
        sort_field: SortField = None,
        sort_direction: SortDirection = None,
        *, api_key: str = decouple.config('DATA_GOV_API_KEY', 'MY_API_KEY')
) -> requests.Response:
    """
    Send a Food Search Endpoint request.

    :param general_search_input: Search query (general text)
    :param included_data_types: Specific data types to include in search
    :param ingredients: The list of ingredients (as it appears on the product label)
    :param brand_owner: Brand owner for the food
    :param require_all_words: When True, the search will only return foods
    that contain all of the words that were entered in the search field
    :param page_number: The page of results to return
    :param sort_field: The name of the field by which to sort
    :param sort_direction: The direction of the sorting
    :param api_key: Required. Must be a data.gov registered API key.
    """
    kwargs = dict(locals().items())
    if kwargs.pop('api_key') == 'MY_API_KEY':
        raise UserWarning('Invalid API key, configure API key in .env first')
    url = 'https://api.nal.usda.gov/fdc/v1/search'
    data = {utils.snake_to_camel(k): v
            for k, v in kwargs.items() if v is not None}
    if not data:
        raise ValueError('No criteria to search')
    return requests.post(url, params={'api_key': api_key}, data=json.dumps(data),
                         headers={'Content-Type': 'application/json'})


def send_food_detail_api_request(
        fdc_id: int,
        *, api_key: str = decouple.config('DATA_GOV_API_KEY', 'MY_API_KEY')
) -> requests.Response:
    """
    Send a Food Detail Endpoint request.

    :param fdc_id: Required. Must be a data.gov registered API key.
    :param api_key: Required. Unique identifier for the food.
    :return:
    """
    url = 'https://api.nal.usda.gov/fdc/v1/' + str(fdc_id)
    return requests.get(url, params={'api_key': api_key},
                        headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    pass
