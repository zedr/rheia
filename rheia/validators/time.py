from rheia.parsers.time import time_sequence_rxp


def is_valid_duration(text):
    return bool(time_sequence_rxp.match(text))
