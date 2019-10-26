"""
https://developers.google.com/search/docs/data-types/video
"""
from typing import Iterable, Union

from structured_data.base import URL, Date, Property, Text, Thing
from structured_data.lower.interaction_counter import InteractionCounter
from structured_data.lower.quantity import Duration


class VideoObject(Thing):
    """
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
    pass
