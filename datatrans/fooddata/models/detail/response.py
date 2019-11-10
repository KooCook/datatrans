import requests

from .food import FoodClass, FoundationFood, SurveyFnddsFood, BrandedFood, SrLegacyFood


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
            self.food = FoundationFood(_dict_=data)
        elif data['foodClass'] == FoodClass.SURVEY.value:
            self.food = SurveyFnddsFood(_dict_=data)
        elif data['foodClass'] == FoodClass.BRANDED.value:
            self.food = BrandedFood(_dict_=data)
        elif data['foodClass'] == FoodClass.LEGACY.value:
            self.food = SrLegacyFood(_dict_=data)
        else:
            raise ValueError('\'foodClass\' is not recognized')
