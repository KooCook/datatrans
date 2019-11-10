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

    for i in range(1, 5):
        criteria = fooddata.search.FoodSearchCriteria(
            general_search_input='',
            included_data_types={FoodDataType.LEGACY: True},
            page_number=i
        )
        res = fooddata.api.send_food_search_api_request(criteria)
        res = fooddata.search.response.FoodSearchResponse(res)
        for food in res.foods:
            if food.data_type is not FoodDataType.LEGACY:
                continue
            d = food.dict
            d['description'] = parse_description(d['description'])
            fields = ('fdc_id', 'common_names', 'description', '')
            ingr.append({field: d.get(utils.snake_to_camel(field), None) for field in fields})

    overwrite_file(ingr)


if __name__ == '__main__':
    # main()
    pass
