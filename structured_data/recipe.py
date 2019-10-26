"""
https://developers.google.com/search/docs/data-types/recipe
"""
from typing import Union, Optional

from structured_data.base import Thing, Number
from structured_data.lower.quantity import Energy, EnergyUnit, Mass, MassUnit


class NutritionInformation(Thing):
    """
    Nutritional information about the recipe

    Required properties:
        calories: Energy
            The number of calories.

    Properties:
        carbohydrateContent: Mass
            The number of grams of carbohydrates.
        cholesterolContent: Mass
            The number of milligrams of cholesterol.
        fatContent: Mass
            The number of grams of fat.
        fiberContent: Mass
            The number of grams of fiber.
        proteinContent: Mass
            The number of grams of protein.
        saturatedFatContent: Mass
            The number of grams of saturated fat.
        servingSize: Mass
            The serving size, in terms of the number of volume or mass.
        sodiumContent: Mass
            The number of milligrams of sodium.
        sugarContent: Mass
            The number of grams of sugar.
        transFatContent: Mass
            The number of grams of trans fat.
        unsaturatedFatContent: Mass
            The number of grams of unsaturated fat.

    https://schema.org/NutritionInformation
    """

    PROPERTIES = (
        # required
        'calories',
        # optional
        'servingSize',
        'carbohydrateContent',
        'cholesterolContent',
        'fatContent',
        'fiberContent',
        'proteinContent',
        'saturatedFatContent',
        'sodiumContent',
        'sugarContent',
        'transFatContent',
        'unsaturatedFatContent',
    )

    def __init__(self, *, calories: Union[Energy, Number], **kwargs):
        if isinstance(calories, Number):
            calories = Energy(calories, EnergyUnit.CALORIE)
        self._calories: Energy = calories


if __name__ == '__main__':
    pass
