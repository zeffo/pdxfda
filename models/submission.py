from typing import Optional
from requests import get
from aiohttp import request
from errors import APIError


class Document:
    """Represents a review document"""

    __slots__ = ("data", "date", "type", "url", "id")

    def __init__(self, data) -> None:
        self.data = data
        for key in self.__slots__[1:]:
            setattr(self, key, data[key])

    def read(self):
        resp = get(self.url)
        if resp.status_code == 200:
            return resp.content
        else:
            raise APIError(resp.status_code)

    async def async_read(self):
        async with request("get", self.url) as resp:
            if resp.status == 200:
                return await resp.read()
            else:
                raise APIError(resp.status)

    def __repr__(self) -> str:
        return self.url


class Submission:
    """Represents a drug submission"""

    __slots__ = ("type", "number", "status", "date", "review_priority", "data")

    def __init__(self, data) -> None:
        self.data = data
        aliases = zip(
            self.__slots__,
            (
                "submission_type",
                "submission_number",
                "submission_status",
                "submission_status_date",
                "review_priority",
            ),
        )
        for attr, value in aliases:
            setattr(self, attr, data.get(value))

    def label(self) -> Optional[Document]:
        """Return a Document of type Label, or None if no such document exists."""
        key = "application_docs"
        if key in self.data:
            for doc in self.data[key]:
                if doc["type"] == "Label":
                    return Document(doc)
        return None

    def __repr__(self) -> str:
        return f"{self.type} {self.number}: Submitted on: {self.date}, Status: {self.status}, Review Priority: {self.review_priority}\n"
