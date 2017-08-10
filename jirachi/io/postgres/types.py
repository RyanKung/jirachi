from typing import NamedTuple
from typing import NewType
import datetime

__all__ = ['json', 'varchar',
           'boolean', 'Table']

json = NewType('json', dict)
varchar = NewType('varchar', str)
boolean = NewType('boolean', bool)
text = NewType('text', str)
integer = NewType('integer', int)
timestamp = NewType('timestamp', datetime.datetime)
array = NewType('array', list)
Table = NamedTuple
