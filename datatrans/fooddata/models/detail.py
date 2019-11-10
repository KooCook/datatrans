"""

References:
    https://fdc.nal.usda.gov/api-guide.html#food-detail-endpoint
    https://fdc.nal.usda.gov/portal-data/external/dataDictionary
"""
import datetime
import enum

import requests

from datatrans.fooddata.models.search import FoodDataType

from datatrans import utils


def parse_fooddata_date(date_str: str) -> datetime.date:
    """ Wrapper specific for fooddata's format """
    return utils.fooddata.parse_date(date_str, sep='/', format='MDY')


class FoodClass(enum.Enum):
    FOUNDATION = 'FinalFood'
    SURVEY = 'Survey'
    BRANDED = 'Branded'
    LEGACY = 'FinalFood'


# class FoodNutrient(utils.DataClass):
#     pass


class BrandedFood(utils.DataClass):
    """
    Foods whose nutrient values are typically obtained from food label
    data provided by food brand owners.

    Attributes:
        fdc_id (int): ID of the food in the food table
        brand_owner: Brand owner for the food
        gtin_upc: GTIN or UPC code identifying the food
        ingredients: The list of ingredients (as it appears on the product label)
        serving_size (float): The amount of the serving size when expressed as gram or ml
        serving_size_unit: The unit used to express the serving size (gram or ml)
        household_serving_fulltext: amount and unit of serving size when
            expressed in household units
        branded_food_category: The category of the branded food, assigned
            by GDSN or Label Insight
        data_source: The source of the data for this food. GDSN (for GS1)
            or LI (for Label Insight).
        modified_date (datetime.date): This date reflects when the product data was last
            modified by the data provider, i.e., the manufacturer
        available_date (datetime.date): This is the date when the product record was
            available for inclusion in the database.
    """

    __attr__ = (
        # Excel
        ('fdc_id', int),
        ('brand_owner', str),
        ('gtin_upc', str),  # 11 digits of number (0-9)
        ('ingredients', str),  # csv (with spaces)
        ('serving_size', float),  # may be int
        ('household_serving_fulltext', str),  # cup
        ('branded_food_category', str),
        ('data_source', str),  # "LI"
        ('modified_date', datetime.date,
         parse_fooddata_date),
        ('available_date', datetime.date,
         parse_fooddata_date),
        # actual JSON
        ('foodClass', FoodClass),  # FoodClass.BRANDED
        ('food_nutrients', list),
        ('food_components', list),
        ('food_attributes', list),
        ('table_alias_name', str),  # "branded_food"
        ('serving_size_unit', str),  # lowercase g
        ('label_nutrients', dict),  # Dict[name, Dict["value", value]]
        ('data_type', FoodDataType),
        ('publication_date', datetime.date,
         parse_fooddata_date),
        ('food_portions', list),
        ('changes', str),
    )


class Food(utils.DataClass):
    """Any substance consumed by humans for nutrition, taste and/or aroma.

    Attributes:
        fdc_id (int): Unique permanent identifier of the food
        food_class (FoodClass): For internal use only
        data_type (FoodDataType): Type of food data
            (see Files tab for possible values).
        description (str): Description of the food
        food_category_id: Id of the food category the food belongs to
        publication_date (datetime.date): Date when the food was published to FoodData Central
        scientific_name (datetime.date): The scientific name for the food
        food_key: A string of characters used to identify both the
            current and all historical records for a specific food.
    """

    __attr__ = (
        ('fdc_id', int),
        ('food_class', FoodClass),
        ('data_type', FoodDataType),
        ('description', str),
        ('food_category_id', str),
        ('publication_date', datetime.date,
         parse_fooddata_date),
        ('scientific_name', str),
        ('food_key', str),
    )


class FoundationFood(utils.DataClass):
    """
    Foods whose nutrient and food component values are derived
    primarily by chemical analysis. Foundation data also include
    extensive underlying metadata, such as the number of samples,
    the location and dates on which samples were obtained, analytical
    approaches used, and if appropriate, cultivar, genotype, and
    production practices.

    Attributes:
        fdc_id (int): ID of the food in the food table
        NDB_number: Unique number assigned for the food, different from
            fdc_id, assigned in SR
        footnote (str): Comments on any unusual aspects. These are
            released to the public Examples might include unusual
            aspects of the food overall.
    """

    __attr__ = (
        ('fdc_id', int),
        ('NDB_number', str),  # temp
        ('footnote', str),
    )


class SrLegacyFood(utils.DataClass):
    """
    Foods from the April 2018 release of the USDA National Nutrient
    Database for Standard Reference. Nutrient and food component values
    are derived from chemical analysis and calculation.

    Attributes:
        fdc_id (int): ID of the food in the food table
        NDB_number: Unique number assigned for the food, different from
            fdc_id, assigned in SR

    """

    __attr__ = (
        ('fdc_id', int),
        ('NDB_number', str),  # temp
    )


class SurveyFnddsFood(utils.DataClass):
    """
    Foods whose consumption is measured by the What We Eat In America
    dietary survey component of the National Health and Nutrition
    Examination Survey (NHANES). Survey nutrient values are usually
    calculated from Branded and SR Legacy data.

    Attributes:
        fdc_id (int): ID of the food in the food table
        food_code (str): A unique ID identifying the food within FNDDS
        wweia_category_code: Unique Identification code for WWEIA food category to which this food is assigned
        start_date (datetime.date): Start date indicates time period corresponding to WWEIA data
        end_date (datetime.date): End date indicates time period corresponding to WWEIA data
    """

    __attr__ = (
        ('fdc_id', int),
        ('food_code', str),
        ('wweia_category_code', str),
        ('start_date', datetime.date,
         parse_fooddata_date),
        ('end_date', datetime.date,
         parse_fooddata_date),
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
