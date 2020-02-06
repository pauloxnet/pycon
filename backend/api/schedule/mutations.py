import typing
from datetime import date, datetime, time, timedelta

import strawberry
from api.conferences.types import Day
from conferences.models import Conference
from schedule.models import Day as DayModel
from schedule.models import Slot
from strawberry.types.datetime import Date


@strawberry.type
class AddScheduleSlotError:
    message: str


def add_minutes_to_time(time: time, minutes: int) -> time:
    return (datetime.combine(date(1, 1, 1), time) + timedelta(minutes=minutes)).time()


# TODO: permission
@strawberry.type
class ScheduleMutations:
    @strawberry.mutation
    def add_schedule_slot(
        self, info, conference: strawberry.ID, duration: int, day: Date
    ) -> typing.Union[AddScheduleSlotError, Day]:
        conference = Conference.objects.get(code=conference)
        day, _ = DayModel.objects.get_or_create(day=day, conference=conference)

        # TODO: ordering
        last_slot = day.slots.last()

        # TODO: is it ok to hardcode this?
        hour = time(8, 45)
        offset = 0

        if last_slot:
            hour = add_minutes_to_time(last_slot.hour, last_slot.duration)
            offset = last_slot.offset + last_slot.size

        Slot.objects.create(day=day, hour=hour, duration=duration, offset=offset)

        return Day(day=day.day, slots=day.slots.all())
