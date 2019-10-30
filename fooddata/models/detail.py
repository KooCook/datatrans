"""

References:
    https://fdc.nal.usda.gov/api-guide.html#food-detail-endpoint
    https://fdc.nal.usda.gov/portal-data/external/dataDictionary
"""
import datetime
import enum

import requests

import utils
from fooddata.models.search import FoodDataType
from fooddata.utils import parse_date


class FoodClass(enum.Enum):
    FOUNDATION = 'FinalFood'
    SURVEY = 'Survey'
    BRANDED = 'Branded'
    LEGACY = 'FinalFood'


class Food:
    """Any substance consumed by humans for nutrition, taste and/or aroma.

    Attributes:
        fdc_id (int): Unique permanent identifier of the food
        food_class (FoodClass): For internal use only
        data_type (FoodDataType): Type of food data
            (see Files tab for possible values).
        description (str): Description of the food
        food_category_id: Id of the food category the food belongs to
        publication_date: Date when the food was published to FoodData Central
        scientific_name: The scientific name for the food
        food_key: A string of characters used to identify both the
            current and all historical records for a specific food.
    """

    __slots__ = (
        'fdc_id',
        'food_class',
        'data_type',
        'description',
        'food_category_id',
        'publication_date',
        'scientific_name',
        'food_key',
    )

    def __init__(self,*, _dict_: dict):
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

        self.fdc_id: int = _dict_.pop('fdcId', None)
        self.food_class: FoodClass = FoodClass(_dict_.pop('foodClass', None))
        self.data_type: FoodDataType = FoodDataType(_dict_.pop('dataType', None))
        self.description: str = _dict_.pop('description', None)
        self.publication_date: 'datetime.date' = parse_date(_dict_.pop('publicationDate', None))

        self.food_category_id = _dict_.pop('foodCategoryId', None)
        self.food_key = _dict_.pop('foodKey', None)
        self.scientific_name = _dict_.pop('scientificName', None)


class BrandedFood:
    """
    Foods whose nutrient values are typically obtained from food label
    data provided by food brand owners.

    Attributes:
        fdc_id (int): ID of the food in the food table
        brand_owner: Brand owner for the food
        gtin_upc: GTIN or UPC code identifying the food
        ingredients: The list of ingredients (as it appears on the product label)
        serving_size: The amount of the serving size when expressed as gram or ml
        serving_size_unit: The unit used to express the serving size (gram or ml)
        household_serving_fulltext: amount and unit of serving size when
            expressed in household units
        branded_food_category: The category of the branded food, assigned
            by GDSN or Label Insight
        data_source: The source of the data for this food. GDSN (for GS1)
            or LI (for Label Insight).
        modified_date: This date reflects when the product data was last
            modified by the data provider, i.e., the manufacturer
        available_date: This is the date when the product record was
            available for inclusion in the database.
    """

    __slots__ = (
        'fdc_id',
        'brand_owner',
        'gtin_upc',
        'ingredients',
        'serving_size',
        'serving_size_unit',
        'household_serving_fulltext',
        'branded_food_category',
        'data_source',
        'modified_date',
        'available_date',
    )

    def __init__(self, *, _dict_: dict):
        pass


class FoodDetailResponse:
    """ FoodData Detail endpoint Response handler. """

    __slots__ = (
        'response',
        'food',
    )

    def __init__(self, response: requests.Response):
        """

        Args:
            response: The Response returned by the FoodData Detail endpoint
        """
        self.response = response

        data = response.json()
        if data['foodClass'] == FoodClass.FOUNDATION.value:
            pass
        elif data['foodClass'] == FoodClass.SURVEY.value:
            pass
        elif data['foodClass'] == FoodClass.BRANDED.value:
            pass
        elif data['foodClass'] == FoodClass.LEGACY.value:
            pass
        else:
            raise ValueError('\'foodClass\' is not recognized')
