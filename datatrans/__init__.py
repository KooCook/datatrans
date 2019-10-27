import enum
import json
from pathlib import Path

import structured_data as schema
from datatrans.utils import BASE_DIR


@enum.unique
class DataSet(enum.Enum):
    ALLRECIPES = BASE_DIR / 'assets/allrecipes-recipes.json'
    BBCCOUK = BASE_DIR / 'assets/bbccouk-recipes.json'
    COOKSTR = BASE_DIR / 'assets/cookstr-recipes.json'
    EPICURIOUS = BASE_DIR / 'assets/epicurious-recipes.json'


if __name__ == '__main__':
    data_set = DataSet.BBCCOUK

    with Path(data_set.value).open('r', encoding='utf-8') as jsonfile:
        counter = 0
        recipes = []
        for line in jsonfile:
            data = json.loads(line)

            if data_set is DataSet.EPICURIOUS:
                d = {
                    'datePublished': schema.DateTime.fromisoformat(data['pubDate']),
                    'name': data['hed'],
                    'recipeInstructions': schema.Property(*data['prepSteps']),
                    'aggregateRating': schema.AggregateRating(
                        ratingValue=data['aggregateRating'],
                        reviewCount=data['reviewsCount']
                    ),
                    'recipeIngredient': schema.Property(*data['ingredients']),
                    'recipeCuisine': data['tag']['name']
                }
                if data['author']:
                    d['author'] = schema.Property(*[schema.Person(author['name'])
                                                    for author in data['author']])
            elif data_set is DataSet.ALLRECIPES:
                d = {
                    'author': schema.Person(data['author']),
                    'description': data['description'],
                    'recipeIngredient': schema.Property(*data['ingredients']),
                    'recipeInstructions': schema.Property(*data['instructions']),
                    'name': data['title']
                }
                if data['prep_time_minutes']:
                    d['prepTime'] = schema.Duration(minutes=data['prep_time_minutes'])
                if data['cook_time_minutes']:
                    d['cookTime'] = schema.Duration(minutes=data['cook_time_minutes'])
                if data['total_time_minutes']:
                    d['totalTime'] = schema.Duration(minutes=data['total_time_minutes'])
                if data['review_count']:
                    d['aggregateRating'] = schema.AggregateRating(
                        ratingValue=data['rating_stars'],
                        reviewCount=data['review_count']
                    ),
            elif data_set is DataSet.BBCCOUK:
                d = {
                    'author': schema.Person(data['chef']),
                    'cookTime': schema.Duration(minutes=data['cooking_time_minutes']),
                    'recipeIngredient': schema.Property(*data['ingredients']),
                    'recipeInstructions': schema.Property(*data['instructions']),
                    'name': data['title']

                }
                if data['description']:
                    d['description'] = data['description']
                if data['preparation_time_minutes']:
                    d['prepTime'] = schema.Duration(minutes=data['preparation_time_minutes'])
                if data['cooking_time_minutes']:
                    d['cookTime'] = schema.Duration(minutes=data['cooking_time_minutes'])
                if data['total_time_minutes']:
                    d['totalTime'] = schema.Duration(minutes=data['total_time_minutes'])

                # TODO: Also include serving size 'serve' into the data

            elif data_set is DataSet.COOKSTR:
                pass

            recipe = schema.Recipe(
                **d,
                suppress=True
            )

            recipes.append(recipe)
            counter += 1
            if counter > 10:
                break

    with open(BASE_DIR / 'assets/out.json-ld', 'w') as jsonfile:
        for recipe in recipes:
            jsonfile.write(json.dumps(recipe, default=schema.utils.default))
            jsonfile.write('\n')

    print(json.dumps(recipes, default=schema.utils.default))
