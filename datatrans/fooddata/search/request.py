"""

References:
    https://fdc.nal.usda.gov/api-guide.html#food-search-endpoint
"""
import enum
from typing import Dict

from datatrans import utils


class FoodDataType(enum.Enum):
    FOUNDATION = 'Foundation'
    SURVEY = 'Survey (FNDDS)'
    BRANDED = 'Branded'
    LEGACY = 'SR Legacy'


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

    __slots__ = (
        'general_search_input', 'included_data_types', 'ingredients', 'brand_owner', 'require_all_words', 'page_number',
        'sort_field', 'sort_direction')

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
