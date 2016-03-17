import re

time_sequence_rxp = re.compile(
    r"^ *((?P<hours>\d+)h)?"
    r" *((?P<minutes>\d+)m)?"
    r" *((?P<seconds>\d+)s)? *$"
)


def parse_time(text):
    """Parse some text and try to infer how many seconds are given.

    The syntax is:
        h for hours
        m for minutes
        s for seconds

    Example: "1h 30m 15s" for "1 hour, 40 minutes, and 15 seconds"

    :returns: the number of seconds, or nothing if the text is not correct.
    :rtype: int|None
    """
    match = time_sequence_rxp.match(text)
    if match:
        ns = match.groupdict()
        hours = ns["hours"] or 0
        minutes = ns["minutes"] or 0
        seconds = ns["seconds"] or 0
        return (int(hours) * 60 * 60) + (int(minutes) * 60) + int(seconds)
    else:
        raise ValueError("Cannot parse `{0}` as time.".format(text))
