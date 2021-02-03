from ward import test

from users.api.tests.graphql_client import graphql_client
from users.tests.factories import user_factory
from users.tests.session import db


@test("cannot get me if unlogged")
async def _(graphql_client=graphql_client, db=db, user_factory=user_factory):
    await user_factory(id=1, email="test@me.it")

    query = """
    {
        me {
            id
            email
        }
    }
    """
    response = await graphql_client.query(query)

    assert response.errors[0]["message"] == "Not authenticated"


@test("fetch my data when logged")
async def _(graphql_client=graphql_client, db=db, user_factory=user_factory):
    user = await user_factory(id=1, email="test@me.it")
    graphql_client.force_login(user)

    query = """
    {
        me {
            id
            email
        }
    }
    """
    response = await graphql_client.query(query)

    assert not response.errors
    assert response.data["me"] == {"id": 1, "email": "test@me.it"}