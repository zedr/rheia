def serialise(collection, **serialiser_kwargs):
    """Serialise a collection of model instance to a sequence of dicts.

    :param sequence: a sequence of model instances, that define a serialise()
        method
    :param: an optional set of keyword arguments to pass to the serialiser.
    :return: generator
    """
    for item in collection:
        yield item.serialise(**serialiser_kwargs)
