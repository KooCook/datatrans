from structured_data.base import Thing, Number


class AggregateRating(Thing):
    """
    Required properties:
        itemReviewed: Thing
            The item that is being rated. However, if the aggregate
            rating is embedded into another schema.org type using the
            aggregateRating property, you can omit the ``itemReviewed``
            property. The valid types for the reviewed item are:
                Book
                Course
                CreativeWorkSeason
                CreativeWorkSeries
                Episode
                Event
                Game
                HowTo
                LocalBusiness
                MediaObject
                Movie
                MusicPlaylist
                MusicRecording
                Organization
                Product
                Recipe
        itemReviewed.name: Text
            The name of the item that is being reviewed. If the review
            is embedded into another schema.org type using the review
            property, you still need to provide the name of the thing
            that is being reviewed.
        ratingCount: Number
            The total number of ratings for the item on your site.
            At least one of ``ratingCount`` or ``reviewCount`` is
            required.
        reviewCount: Number
            Specifies the number of people who provided a review with
            or without an accompanying rating. At least one of
            ``ratingCount`` or ``reviewCount`` is required.
        ratingValue: Number or Text
            A numerical quality rating for the item, either a number,
            fraction, or percentage. (for example, "4", "60%", or
            "6 / 10"). If the scale is not implicit (for example, "4")
            a 1 to 5 scale is assumed. If another scale is intended,
            use ``bestRating`` and ``worstRating``.

    Recommended properties:
        bestRating: Number
            The highest value allowed in this rating system. The
            ``bestRating`` property is only required if the rating
            system is not a 5-point scale. If ``bestRating`` is
            omitted, 5 is assumed.
        worstRating: Number
            The lowest value allowed in this rating system. The
            ``worstRating`` property is only required if the rating
            system is not a 5-point scale. If ``worstRating`` is
            omitted, 1 is assumed.

    http://schema.org/AggregateRating.
    """
    PROPERTIES = (
        # required
        'ratingValue'
        # one of the following
        'ratingCount'
        'reviewCount'
        # recommended
        'bestRating'
        'worstRating'
    )

    def __init__(self, *, itemReviewed: Thing = None, ratingValue: Number,
                 ratingCount: Number = None, reviewCount = None, **kwargs):
        self._item_reviewed = itemReviewed
        self._rating_value = ratingValue
        if ratingCount is None and reviewCount is None:
            raise ValueError('At least one of \'ratingCount\' or \'reviewCount\''
                             ' is required.')
        self._rating_count = ratingCount
        self._review_count = reviewCount
        self._best_rating = kwargs.pop('bestRating', None)  # assumed to be 5
        self._worst_rating = kwargs.pop('worstRating', None)  # assumed to be 1


if __name__ == '__main__':
    import json
    from structured_data import utils

    print(json.dumps(AggregateRating(
        ratingValue=4.6,
        ratingCount=564,
        worstRating=0,
    ), default=utils.default))
    pass
