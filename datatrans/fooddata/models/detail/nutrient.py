from datatrans import utils


class Nutrient(utils.DataClass):

    __slots__ = ('rank', 'unit_name', 'id', 'name', 'number')

    __attr__ = {
        ('id', int),
        ('number', str),
        ('name', str),
        ('rank', int),
        ('unit_name', str),
    }


class FoodNutrientSource(utils.DataClass):

    __slots__ = ('id', 'code', 'description')

    __attr__ = (
        ('id', int),
        ('code', str),
        ('description', str),
    )


class FoodNutrientDerivation(utils.DataClass):

    __slots__ = ('description', 'food_nutrient_source', 'code', 'id')

    __attr__ = {
        ('id', int),
        ('code', str),  # LCCD
        ('description', str),
        ('food_nutrient_source', FoodNutrientSource),
    }


class FoodNutrient(utils.DataClass):
    
    __slots__ = ('type', 'id', 'nutrient', 'food_nutrient_derivation', 'amount')

    __attr__ = (
        ('type', str),  # FoodNutrient
        ('id', int),
        ('nutrient', Nutrient),
        ('food_nutrient_derivation', FoodNutrientDerivation),
        ('amount', float),
    )
