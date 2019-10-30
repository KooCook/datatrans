import datetime
import enum
from typing import Dict, List

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


class FoodSearchCriteria:
    """Represents a FoodData Central search criteria.

    Attributes:
        general_search_input: Search query (general text)
        included_data_types: Specific data types to include in search
        ingredients: The list of ingredients (as it appears on the product label)
        brand_owner: Brand owner for the food
        require_all_words: When True, the search will only return foods
        contain all of the words that were entered in the search field
        page_number: The page of results to return
        sort_field: The name of the field by which to sort
        sort_direction: The direction of the sorting
    """

    __slots__ = (
        'general_search_input',
        'included_data_types',
        'ingredients',
        'brand_owner',
        'require_all_words',
        'page_number',
        'sort_field',
        'sort_direction',
    )

    def __init__(
            self,
            general_search_input: str = None,
            included_data_types: Dict[str, bool] = None,
            ingredients: str = None,
            brand_owner: str = None,
            require_all_words: bool = None,
            page_number: int = None,
            sort_field: SortField = None,
            sort_direction: SortDirection = None,
            *, _dict_: Dict = None):
        """Create a FoodData Central criteria.

        Args:
            ...
            _dict_: A dict with fields in camelCase to base creation on
        """
        if _dict_ is None:
            _dict_ = {}
        elif not isinstance(_dict_, dict):
            raise ValueError('\'_dict_\' should be a \'dict\'')
        for k, v in locals().items():
            if k not in self.__slots__:
                continue
            if v is not None:
                _dict_[utils.snake_to_camel(k)] = v
            elif not hasattr(_dict_, utils.snake_to_camel(k)):
                _dict_[utils.snake_to_camel(k)] = None

        self.general_search_input: str = _dict_['generalSearchInput']
        self.included_data_types: Dict[str, bool] = _dict_['includedDataTypes']
        self.ingredients: str = _dict_['ingredients']
        self.brand_owner: str = _dict_['brandOwner']
        self.require_all_words: bool = _dict_['requireAllWords']
        self.page_number: int = _dict_['pageNumber']
        self.sort_field: SortField = _dict_['sortField']
        self.sort_direction: SortDirection = _dict_['sortDirection']

    def dict(self):
        """ Returns a dict with fields in camelCase. """
        return {utils.snake_to_camel(field): getattr(self, field)
                for field in self.__slots__}

    def items(self):
        return self.dict().items()


#


class FoodDataType(enum.Enum):
    FOUNDATION = 'Foundation'
    SURVEY = 'Survey (FNDDS)'
    BRANDED = 'Branded'
    LEGACY = 'SR Legacy'


class Food:
    """Represents a minimal food object returned by FoodData Search endpoint.

    Attributes:
        fdc_id:
        description:
        data_type:
        published_date:
        all_highlight_fields:
        score:
        additional_descriptions:
        food_code:
        gtin_upc:
        brand_owner:
    """
    __slots__ = (
        # always
        'fdc_id',
        'description',
        'data_type',
        'published_date',
        'all_highlight_fields',
        'score',
        # optional
        'additional_descriptions',
        # Survey only
        'food_code',
        # Branded only
        'gtin_upc',
        'brand_owner',
    )

    def __init__(self, *, _dict_: dict):
        """Create a Food data class.

        Args:
            _dict_: A dict with fields in camelCase to base creation on
        """
        if _dict_ is None:
            _dict_ = {}
        elif not isinstance(_dict_, dict):
            raise ValueError('\'_dict_\' should be a \'dict\'')
        for k, v in locals().items():
            if k not in self.__slots__:
                continue
            if v is not None:
                _dict_[utils.snake_to_camel(k)] = v
            elif not hasattr(_dict_, utils.snake_to_camel(k)):
                _dict_[utils.snake_to_camel(k)] = None

        self.fdc_id: int = _dict_['fcdId']
        self.description: str = _dict_['description']
        self.data_type: FoodDataType = _dict_['dataType']
        self.published_date: datetime.date = _dict_['publishedDate']
        self.all_highlight_fields: str = _dict_['allHighlightFields']
        self.score: float = _dict_['score']
        # optional
        self.additional_descriptions: str = _dict_['additionalDescriptions']
        # Survey only
        self.food_code: str = _dict_['foodCode']  # not sure
        # Branded only
        self.gtin_upc: str = _dict_['gtinUpc']  # can have 0 in front
        self.brand_owner: str = _dict_['brandOwner']

    def dict(self):
        """ Returns a dict with fields in camelCase. """
        _dict_ = {utils.snake_to_camel(field): getattr(self, field)
                  for field in self.__slots__[:-3]}
        if self.data_type is FoodDataType.SURVEY:
            _dict_['foodCode'] = self.food_code
        elif self.data_type is FoodDataType.BRANDED:
            _dict_['dtinUpc'] = self.gtin_upc
            _dict_['brandOwner'] = self.brand_owner
        return _dict_

    def items(self):
        return self.dict().items()


class FoodSearchResponse:
    """ Represents a FoodData Search endpoint response object. """

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
        self.foods: List[Food] = [data['foods']]
