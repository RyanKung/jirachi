from typing import Any
from collections import defaultdict

__all__ = ['configdict']


def configdict(cases: dict, other: Any) -> defaultdict:
    assert other in cases.keys(), 'cases should include default cases'
    return defaultdict(lambda: other)(cases)
