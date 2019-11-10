import json

from datatrans import utils
from datatrans.utils.classes import JSONEnum as Enum
from datatrans.fooddata.detail import *
from datatrans import fooddata
from datatrans.fooddata.search import *

DATA_DIR = utils.BASE_DIR / 'assets'


def print_food_category_instances_code():
    with (DATA_DIR / 'food-categories.csv').open('r') as csvfile:
        lines = csvfile.read().splitlines()
        for line in lines:
            parts = line.split('\t')
            print(f"{utils.to_constant(parts[2])} = FoodCategory(_dict_={{'id': {parts[0]}, 'code': '{parts[1]}', 'description': '{parts[2]}'}})")


def overwrite_file(data):
    file = DATA_DIR / 'ingredients.json'
    with file.open('w') as f:
        f.write(json.dumps(data, cls=utils.JSONEncoder))


def append_file(data):
    file = DATA_DIR / 'ingredients.json'
    with file.open('a') as f:
        f.write(json.dumps(data, cls=utils.JSONEncoder))


def parse_description(description: str) -> str:
    """ Make an effort to make the description more human """
    if 'Alcoholic beverage, ' in description:
        return description[20:]
    if 'Alcoholic beverages, ' in description:
        return description[21:]
    return description


def main():
    ingr = []
    ignored_category = (
        FoodCategoryInstance.RESTAURANT_FOODS.value,
        FoodCategoryInstance.MEALS_ENTREES_AND_SIDE_DISHES.value,
        FoodCategoryInstance.BABY_FOODS.value,
        FoodCategoryInstance.SOUPS_SAUCES_AND_GRAVIES.value,
        FoodCategoryInstance.FAST_FOODS.value,
        FoodCategoryInstance.SNACKS.value,  # Could be used, but ignore for now
        FoodCategoryInstance.FAST_FOODS.value,
    )

    for i in range(1, 2):
        criteria = fooddata.search.FoodSearchCriteria(
            general_search_input='',
            included_data_types={FoodDataType.LEGACY: True},
            page_number=i
        )
        search_res = fooddata.api.send_food_search_api_request(criteria)
        search_res = fooddata.search.response.FoodSearchResponse(search_res)
        for food in search_res.foods:
            if food.data_type is not FoodDataType.LEGACY:
                continue
            detail_res = fooddata.api.send_food_detail_api_request(food.fdc_id)
            detail_res = fooddata.detail.response.FoodDetailResponse(detail_res, data_type=FoodDataType.LEGACY)
            food_: fooddata.detail.SrLegacyFood = detail_res.food
            if food_.food_category in ignored_category:
                continue
            ingr.append(
                {
                    'fdc_id': food_.fdc_id,
                    'common_names': food_.common_names,
                    'description': food_.description,
                }
            )

    overwrite_file(ingr)


if __name__ == '__main__':
    main()
    pass
