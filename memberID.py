from enum import Enum
from collections import namedtuple

MemberID = namedtuple('memberID', [
    'character',
    'description'
])


class Character(Enum):
    NAMESPACE = 'N'
    TYPE = 'T'
    METHOD = 'M'
    FIELD = 'F'
