import datetime
from typing import List

import requests

from datatrans import utils
from datatrans.fooddata.search.request import FoodDataType, FoodSearchCriteria


class Food(utils.DataClass):
    """Represents a minimal food object returned by FoodData Search endpoint.

    Attributes:
        fdc_id: Unique ID of the food.
        description: The description of the food.
        # scientific_name: Optional. The scientific name of the food.
        # common_names: Optional. Any other common names for the food.
        additional_descriptions: Optional. Any additional descriptions of the food.
        data_type: The type of the food data.
        food_code: Any A unique ID identifying the food within FNDDS.
        gtin_upc: GTIN or UPC code identifying the food.
        # ndb_number: Unique number assigned for foundation foods.
        published_date: Date the item was published to FDC.
        brand_owner: Brand owner for the food.
        # ingredients: The list of ingredients (as it appears on the product label).
        all_highlight_fields: Fields that were found matching the criteria.
        score: Relative score indicating how well the food matches the search criteria.
    """

    __attr__ = (
        ('fdc_id', int),
        ('description', str),
        ('data_type', FoodDataType),
        ('published_date', datetime.date, utils.fooddata.parse_date, {'sep': '/', 'format': 'MDY'}),
        ('all_highlight_fields', str),
        ('score', float),
        # Survey only
        ('food_code', str),  # not sure
        # Branded only
        ('gtin_upc', str),  # can have 0 in front
        ('brand_owner', str),
        # optional
        ('additional_descriptions', str),
        # 'scientific_name',
        # 'common_names',
        # 'ndb_number'
        # 'ingredients',
    )


class FoodSearchResponse:
    """ FoodData Search endpoint response handler. """

    __slots__ = (
        'response',
        'food_search_criteria',
        'total_hits',
        'current_page',
        'total_pages',
        'foods',
    )

    def __init__(self, response: requests.Response):
        """

        Args:
            response: The Response returned by the FoodData Search endpoint
        """
        self.response = response

        data = response.json()
        self.food_search_criteria = FoodSearchCriteria(_dict_=data['foodSearchCriteria'])
        self.total_hits: int = data['totalHits']
        self.current_page: int = data['currentPage']
        self.total_pages: int = data['totalPages']
        self.foods: List[Food] = [Food(_dict_=_dict_) for _dict_ in data['foods']]
