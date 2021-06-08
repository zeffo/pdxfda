from .submission import Submission, Document
from .product import Product
from typing import List, Optional
from utils import check_for_keywords


class Drug:
    """Represents an OpenFDA Drug"""

    def __init__(self, data) -> None:
        self.data: dict = data
        self.id: str = data["application_number"]
        self.sponsor: str = data["sponsor_name"]

    @property
    def latest_submission(self) -> Optional[Submission]:
        subs = self.submissions()
        return subs[0] or None

    def submissions(self) -> List[Submission]:
        """Returns a list of Submissions, sorted from newest to oldest"""
        return sorted(
            [Submission(sub) for sub in self.data["submissions"]],
            key=lambda s: int(s.date),
            reverse=True,
        )

    def products(self) -> List[Product]:
        return (
            [Product(d) for d in self.data["products"]]
            if "products" in self.data
            else None
        )

    @property
    def label(self) -> Optional[Document]:
        """Returns the label of the latest submission"""
        for submission in self.submissions():
            if label := submission.label():
                return label

    @property
    def name(self) -> str:
        """Find the name of the drug from OpenFDA data and Product data"""
        if "openfda" in self.data:
            drug = self.data["openfda"].get("brand_name", ("Unnamed Drug"))[0]
        elif products := self.products():
            drug = products[0].name
        else:
            drug = f"Unnamed Drug"
        return drug


    def _dict(self) -> dict:
        data = {
            "id": self.id,
            "name": self.name,
            "label": str(self.label),
        }
        return data
