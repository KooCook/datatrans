"""

References:
    https://fdc.nal.usda.gov/api-guide.html#food-detail-endpoint
    https://fdc.nal.usda.gov/portal-data/external/dataDictionary
"""
import datetime
import enum
from typing import List, Dict, Union

from datatrans import utils
from datatrans.fooddata.search import FoodDataType
from datatrans.fooddata.models.detail.nutrient import FoodNutrient, NutrientConversionFactor
from datatrans.fooddata.models.detail.base import IdMixin


def parse_fooddata_date(date_str: str) -> datetime.date:
    """ Wrapper specific for fooddata's format """
    return utils.fooddata.parse_date(date_str, sep='/', format='MDY')


def parse_food_nutrients(data: List[Dict[str, Union[str, int, float]]]) -> List[FoodNutrient]:
    return [FoodNutrient(_dict_=d) for d in data]


def parse_label_nutrients(data: Dict[str, Dict[str, float]]) -> List[Dict[str, float]]:
    """ Change incoming data to be in list format. """
    return [{k: v['value']} for k, v in data.items()]


def parse_nutrient_conversion_factors(data: List[Dict[str, Union[str, float]]]) -> List[NutrientConversionFactor]:
    return [NutrientConversionFactor(_dict_=d) for d in data]


def parse_food_portions(data: List[Dict[str, Union[str, float, int]]]) -> List['FoodPortion']:
    return [FoodPortion(_dict_=d) for d in data]


class FoodClass(enum.Enum):
    FOUNDATION = 'FinalFood'
    SURVEY = 'Survey'
    BRANDED = 'Branded'
    LEGACY = 'FinalFood'


class FoodCategory(IdMixin, utils.DataClass):
    """Foods of defined similarity

    Attributes:
        id (int):
        code (str): Food group code
        description (str): Description of the food group
    """

    __slots__ = ('id', 'code', 'description')

    __attr__ = (
        ('id', int),
        ('code', str),
        ('description', str),
    )


class MeasureUnit(IdMixin, utils.DataClass):
    """units for measuring quantities of foods

    Attributes:
        id (int):
        name: name of the unit
        abbreviation: abbreviated name of the unit
    """

    __slots__ = ('id', 'name', 'abbreviation')

    __attr__ = (
        ('id', int),
        ('name', str),
        ('abbreviation', str),
    )


class FoodPortion(IdMixin, utils.DataClass):
    """Discrete amount of food

    Attributes:
        id (int):
        fdc_id: ID of the food this food portion pertains to

        seq_num: The order the measure will be displayed on the released food.
        amount: The number of measure units that comprise the measure (e.g. if measure is 3 tsp, the amount is 3). Not defined for survey (FNDDS) foods (amount is instead embedded in portion description).
        measure_unit: The unit used for the measure (e.g. if measure is 3 tsp, the unit is tsp). For food types that do not use measure SR legacy foods and survey (FNDDS) foods), a value of '9999' is assigned to this field.
        portion_description: Foundation foods: Comments that provide more specificity on the measure. For example, for a pizza measure the dissemination text might be 1 slice is 1/8th of a 14 inch pizza"."   Survey (FNDDS) foods: The household description of the portion.
        modifier: Foundation foods: Qualifier of the measure (e.g. related to food shape or form)  (e.g. melted, crushed, diced). Survey (FNDDS) foods: The portion code. SR legacy foods: description of measures, including the unit of measure and the measure modifier (e.g. waffle round (4" dia)).
        gram_weight: The weight of the measure in grams
        data_points: The number of observations on which the measure is based
        footnote: Comments on any unusual aspects of the measure. These are released to the public. Examples might include caveats on the usage of a measure, or reasons why a measure gram weight is an unexpected value.
        min_year_acquired: Minimum purchase year of all acquisitions used to derive the measure value
    """

    __slots__ = ('id', 'measure_unit', 'modifier', 'gram_weight', 'data_points', 'amount', 'sequence_number')

    __attr__ = (
        ('id', int),
        ('measure_unit', MeasureUnit),
        ('modifier', str),
        ('gram_weight', float),
        ('data_points', int),
        ('amount', float),
        ('sequence_number', int),
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

    __slots__ = ('fdc_id', 'brand_owner', 'gtin_upc', 'ingredients', 'serving_size', 'household_serving_full_text',
                 'branded_food_category', 'data_source', 'modified_date', 'available_date', 'foodClass', 'description',
                 'food_nutrients', 'food_components', 'food_attributes', 'table_alias_name', 'serving_size_unit',
                 'label_nutrients', 'data_type', 'publication_date', 'food_portions', 'changes')

    __attr__ = (
        # Excel
        ('fdc_id', int),
        ('brand_owner', str),
        ('gtin_upc', str),  # 11 digits of number (0-9)
        ('ingredients', str),  # csv (with spaces)
        ('serving_size', float),  # may be int
        ('household_serving_full_text', str),  # cup
        ('branded_food_category', str),
        ('data_source', str),  # "LI"
        ('modified_date', datetime.date,
         parse_fooddata_date),
        ('available_date', datetime.date,
         parse_fooddata_date),
        # actual JSON
        ('foodClass', FoodClass),  # FoodClass.BRANDED
        ('description', str),
        ('food_nutrients', list,
         parse_food_nutrients),
        ('food_components', list),
        ('food_attributes', list),
        ('table_alias_name', str),  # "branded_food"
        ('serving_size_unit', str),  # lowercase g
        ('label_nutrients', list,  # type: List[Dict[str, float]]
         parse_label_nutrients),
        ('data_type', FoodDataType),
        ('publication_date', datetime.date,
         parse_fooddata_date),
        ('food_portions', list,  # type: List[FoodPortion]
         parse_food_portions),
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

    __slots__ = (
    'fdc_id', 'description', 'data_type', 'published_date', 'all_highlight_fields', 'score', 'food_code', 'gtin_upc',
    'brand_owner', 'additional_descriptions')

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

    __slots__ = (
    'ndb_number', 'fdc_id', 'foodClass', 'description', 'food_nutrients', 'food_components', 'food_attributes',
    'table_alias_name', 'nutrient_conversion_factors', 'is_historical_reference', 'data_type', 'data_type',
    'food_category', 'food_portions', 'input_foods', 'publication_date', 'changes')

    __attr__ = (
        # Excel
        ('ndb_number', str),
        ('fdc_id', int),
        # actual JSON
        ('food_class', FoodClass),
        ('description', str),
        ('food_nutrients', list,  # type: List[FoodNutrient]
         parse_food_nutrients),
        ('food_components', list),
        ('food_attributes', list),
        ('table_alias_name', str),
        ('nutrient_conversion_factors', list,  # type: List[NutrientConversionFactor]
         parse_nutrient_conversion_factors),
        ('is_historical_reference', bool),
        ('data_type', FoodDataType),
        ('food_category', FoodCategory),
        ('food_portions', list,  # type: List[FoodPortion]
         parse_food_portions),
        ('input_foods', list),
        ('publication_date', datetime.date,
         parse_fooddata_date),
        ('changes', str),
    )

    def __init__(self, _dict_: dict = None, **kwargs):
        super().__init__(_dict_, **kwargs)
        if self.food_class is not FoodClass.LEGACY:
            raise ValueError('invalid value for \'{}\': \'{}\' \'{}\''
                             .format(self.__class__.__name__, 'food_class', self.food_class))
        if self.data_type is not FoodDataType.LEGACY:
            raise ValueError('invalid value for \'{}\': \'{}\' \'{}\''
                             .format(self.__class__.__name__, 'data_type', self.data_type))
        if self.table_alias_name != 'sr_legacy_food':
            raise ValueError('invalid value for \'{}\': \'{}\' \'{}\''
                             .format(self.__class__.__name__, 'table_alias_name', self.table_alias_name))


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
