from datatrans import utils
from datatrans.fooddata.detail.base import IdMixin
from datatrans.utils.classes import JSONEnum as Enum


class Nutrient(IdMixin, utils.DataClass):
    __slots__ = ('rank', 'unit_name', 'id', 'name', 'number')

    __attr__ = {
        ('id', int),
        ('number', str),
        ('name', str),
        ('rank', int),
        ('unit_name', str),
    }


class FoodNutrientSource(IdMixin, utils.DataClass):
    __slots__ = ('id', 'code', 'description')

    __attr__ = (
        ('id', int),
        ('code', str),
        ('description', str),
    )


class FoodNutrientDerivation(IdMixin, utils.DataClass):
    __slots__ = ('description', 'food_nutrient_source', 'code', 'id')

    __attr__ = {
        ('id', int),
        ('code', str),  # LCCD
        ('description', str),
        ('food_nutrient_source', FoodNutrientSource),
    }


class FoodNutrient(IdMixin, utils.DataClass):
    """A nutrient value for a food

    Attributes:
        id
        fdc_id: ID of the food this food nutrient pertains to
        nutrient: Nutrient to which the food nutrient pertains
        amount: Amount of the nutrient per 100g of food.
            Specified in unit defined in the nutrient table.
        data_points: Number of observations on which the value is based
        derivation_id: ID of the food nutrient derivation technique
            used to derive the value
        standard_error: Standard error
        min: The minimum amount
        max: The maximum amount
        median: The median amount
        footnote: Comments on any unusual aspects of the food nutrient.
            Examples might include why a nutrient value is different
            than typically expected.
        min_year_acquired: Minimum purchase year of all acquisitions
            used to derive the nutrient value
        nutrient_analysis_details: Details of the analysis of the
            nutrient (API only)
    """

    __slots__ = ('type', 'id', 'nutrient', 'data_points', 'min', 'food_nutrient_derivation', 'max', 'min', 'amount')

    __attr__ = (
        ('type', str),  # FoodNutrient
        ('id', int),
        ('nutrient', Nutrient),
        ('data_points', int),
        ('min', float),
        ('food_nutrient_derivation', FoodNutrientDerivation),
        ('max', float),
        ('min', float),
        ('amount', float),
    )


class NutrientConversionFactorType(Enum):
    PROTEIN = '.ProteinConversionFactor'
    CALORIE = '.CalorieConversionFactor'


class NutrientConversionFactor(IdMixin, utils.DataClass):
    __attr__ = (
        ('type', NutrientConversionFactorType),
        ('id', int),
        ('name', str),
        ('value', float),
        ('protein_value', float),
        ('fat_value', float),
        ('carbohydrate_value', float),
    )
