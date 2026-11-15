# coding: utf-8
"""
Helpers for building request parameters.
"""


def bool_params(params):
    """
    Send booleans as "true" / "false", the form the Backlog API documents
    (instead of Python's "True" / "False").
    """
    return {k: ("true" if v else "false") if isinstance(v, bool) else v for k, v in params.items()}
