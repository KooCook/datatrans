"""

References:
    https://fdc.nal.usda.gov/api-guide.html#food-search-endpoint
"""
from typing import Dict, List

import datetime
import enum
import importlib

import requests

utils = importlib.import_module('datatrans.utils')


class SortField(enum.Enum):
    DESCRIPTION = 'lowercaseDescription.keyword'
    DATATYPE = 'dataType.keyword'
    PUBDATE = 'publishedDate'
    ID = 'fdcId'


class SortDirection(enum.Enum):
    ASC = 'asc'
    DESC = 'desc'


class FoodSearchCriteria(utils.DataClass):
    """Represents a FoodData Central search criteria.

    Attributes:
        general_search_input (str): Search query (general text)
        included_data_types (Dict[str, bool]): Specific data types to include in search
        ingredients: The list of ingredients (as it appears on the product label)
        brand_owner (str): Brand owner for the food
        require_all_words (bool): When True, the search will only return foods
        contain all of the words that were entered in the search field
        page_number (int): The page of results to return
        sort_field (SortField): The name of the field by which to sort
        sort_direction (SortDirection): The direction of the sorting
    """

    __attr__ = (
        ('general_search_input', str),
        ('included_data_types', dict, lambda x: x),
        ('ingredients', str),
        ('brand_owner', str),
        ('require_all_words', bool),
        ('page_number', int),
        ('sort_field', SortField),
        ('sort_direction', SortDirection),
    )

    def __init__(self, _dict_: dict = None, **kwargs):
        super(FoodSearchCriteria, self).__init__(_dict_)
        for k, v in kwargs.items():
            if k in self.__slots__:
                setattr(self, k, v)


#


class FoodDataType(enum.Enum):
    FOUNDATION = 'Foundation'
    SURVEY = 'Survey (FNDDS)'
    BRANDED = 'Branded'
    LEGACY = 'SR Legacy'


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
        ('food_code', str),   # not sure
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
