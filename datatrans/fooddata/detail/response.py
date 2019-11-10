import requests

from datatrans.fooddata.search.request import FoodDataType
from .food import FoodClass, FoundationFood, SurveyFnddsFood, BrandedFood, SrLegacyFood


class FoodDetailResponse:
    """ FoodData Detail endpoint Response handler. """

    __slots__ = (
        'response',
        'food',
    )

    def __init__(self, response: requests.Response, **kwargs):
        """

        Args:
            response: The Response returned by the FoodData Detail endpoint
        """
        self.response = response

        data = response.json()
        if data['foodClass'] == FoodClass.FOUNDATION.value:
            data_type = kwargs.pop('data_type', None)
            if data_type:
                if data_type is FoodDataType.LEGACY:
                    self.food = SrLegacyFood(_dict_=data)
                    return
                if data_type is FoodDataType.FOUNDATION:
                    self.food = FoundationFood(_dict_=data)
                    return
            try:
                self.food = SrLegacyFood(_dict_=data)
            except ValueError as e:
                try:
                    self.food = FoundationFood(_dict_=data)
                except ValueError as ee:
                    raise ee from e
        elif data['foodClass'] == FoodClass.SURVEY.value:
            self.food = SurveyFnddsFood(_dict_=data)
        elif data['foodClass'] == FoodClass.BRANDED.value:
            self.food = BrandedFood(_dict_=data)
        else:
            raise ValueError('\'foodClass\' is not recognized')
