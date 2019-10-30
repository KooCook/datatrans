from structured_data.base import Integer, Thing
from structured_data.lower.action import Action


class InteractionCounter(Thing):
    """Schema.org's InteractionCounter

    A summary of how users have interacted with this CreativeWork. In
    most cases, authors will use a subtype to specify the specific type
    of interaction.

    References:
        https://schema.org/InteractionCounter
    """
    PROPERTIES = (
        # required
        'interactionType',
        'userInteractionCount',
        # optional
        'interactionService',
    )

    def __init__(self, *, interactionType: Action,
                 userInteractionCount: Integer, **kwargs):
        self._interaction_service = kwargs.pop('interactionService', None)
        self._interaction_type = interactionType
        self.user_interaction_count = userInteractionCount


if __name__ == '__main__':
    import json
    from structured_data import utils

    print(json.dumps(InteractionCounter(
        interactionType=Action.WatchAction, userInteractionCount=125
    ), default=utils.default))
    pass
