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


class FoodCategoryInstance(Enum):
    DAIRY_AND_EGG_PRODUCTS = FoodCategory(_dict_={'id': 1, 'code': '0100', 'description': 'Dairy and Egg Products'})
    SPICES_AND_HERBS = FoodCategory(_dict_={'id': 2, 'code': '0200', 'description': 'Spices and Herbs'})
    BABY_FOODS = FoodCategory(_dict_={'id': 3, 'code': '0300', 'description': 'Baby Foods'})
    FATS_AND_OILS = FoodCategory(_dict_={'id': 4, 'code': '0400', 'description': 'Fats and Oils'})
    POULTRY_PRODUCTS = FoodCategory(_dict_={'id': 5, 'code': '0500', 'description': 'Poultry Products'})
    SOUPS, _SAUCES, _AND_GRAVIES = FoodCategory(
        _dict_={'id': 6, 'code': '0600', 'description': 'Soups, Sauces, and Gravies'})
    SAUSAGES_AND_LUNCHEON_MEATS = FoodCategory(
        _dict_={'id': 7, 'code': '0700', 'description': 'Sausages and Luncheon Meats'})
    BREAKFAST_CEREALS = FoodCategory(_dict_={'id': 8, 'code': '0800', 'description': 'Breakfast Cereals'})
    FRUITS_AND_FRUIT_JUICES = FoodCategory(_dict_={'id': 9, 'code': '0900', 'description': 'Fruits and Fruit Juices'})
    PORK_PRODUCTS = FoodCategory(_dict_={'id': 10, 'code': '1000', 'description': 'Pork Products'})
    VEGETABLES_AND_VEGETABLE_PRODUCTS = FoodCategory(
        _dict_={'id': 11, 'code': '1100', 'description': 'Vegetables and Vegetable Products'})
    NUT_AND_SEED_PRODUCTS = FoodCategory(_dict_={'id': 12, 'code': '1200', 'description': 'Nut and Seed Products'})
    BEEF_PRODUCTS = FoodCategory(_dict_={'id': 13, 'code': '1300', 'description': 'Beef Products'})
    BEVERAGES = FoodCategory(_dict_={'id': 14, 'code': '1400', 'description': 'Beverages'})
    FINFISH_AND_SHELLFISH_PRODUCTS = FoodCategory(
        _dict_={'id': 15, 'code': '1500', 'description': 'Finfish and Shellfish Products'})
    LEGUMES_AND_LEGUME_PRODUCTS = FoodCategory(
        _dict_={'id': 16, 'code': '1600', 'description': 'Legumes and Legume Products'})
    LAMB, _VEAL, _AND_GAME_PRODUCTS = FoodCategory(
        _dict_={'id': 17, 'code': '1700', 'description': 'Lamb, Veal, and Game Products'})
    BAKED_PRODUCTS = FoodCategory(_dict_={'id': 18, 'code': '1800', 'description': 'Baked Products'})
    SWEETS = FoodCategory(_dict_={'id': 19, 'code': '1900', 'description': 'Sweets'})
    CEREAL_GRAINS_AND_PASTA = FoodCategory(_dict_={'id': 20, 'code': '2000', 'description': 'Cereal Grains and Pasta'})
    FAST_FOODS = FoodCategory(_dict_={'id': 21, 'code': '2100', 'description': 'Fast Foods'})
    MEALS, _ENTREES, _AND_SIDE_DISHES = FoodCategory(
        _dict_={'id': 22, 'code': '2200', 'description': 'Meals, Entrees, and Side Dishes'})
    SNACKS = FoodCategory(_dict_={'id': 23, 'code': '2500', 'description': 'Snacks'})
    AMERICAN_INDIAN_ALASKA_NATIVE_FOODS = FoodCategory(
        _dict_={'id': 24, 'code': '3500', 'description': 'American Indian/Alaska Native Foods'})
    RESTAURANT_FOODS = FoodCategory(_dict_={'id': 25, 'code': '3600', 'description': 'Restaurant Foods'})
    BRANDED_FOOD_PRODUCTS_DATABASE = FoodCategory(
        _dict_={'id': 26, 'code': '4500', 'description': 'Branded Food Products Database'})
    QUALITY_CONTROL_MATERIALS = FoodCategory(
        _dict_={'id': 27, 'code': '2600', 'description': 'Quality Control Materials'})
    ALCOHOLIC_BEVERAGES = FoodCategory(_dict_={'id': 28, 'code': '1410', 'description': 'Alcoholic Beverages'})


def write_to_file(data):
    file = DATA_DIR / 'ingredients.json'
    with file.open('w') as f:
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
    
    write_to_file(ingr)


if __name__ == '__main__':
    # main()
    pass
