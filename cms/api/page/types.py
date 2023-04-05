from typing import Self
from page.models import GenericPage as GenericPageModel

import strawberry

from api.page.blocks.slider_cards_section import SliderCardsSection
from api.page.blocks.text_section import TextSection
from api.base.blocks.map import CMSMap
from api.home.blocks.home_intro_section import HomeIntroSection
from api.page.blocks.sponsors_section import SponsorsSection
from api.page.blocks.schedule_preview_section import SchedulePreviewSection
from api.page.blocks.keynoters_section import KeynotersSection
from api.page.blocks.socials_section import SocialsSection
from api.page.blocks.special_guest_section import SpecialGuestSection
from api.page.blocks.information_section import InformationSection


REGISTRY = {
    "text_section": TextSection,
    "map": CMSMap,
    "slider_cards_section": SliderCardsSection,
    "sponsors_section": SponsorsSection,
    "home_intro_section": HomeIntroSection,
    "keynoters_section": KeynotersSection,
    "schedule_preview_section": SchedulePreviewSection,
    "socials_section": SocialsSection,
    "special_guest_section": SpecialGuestSection,
    "information_section": InformationSection,
}

Block = strawberry.union(
    "Block",
    REGISTRY.values(),
)


@strawberry.type
class GenericPage:
    id: strawberry.ID
    title: str
    body: list[Block]

    @classmethod
    def from_model(cls, obj: GenericPageModel) -> Self:
        return cls(
            id=obj.id,
            title=obj.title,
            body=[
                REGISTRY.get(block.block_type).from_block(block) for block in obj.body
            ],
        )