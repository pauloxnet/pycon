from typing import List

import strawberry

from users.models import get_countries

from .types import Country


@strawberry.type
class CountryQuery:
    @strawberry.field
    def countries(self, info) -> List[Country]:
        resp = get_countries()
        return [Country(code=country["code"], name=country["name"]) for country in resp]

    @strawberry.field
    def country(self, info, code: str = "") -> Country:
        resp = get_countries(code)
        return Country(code=resp["code"], name=resp["name"])
