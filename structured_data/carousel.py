"""
https://developers.google.com/search/docs/data-types/carousel

In addition to the standard structured data guidelines, the following
guidelines apply to all list markup:

  - All items in the list must be of the same type, for example:
    Article or Recipe.
  - The text visible to the user must be similar to the information
    contained in the structured data on the page.
  - Items shown in list format will be shown in the order specified
    by the position property.
  - List format is currently supported for the following content
    types: Recipe, Course, Article, Restaurant, Movie.

There are two ways to implement a list format for your structured data:

1.  Summary page + multiple full details pages
    Summary page
        Defines an ``ItemList``, where each ``ListItem`` has only three
        properties: @type (set to "ListItem"), position (the position
        in the list), and url (the URL of a page with full details
        about that item).
    Details page
        Defines a structured data element appropriate for that list type.

2.  A single, all-in-one-page list
    Defines an ``ItemList``, where each element is a ``ListItem`` with
    the item property populated with the structured data for that
    schema.org element type (for example, ``Movie`` or ``Course``).
    The page should contain user-visible text and an anchor to match
    each ``ListItem`` element.
"""
from typing import List, Optional
import enum

from structured_data.base.data_type import Integer, URL
from structured_data.base.thing import Thing


class ItemLIstOrderType(enum.Enum):
    ItemListOrderAscending = 'http://schema.org/ItemListOrderAscending'
    ItemListOrderDescending = 'https://schema.org/ItemListOrderDescending'
    ItemListUnordered = 'https://schema.org/ItemListUnordered'


class ItemList(Thing):
    """
    `ItemList` is the container item that holds all elements in the
    list. If used on a summary page, all URLs in the list must point to
    different pages on the same domain. If used on an all-in-one-page
    list, all URLs must point to the page hosting the list structured
    data.

    The full definition of `ItemList` is available at
    https://schema.org/ItemList.

    Required properties:

        itemListElement: ListItem
            List of items. All items must be of the same type.
            See ``ListItem`` for details.
    """

    def __init__(self, *args, **kwargs):
        self._item_list_element: List[ListItem] = []
        for item in args:
            if not isinstance(item, ListItem):
                item = ListItem(item, position=self.numberOfItems + 1)
            self._item_list_element.append(item)

        self._item_list_order: Optional[ItemLIstOrderType] = kwargs.pop(
            'ItemLIstOrder', ItemLIstOrderType.ItemListOrderDescending)

        if not self.has_one_type_of_item():
            raise ValueError('More than 1 type of item')

    def has_one_type_of_item(self) -> bool:
        return len(set(listitem.item.__class__.__name__
                       for listitem in self._item_list_element)) == 1

    def get_json_ld(self, top_level: bool = False) -> str:
        if top_level:
            return '{{{}}}'.format(','.join((
                Thing.get_context(),
                self.get_type_specification(),
                self.get_str_item_list_element(),
            )))
        return '{{{}}}'.format(','.join((
            self.get_type_specification(),
            self.get_str_item_list_element(),
        )))

    def __str__(self):
        return self.get_json_ld()

    def get_str_item_list_element(self) -> str:
        return '"itemListElement":{}'.format(self._item_list_element)

    def get_str_item_list_order(self) -> str:
        if self._item_list_order is not None:
            return '"itemListOrder":{}'.format(self._item_list_order)
        return ''

    def get_str_number_of_items(self) -> str:
        return '"numberOfItems":{}'.format(self.numberOfItems)

    def sort(self) -> None:
        if self.itemListOrder != ItemLIstOrderType.ItemListUnordered:
            def get_position(listitem: ListItem):
                return listitem.position
            self._item_list_element.sort(key=get_position, reverse={
                ItemLIstOrderType.ItemListOrderAscending: True,
                ItemLIstOrderType.ItemListOrderDescending: False,
            }[self.itemListOrder])
        else:
            raise ValueError('cannot sort ItemListUnordered')

    def append(self, item: 'ListItem') -> None:
        if not isinstance(item, ListItem):
            item = ListItem(item, position=self.numberOfItems + 1)
        self._item_list_element.append(item)


    @property
    def itemListElement(self) -> List['ListItem']:
        return self._get_item_list_element()

    def _get_item_list_element(self) -> List['ListItem']:
        return self._item_list_element

    @property
    def itemListOrder(self) -> ItemLIstOrderType:
        return self._get_item_list_order()

    @itemListOrder.setter
    def itemListOrder(self, item_list_order: ItemLIstOrderType):
        self._set_item_list_order(item_list_order)

    def _get_item_list_order(self) -> ItemLIstOrderType:
        return self._item_list_order

    def _set_item_list_order(self, new_item_list_order: ItemLIstOrderType):
        if isinstance(new_item_list_order, ItemLIstOrderType):
            self._item_list_order = new_item_list_order
            return
        raise TypeError('itemListOrder should be \'ItemLIstOrderType\'')

    @property
    def numberOfItems(self) -> Integer:
        return self._get_number_of_items()

    def _get_number_of_items(self) -> Integer:
        return len(self._item_list_element)


class ListItem(Thing):
    """
    `ListItem` contains details about an individual item in the list.
      - If this is a **summary page**, the `ListItem` should include
        only the `type`, `position`, and `url` properties.
      - If this is an **all-in-one-page** list, the `ListItem` should
        include all the additional schema.org properties for the data
        type that it describes (for example, `Recipe` or `Course`
        objects).

    Required properties (summary page):
        position: Integer
            The item's position in the carousel. This is a 1-based number.
        url: URL
            Used for summary page lists only. This property is required
            for summary pages. **Do not include** for all-in-one-page
            lists. The canonical URL of the item detail page. All URLs
            in the list must be unique, but live on the same domain
            (the same domain or sub/super domain as the current page).

    Required properties (all-in-one-page):
        item: Thing
            Used for all-in-one-page lists only. This property is
            required for all-in-one-page lists. **Do not include** for
            summary pages. Populate this object with the following
            values, plus all the members of the specific structured
            data type being described
        item.name: Text
            String name of the item, displayed in the rendered gallery.
            HTML formatting is ignored. This property is required for
            all-in-one-page lists. **Do not include** for summary pages.
        item.url: URL
            Fully-qualified URL + page anchor to this item on the page.
            This property is required for all-in-one-page lists.
            **Do not include** for summary pages. The URL must be the
            current page, and you must include an HTML anchor (<a> tag
            or name or id value) in your page near the user-visible
            text. Example: https://example.org/recipes/pies#apple_pie.
        position: Integer
            The item's position in the carousel. This is a 1-based number.
    """
    def __init__(self, arg, *, position):
        self._position = position
        if URL.is_url(arg):
            self._url: Optional[URL] = arg
            self._item: Optional[Thing] = None
        else:
            self._item: Optional[Thing] = arg
            self._url: Optional[URL] = None

    def get_json_ld(self, top_level: bool = False) -> str:
        assert not top_level, '\'ListItem cannot be top level\''
        if self._url is not None:
            assert self._item is None
            return '{{{}}}'.format(','.join((
                self.get_type_specification(),
                self.get_str_position(),
                self.get_str_url(),
            )))
        return '{{{}}}'.format(','.join((
            self.get_type_specification(),
            self.get_str_position(),
            self.get_str_item(),
        )))

    def __str__(self):
        return self.get_json_ld()

    def __repr__(self):
        return self.get_json_ld()

    def get_str_position(self) -> str:
        return '"position":{}'.format(self.position)

    def get_str_url(self) -> str:
        if self._url is not None:
            return '"url":"{}"'.format(self.url)
        raise AttributeError('This ListItem has no url')

    def get_str_item(self) -> str:
        if self._item is not None:
            return '"item":{}'.format(self.item)
        raise AttributeError('This ListItem has no item')

    @property
    def item(self):
        return self._get_item()

    def _get_item(self):
        return self._item

    @property
    def position(self):
        return self._get_position()

    def _get_position(self):
        return self._position

    @property
    def url(self):
        return self._get_url()

    # @url.setter
    # def url(self, new_url: URL):
    #     self._set_url(new_url)

    def _get_url(self):
        return self._url

    # def _set_url(self, new_url: URL):
    #     if URL.is_url(new_url):
    #         self._url = new_url


if __name__ == '__main__':
    pass
