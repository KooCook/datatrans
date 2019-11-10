import enum

from datatrans import utils
from datatrans.fooddata.models.detail.base import IdMixin


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


    
    __slots__ = ('type', 'id', 'nutrient', 'food_nutrient_derivation', 'amount')
class FoodNutrient(IdMixin, utils.DataClass):

    __attr__ = (
        ('type', str),  # FoodNutrient
        ('id', int),
        ('nutrient', Nutrient),
        ('food_nutrient_derivation', FoodNutrientDerivation),
        ('amount', float),
    )


class NutrientConversionFactorType(enum.Enum):
    PROTEIN = '.ProteinConversionFactor'
    CALORIE = '.CalorieConversionFactor'


class NutrientConversionFactor(IdMixin, utils.DataClass):
    __attr__ = (
        ('type', NutrientConversionFactorType),
        ('id', int),
        ('name', str),
        ('protein_value', float),
        ('fat_value', float),
        ('carbohydrate_value', float),
    )
