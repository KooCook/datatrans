"""
https://developers.google.com/search/docs/data-types/logo
"""
from .base import Thing


class Organization(Thing):
    """
    Required properties:

        logo: URL
        URL of a logo that is representative of the organization.

        Additional image guidelines:
          - The image must be 112x112px, at minimum.
          - The image URL must be crawlable and indexable.
          - The image must be in .jpg, .png, or. gif format.

        url: URL

        The URL of the website associated with the logo.
    """
