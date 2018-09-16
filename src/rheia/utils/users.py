def fullname_or_username(user):
    """The full-name or username of this user.

    :param user: the user instance
    :type user: :class:`django.contrib.auth.models.User`
    :returns: the name
    :rtype: str
    """
    user.get_full_name()
    if user.first_name:
        if user.last_name:
            return user.first_name + " " + user.last_name
        else:
            return user.first_name
    else:
        return user.username
