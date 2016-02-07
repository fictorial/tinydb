def delete(field):
    """
    Delete a given field from the element.
    """
    def transform(element):
        del element[field]

    return transform


def increment(field, delta=1):
    """
    Increment a given field in the element
    by the given delta.
    """
    def transform(element):
        element.setdefault(field, 0)
        element[field] += delta

    return transform


def decrement(field, delta=1, raise_if_negative=False):
    """
    Decrement a given field in the element by the
    given delta.

    If `raise_if_negative` and the value at field _would_
    become negative, raise `ValueError`.
    """
    def transform(element):
        value = element.setdefault(field, 0)

        if raise_if_negative and value - delta < 0:
            raise ValueError(field)

        element[field] = value - delta

    return transform


def add_to_set(field, member):
    """
    Add a member to a set at field in the element.
    """
    def transform(element):
        members = set(element.setdefault(field, []))
        members.add(member)
        element[field] = list(members)

    return transform


def remove_from_set(field, member):
    """
    Remove a member from a set at field in the element.
    """
    def transform(element):
        if field in element:
            members = set(element[field])
            members.remove(member)
            element[field] = list(members)

    return transform


def append(field, item):
    """
    Add an item to the end of the list at field
    in the element.
    """
    def transform(element):
        element.setdefault(field, []).append(item)

    return transform


def prepend(field, item):
    """
    Add an item to the front of the list at field
    in the element.
    """
    def transform(element):
        element.setdefault(field, []).insert(0, item)

    return transform


def slice(field, start, end):
    """
    Slice the list at field in the element such that
    the items in range `[start, end)` remain.
    """
    def transform(element):
        if field in element and type(element[field]) == list:
            element[field] = element[field][start:end]

    return transform
