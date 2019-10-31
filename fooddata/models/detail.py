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
import fooddata.utils


class FoodClass(enum.Enum):
    FOUNDATION = 'FinalFood'
    SURVEY = 'Survey'
    BRANDED = 'Branded'
    LEGACY = 'FinalFood'


class Food(utils.DataClass):
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

    __attr__ = (
        ('fdc_id', int),
        ('food_class', FoodClass),
        ('data_type', FoodDataType),
        ('description', str),
        ('food_category_id', str),
        ('publication_date', datetime.date, fooddata.utils.parse_date),
        ('scientific_name', str),
        ('food_key', str),
    )


class BrandedFood(utils.DataClass):
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

    __attr__ = (
        ('fdc_id', int),
        ('brand_owner', str),
        ('gtin_upc', str),
        ('ingredients', str),
        ('serving_size', str),
        ('household_serving_fulltext', str),
        ('branded_food_category', str),
        ('modified_date', datetime.date, fooddata.utils.parse_date),
        ('available_date', datetime.date, fooddata.utils.parse_date),
    )


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
