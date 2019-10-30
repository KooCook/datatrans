"""
https://developers.google.com/search/docs/data-types/video
"""
from typing import Iterable, Union

from structured_data.base import URL, Date, Property, Text, Thing
from structured_data.lower.interaction_counter import InteractionCounter
from structured_data.lower.quantity import Duration


class VideoObject(Thing):
    """Schema.org's VideoObject, as specified by Google

    Required properties:
        description: Text
            The description of the video. HTML tags are ignored.
        name: Text
            The title of the video
        thumbnailUrl: Repeated ImageObject or UR
            A URL pointing to the video thumbnail image file.
              - Image URLs must be crawlable and indexable.
              - Images must represent the marked up content.
              - Images must be in .jpg, .png, or. gif format.
              - Images must 60px x 30px, at minimum.
        uploadDate: Date
            The date the video was first published, in ISO 8601 format

    Recommended properties:
        contentUrl: URL
            A URL pointing to the actual video media file.
            We recommend that you provide a URL to your video.
            You can provide a URL by using one or both of the
            following properties: ``contentUrl`` and ``embedUrl``.
        duration: Duration
            The duration of the video in ISO 8601 format.
            For example, T00H30M5S represents a duration of
            "thirty minutes and five seconds".
        embedUrl: URL
            A URL pointing to a player for the specific video.
            Usually this is the information in the src element
            of an <embed> tag.
        expires: Date
            If applicable, the date after which the video will no
            longer be available, in ISO 8601 format.
            Don't supply this information if your video does not expire.
        interactionStatistic: InteractionCounter
            The number of times the video has been watched.
            For example:
            ```
            "interactionStatistic":
              {
                "@type": "InteractionCounter",
                "interactionType": { "@type": "http://schema.org/WatchAction" },
                "userInteractionCount": 12345
              }
            ```
    """
    PROPERTIES = (
        # required
        'name',
        'description',
        'thumbnailUrl',
        'uploadDate',
        # recommended
        'contentUrl',
        'duration',
        'embedUrl',
        'expires',
        'interactionStatistic',
        # optional,
        'author'
    )

    def __init__(self, *, name: Text, description: Text,
                 thumbnailUrl: Iterable[Union[URL, str]], uploadDate: Date,
                 contentUrl: Union[URL, str], duration: Duration = None,
                 embedUrl: Union[URL, str] = None, expires: Date = None,
                 interactionStatistic: InteractionCounter = None, **kwargs):
        self._name: Text = name
        self._description: Text = description
        self._thumbnail_url = Property(*thumbnailUrl, class_=URL)
        self._upload_date = uploadDate
        if not URL.is_url(contentUrl) and contentUrl is not None:
            raise ValueError('contentUrl is invalid URL')
        self._content_url = contentUrl
        self._duration = duration
        if not URL.is_url(embedUrl) and embedUrl is not None:
            raise ValueError('embedUrl is invalid URL')
        self._embed_url = embedUrl
        self._expires = expires
        self._interaction_statistic = interactionStatistic
        self._author = kwargs.pop('author', None)


if __name__ == '__main__':
    import json
    from structured_data import utils
    from structured_data.lower.action import Action
    from structured_data.base import DateTime

    print(json.dumps(VideoObject(
        name='Introducing the self-driving bicycle in the Netherlands',
        description='This spring, Google is introducing the self-driving bicycle in Amsterdam, the world’s premier cycling city. The Dutch cycle more than any other nation in the world, almost 900 kilometres per year per person, amounting to over 15 billion kilometres annually. The self-driving bicycle enables safe navigation through the city for Amsterdam residents, and furthers Google’s ambition to improve urban mobility with technology. Google Netherlands takes enormous pride in the fact that a Dutch team worked on this innovation that will have great impact in their home country.',
        thumbnailUrl=[("https://example.com/photos/1x1/photo.jpg"),
                      ("https://example.com/photos/4x3/photo.jpg"),
                      ("https://example.com/photos/16x9/photo.jpg")],
        uploadDate=DateTime(2016, 3, 31),
        contentUrl='https://www.example.com/video/self-driving-bicycle/file.mp4',
        embedUrl='https://www.example.com/embed/123',
        interactionStatistic=InteractionCounter(
            userInteractionCount=567018,
            interactionType=Action.WatchAction
        )
    ), default=utils.default))
    pass
