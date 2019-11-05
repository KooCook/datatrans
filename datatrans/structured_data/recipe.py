"""

References:
    https://developers.google.com/search/docs/data-types/recipe
"""
import warnings
from typing import Iterable, Optional, Union

from datatrans.structured_data.base import URL, Date, Number, Property, Text, Thing
from datatrans.structured_data.lower.quantity import Duration, Energy, EnergyUnit
from datatrans.structured_data.person import Person
from datatrans.structured_data.review import AggregateRating
from datatrans.structured_data.video import VideoObject


class NutritionInformation(Thing):
    """Nutritional information about the recipe

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

    References:
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


class Recipe(Thing):
    """Schema.org's Recipe, as specified by Google

    Required properties:
        image: URL, ImageObject
            Image of the completed dish.

            Additional image guidelines:
              - Every page must contain at least one image (whether or not you include markup). Google will pick the best image to display in Search results based on the aspect ratio and resolution.
              - Image URLs must be crawlable and indexable.
              - Images must represent the marked up content.
              - Images must be in .jpg, .png, or. gif format.
              - For best results, provide multiple high-resolution images (minimum of 50K pixels when multiplying width and height) with the following aspect ratios: 16x9, 4x3, and 1x1.
            For example:
            ```
            "image": [
              "https://example.com/photos/1x1/photo.jpg",
              "https://example.com/photos/4x3/photo.jpg",
              "https://example.com/photos/16x9/photo.jpg"
            ]
            ```
        name: Text
            The name of the dish.

    Recommended properties:
        aggregateRating: AggregateRating
            Annotation for the average review score assigned to the item.
            Follow the Review snippet guidelines and list of required
            and recommended AggregateRating properties.
            If the recipe structured data contains a single review, the
            reviewer’s name must be a valid person or organization.
            For example, "50% off ingredients" is not a valid name for
            a reviewer.
        author: Person
            Creator of the recipe.
        cookTime: Duration
            The time it takes to actually cook the dish in ISO 8601
            format. You can use min and max as child elements to
            specify a range of time.
            Always use in combination with prepTime.
        datePublished: Date
            The date the recipe was published in ISO 8601 format.
        description: Text
            A short summary describing the dish.
        keywords: Text
            Other terms for your recipe such as the season ("summer"),
            the holiday ("Halloween"), or other descriptors
            ("quick", "easy", "authentic").
            Additional guidelines:
              - Separate multiple entries in a keywords list with commas.
              - Don't use a tag that should be in ``recipeCategory``
                or ``recipeCuisine``.
            Not recommended:
                "keywords": "dessert, American"
            Recommended:
                "keywords": "winter apple pie, nutmeg crust"
        nutrition.calories: Energy
            The number of calories in each serving.
        prepTime: Duration
            The length of time it takes to prepare the dish, in ISO
            8601 format. You can use min and max as child elements to
            specify a range of time.
            Always use in combination with cookTime.
        recipeCategory: Text
            The type of meal or course your recipe is about.
            For example: "dinner", "entree", or "dessert, snack".
        recipeCuisine: Text
            The region associated with your recipe. For example,
            "French", Mediterranean", or "American".
        recipeIngredient: Text
            An ingredient used in the recipe. This property is
            recommended for recipes on Google Search, but it's required
            for guidance with the Google Assistant on Google Home and
            mart displays.
            Additional guidelines:
              - Include only the ingredient text that is necessary for
                making the recipe.
              - Don't include unnecessary information, such as a
                definition of the ingredient.
        recipeInstructions: Text
            The steps to make the dish. This property is recommended
            for recipes on Google Search, but it's required for
            guidance with the Google Assistant on Google Home and smart
            displays.
            There are several options for setting the value of
            ``recipeInstructions``.
            We recommend using ``HowToStep`` or ``HowToSection``:
              - HowToStep: You can specify the exact text for each step
                sentence by setting the value of each HowToStep. This
                provides hints to the Google Assistant, but note it may
                group the recipe steps differently based on the context.
              - HowToSection (only if a recipe has multiple sections):
                Use to group steps into multiple sections. Provide the
                section name in its name property (for example, "Make the
                crust") and specify each HowToStep as an itemListElement.
                Set the text property of each HowToStep.
                For example, a pizza recipe may have one section of steps
                for making the crust, one for preparing the toppings, and
                one for combining and baking. If you don't indicate
                multiple sections, the Google Assistant may mistakenly
                present the section name as just another step (for example,
                a "Make the crust" step followed by a "Combine the
                flour and yeast" step).
              - Single or repeated property of text: A block of text
                that includes one or more steps. Google treats all steps
                as being in a single section. Repeated property values
                are concatenated into a single block of text. Google
                then attempts to automatically split the single block
                of text into individual steps. Google tries to find and
                remove any section names, step numbers, keywords, and
                anything else that can incorrectly appear in recipe step
                text. For best results, we recommend you unambiguously
                specify individual step sentences with HowToStep, as
                described above.
            Additional guidelines
              - Don't include metadata that belongs elsewhere.
                In particular, use the author property to specify the
                author, recipeCuisine for cuisine, recipeCategory for
                category, and keywords for other keywords.
              - Include only text on how to make the recipe and don't
                include other text such as "Directions", "Watch the video",
                "Step 1". Those phrases should be specified outside of
                the structured data.
        recipeYield: Text
            The quantity produced by the recipe.
            For example: number of people served, or number of servings.
        totalTime: Duration
            The total time it takes to prepare the cook the dish, in
            ISO 8601 format. You can use min and max as child elements
            to specify a range of time.
            Use totalTime or a combination of both cookTime and prepTime.
        video: VideoObject
            An array of video properties that depict the recipe on the page.
            Follow the list of required and recommended Video properties.
    """
    PROPERTIES = (
        # required
        'name',
        'image',
        # recommended
        'author',
        'datePublished',
        'description',
        'prepTime',
        'cookTime',
        'totalTime',
        'keywords',
        'recipeYield',
        'recipeCategory',
        'recipeCuisine',
        'nutrition',
        'recipeIngredient',
        'recipeInstructions',
        'aggregateRating',
        'video',
        # optional
        'cookingMethod',
    )

    def __init__(
            self,
            *,
            image: Iterable[Union[URL, str]] = None,
            name: Text = None,
            aggregateRating: Optional[AggregateRating] = None,
            author: Optional[Person] = None,
            cookTime: Optional[Duration] = None,
            datePublished: Optional[Date] = None,
            description: Optional[Text] = None,
            keywords: Optional[Text] = None,
            nutrition: Optional[NutritionInformation] = None,
            prepTime: Optional[Duration] = None,
            recipeCategory: Optional[Text] = None,
            recipeCuisine: Optional[Text] = None,
            recipeIngredient: Optional[Iterable[Text]] = None,
            recipeInstructions: Optional[Iterable[Text]] = None,  # TODO
            recipeYield: Optional[Text] = None,
            totalTime: Optional[Duration] = None,
            video: Optional[VideoObject] = None,
            **kwargs):
        suppress = kwargs.pop('suppress', False)
        if image is None:
            self._image = None
            if suppress:
                warnings.warn('Warning: required property \'image\' unfilled')
            else:
                raise ValueError('required property \'image\' unfilled')
        else:
            self._image: Property[URL] = Property(*image, class_=URL)
        if name is None:
            self._name = None
            if suppress:
                warnings.warn('Warning: required property \'name\' unfilled')
            else:
                raise ValueError('required property \'name\' unfilled')
        else:
            self._name: Text = name
        self._aggregate_rating = aggregateRating
        self._author = author
        self._cook_time = cookTime
        self._date_published = datePublished
        self._description = description
        self._keywords = keywords
        self._nutrition = nutrition
        self._prep_time = prepTime
        self._recipe_category = recipeCategory
        self._recipe_cuisine = recipeCuisine
        self._recipe_ingredient = recipeIngredient
        self._recipe_instructions = recipeInstructions
        self._recipe_yield = recipeYield
        self._total_time = totalTime
        self._video = video
        self._cooking_method = kwargs.pop('cookingMethod', None)


if __name__ == '__main__':
    import json
    from datatrans.structured_data import utils

    print(
        json.dumps(NutritionInformation(calories=1024, ),
                   default=utils.default))

    print(
        json.dumps(Recipe(
            image=[
                "https://example.com/photos/1x1/photo.jpg",
                "https://example.com/photos/4x3/photo.jpg",
                "https://example.com/photos/16x9/photo.jpg"
            ],
            name='Coffee Cake',
            author=Person('Mary Stone'),
            datePublished=Date(2018, 3, 10),
            description="This coffee cake is awesome and perfect for parties.",
            prepTime=Duration(0, 20 * 60),
            # cookTime=Duration(0, 30 * 60),
            totalTime=Duration(0, 50 * 60),
            keywords="cake for a party, coffee",
            recipeYield='10 servings',
            recipeCategory='Dessert',
            recipeCuisine='American',
            recipeIngredient=[
                '2 cups of flour',
                '3/4 cup white sugar',
                '2 teaspoons baking powder',
                '1/2 teaspoon salt',
                '1/2 cup butter',
                '2 eggs',
                '3/4 cup milk',
            ],
            recipeInstructions=[
                'Preheat the oven to 350 degrees F. Grease and flour a 9x9 inch pan.',
                'In a large bowl, combine flour, sugar, baking powder, and salt.',
                'Mix in the butter, eggs, and milk.',
                'Spread into the prepared pan.',
                'Bake for 30 to 35 minutes, or until firm.',
                'Allow to cool.',
            ],
            aggregateRating=AggregateRating(ratingValue=5, ratingCount=18),
            video=VideoObject(
                name='How to make a Party Coffee Cak',
                description='This is how you make a Party Coffee Cake.',
                thumbnailUrl=[
                    "https://example.com/photos/1x1/photo.jpg",
                    "https://example.com/photos/4x3/photo.jpg",
                    "https://example.com/photos/16x9/photo.jpg"
                ],
                contentUrl='http://www.example.com/video123.mp4',
                embedUrl='http://www.example.com/videoplayer?video=123',
                uploadDate=Date(2018, 2, 5),
                duration=Duration(0, 1 * 60 + 33),
                expires=Date(2019, 2, 5)),
            nutrition=NutritionInformation(calories=270)),
                   default=utils.default))
    pass
