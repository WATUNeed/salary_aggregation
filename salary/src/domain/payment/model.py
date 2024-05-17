import datetime

from beanie import Document


class Payment(Document):
    value: int
    dt: datetime.datetime
