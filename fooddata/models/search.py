"""

References:
    https://fdc.nal.usda.gov/api-guide.html#food-search-endpoint
"""
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
            *, _dict_: dict = None):
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

        self.general_search_input: str = _dict_.pop('generalSearchInput', None)
        self.included_data_types: Dict[str, bool] = _dict_.pop('includedDataTypes', None)
        self.ingredients: str = _dict_.pop('ingredients', None)
        self.brand_owner: str = _dict_.pop('brandOwner', None)
        self.require_all_words: bool = _dict_.pop('requireAllWords', None)
        self.page_number: int = _dict_.pop('pageNumber', None)
        self.sort_field: SortField = SortField(_dict_.pop('sortField', None))
        self.sort_direction: SortDirection = SortDirection(_dict_.pop('sortDirection', None))

        if len(_dict_) != 0:
            import warnings
            warnings.warn('\'_dict_\' has left-over keys: {}'.format(_dict_))

    def dict(self) -> dict:
        """ Returns a dict with fields in camelCase. """
        return {utils.snake_to_camel(field): getattr(self, field)
                for field in self.__slots__
                if getattr(self, field) is not None}

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
    __slots__ = (
        # always
        'fdc_id',
        'description',
        'data_type',
        'published_date',
        'all_highlight_fields',
        'score',
        # Survey only
        'food_code',
        # Branded only
        'gtin_upc',
        'brand_owner',
        # optional
        # 'scientific_name',
        # 'common_names',
        'additional_descriptions',
        # 'ndb_number'
        # 'ingredients',
    )

    def __init__(self, *, _dict_: dict):
        """Create a minimal Food data class.

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

        self.fdc_id: int = _dict_.pop('fcdId', None)
        self.description: str = _dict_.pop('description', None)
        self.data_type: FoodDataType = FoodDataType(_dict_.pop('dataType', None))
        self.published_date: datetime.date = datetime.date.fromisoformat(_dict_.pop('publishedDate', None))
        self.all_highlight_fields: str = _dict_.pop('allHighlightFields', None)
        self.score: float = _dict_.pop('score', None)
        # optional
        self.additional_descriptions: str = _dict_.pop('additionalDescriptions', None)
        # Survey only
        self.food_code: str = _dict_.pop('foodCode', None)  # not sure
        # Branded only
        self.gtin_upc: str = _dict_.pop('gtinUpc', None)  # can have 0 in front
        self.brand_owner: str = _dict_.pop('brandOwner', None)

        if len(_dict_) != 0:
            import warnings
            warnings.warn('\'_dict_\' has left-over keys: {}'.format(_dict_))

    def dict(self) -> dict:
        """ Returns a dict with fields in camelCase. """
        return {utils.snake_to_camel(field): getattr(self, field)
                for field in self.__slots__
                if getattr(self, field) is not None}

    def items(self):
        return self.dict().items()


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
