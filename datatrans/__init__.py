import enum
import json
from pathlib import Path
import warnings

import structured_data as schema
from datatrans.utils import BASE_DIR


@enum.unique
class DataSet(enum.Enum):
    ALLRECIPES = BASE_DIR / 'assets/allrecipes-recipes.json'
    BBCCOUK = BASE_DIR / 'assets/bbccouk-recipes.json'
    COOKSTR = BASE_DIR / 'assets/cookstr-recipes.json'
    EPICURIOUS = BASE_DIR / 'assets/epicurious-recipes.json'


if __name__ == '__main__':
    data_set = DataSet.EPICURIOUS

    with Path(data_set.value).open('r', encoding='utf-8') as jsonfile:
        counter = 1
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
                    )
                }

                if data['reviewsCount'] != 0:
                    d['aggregateRating'] = schema.AggregateRating(
                        ratingValue=data['aggregateRating'],
                        reviewCount=data['reviewsCount']
                    )

                if data['author']:
                    d['author'] = schema.Property(*[schema.Person(author['name'])
                                                    for author in data['author']])

                try:
                    d['recipeIngredient'] = schema.Property(*data['ingredients'])
                except KeyError as e:
                    warnings.warn('KeyError: {} in line#{}'.format(e, counter))
                    try:
                        if data['tag']['category'] == 'ingredient':
                            d['recipeIngredient'] = data['tag']['name']
                    except KeyError as e:
                        warnings.warn('KeyError: {} in line#{}'.format(e, counter))

                try:
                    if data['tag']['category'] == 'cuisine':
                        d['recipeCuisine'] = data['tag']['name']
                except KeyError as e:
                    warnings.warn('KeyError: {} in line#{}'.format(e, counter))
            elif data_set is DataSet.ALLRECIPES:
                d = {
                    'author': schema.Person(data['author']),
                    'description': data['description'],
                    'recipeIngredient': schema.Property(*data['ingredients']),
                    'recipeInstructions': schema.Property(*data['instructions']),
                    'name': data['title']
                }
                if data['prep_time_minutes'] != 0 or data['cook_time_minutes'] != 0:
                    d['prepTime'] = schema.Duration(minutes=data['prep_time_minutes'])
                    d['cookTime'] = schema.Duration(minutes=data['cook_time_minutes'])
                if data['total_time_minutes'] != 0:
                    d['totalTime'] = schema.Duration(minutes=data['total_time_minutes'])
                if data['review_count']:
                    d['aggregateRating'] = schema.AggregateRating(
                        ratingValue=data['rating_stars'],
                        reviewCount=data['review_count']
                    )
            elif data_set is DataSet.BBCCOUK:
                d = {
                    'author': schema.Person(data['chef']),
                    'recipeIngredient': schema.Property(*data['ingredients']),
                    'recipeInstructions': schema.Property(*data['instructions']),
                    'name': data['title']

                }
                if data['description']:
                    d['description'] = data['description']
                if data['preparation_time_minutes'] != 0 or data['cooking_time_minutes'] != 0:
                    d['prepTime'] = schema.Duration(minutes=data['preparation_time_minutes'])
                    d['cookTime'] = schema.Duration(minutes=data['cooking_time_minutes'])
                if data['total_time_minutes'] != 0:
                    d['totalTime'] = schema.Duration(minutes=data['total_time_minutes'])

                # TODO: Also include serving size 'serve' into the data

            elif data_set is DataSet.COOKSTR:
                d = {
                    'author': schema.Person(data['chef']),
                    'cookingMethod': data['cooking_method'],
                    'datePublished': data['date_modified'],
                    'recipeIngredient': schema.Property(*data['ingredients']),
                    'recipeInstructions': schema.Property(*data['instructions']),
                    'name': data['title']
                }
                if data['description']:
                    d['description'] = data['description']
                if data['rating_count']:
                    d['aggregateRating'] = schema.AggregateRating(
                        ratingValue=data['rating_value'],
                        ratingCount=data['rating_count']
                    )

            recipe = schema.Recipe(
                **d,
                suppress=True
            )

            recipes.append(recipe)
            counter += 1
            # if counter > 10:
            #     break

    with open(BASE_DIR / 'assets/epicurious-recipes.json-ld', 'w') as jsonfile:
        for recipe in recipes:
            jsonfile.write(json.dumps(recipe, default=schema.utils.default))
            jsonfile.write('\n')

    # print(json.dumps(recipes, default=schema.utils.default))
