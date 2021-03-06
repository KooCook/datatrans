"""

References:
    https://fdc.nal.usda.gov/api-guide.html#food-search-endpoint
"""
from typing import Dict, Union

from datatrans import utils
from datatrans.utils.classes import JSONEnum as Enum


__all__ = ['FoodDataType', 'SortField', 'SortDirection', 'FoodSearchCriteria']


class FoodDataType(Enum):
    FOUNDATION = 'Foundation'
    SURVEY = 'Survey (FNDDS)'
    BRANDED = 'Branded'
    LEGACY = 'SR Legacy'


class SortField(Enum):
    DESCRIPTION = 'lowercaseDescription.keyword'
    DATATYPE = 'dataType.keyword'
    PUBDATE = 'publishedDate'
    ID = 'fdcId'


class SortDirection(Enum):
    ASC = 'asc'
    DESC = 'desc'


def verify_included_data_types(d: Dict[Union[FoodDataType, str], bool]):
    d = {FoodDataType(k): v for k, v in d.items()}
    return {
        FoodDataType.FOUNDATION.value: d.pop(FoodDataType.FOUNDATION, False),
        FoodDataType.SURVEY.value: d.pop(FoodDataType.SURVEY, False),
        FoodDataType.BRANDED.value: d.pop(FoodDataType.BRANDED, False),
        FoodDataType.LEGACY.value: d.pop(FoodDataType.LEGACY, False),
    }


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
        ('included_data_types', dict,
         verify_included_data_types),
        ('ingredients', str),
        ('brand_owner', str),
        ('require_all_words', bool),
        ('page_number', int),
        ('sort_field', SortField),
        ('sort_direction', SortDirection),
    )

    def __init__(self, _dict_: dict = None, **kwargs):
        if _dict_ is not None:
            super().__init__(_dict_=_dict_)
            return
        for k, v in kwargs.items():
            if k in self.__slots__:
                kwargs[utils.snake_to_camel(k)] = kwargs.pop(k)
        super().__init__(_dict_=kwargs)
