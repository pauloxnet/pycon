import strawberry

from api.users.types import User

from .blog.schema import BlogQuery
from .conferences.schema import ConferenceQuery
from .grants.mutations import GrantsMutations
from .job_board.schema import JobBoardQuery
from .newsletters.schema import NewsletterMutations
from .orders.mutations import OrdersMutations
from .orders.query import OrdersQuery
from .pages.schema import PagesQuery
from .schedule.mutations import ScheduleMutations
from .submissions.mutations import SubmissionsMutations
from .submissions.schema import SubmissionsQuery
from .users.schema import CountryQuery
from .voting.mutations import VotesMutations


@strawberry.type
class Query(
    ConferenceQuery,
    BlogQuery,
    SubmissionsQuery,
    PagesQuery,
    CountryQuery,
    OrdersQuery,
    JobBoardQuery,
):
    pass


@strawberry.type
class Mutation(
    SubmissionsMutations,
    VotesMutations,
    OrdersMutations,
    GrantsMutations,
    NewsletterMutations,
    ScheduleMutations,
):
    pass


schema = strawberry.federation.Schema(query=Query, mutation=Mutation, types=[User])
