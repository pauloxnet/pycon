import pytest
import respx
from django.conf import settings

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def mock_users(mocker):

    with respx.mock as mock:
        mock.post(f"{settings.USERS_SERVICE_URL}/internal-api").respond(
            json={
                "data": {
                    "usersByIds": [
                        {
                            "id": 10,
                            "fullname": "Marco Acierno",
                            "name": "Marco",
                            "username": "marco",
                        }
                    ]
                }
            }
        )


def test_conference_ranking_does_not_exists(
    conference_factory, graphql_client, mock_users
):
    conference = conference_factory(
        topics=[
            "Sushi",
        ]
    )

    query = """
        query($code: String!, $topic: ID!) {
            conference(code: $code) {
                ranking(topic: $topic) {
                    isPublic
                    rankedSubmissions {
                        rank
                        score
                    }
                }
            }
        }
    """

    resp = graphql_client.query(
        query,
        variables={"code": conference.code, "topic": conference.topics.first().id},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["ranking"] is None


def test_conference_ranking_is_not_public(
    conference_factory, rank_request_factory, graphql_client, mock_users
):
    conference = conference_factory(
        topics=[
            "Sushi",
        ]
    )
    rank_request_factory(conference=conference, is_public=False)
    query = """
        query($code: String!, $topic: ID!) {
            conference(code: $code) {
                ranking(topic: $topic) {
                    isPublic
                }
            }
        }
    """

    resp = graphql_client.query(
        query,
        variables={"code": conference.code, "topic": conference.topics.first().id},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["ranking"] is None


def test_conference_ranking_is_public_anyone_can_see(
    conference,
    rank_request_factory,
    rank_submission_factory,
    graphql_client,
    mock_users,
):
    rank_request = rank_request_factory(conference=conference, is_public=True)
    rank_submission = rank_submission_factory(rank_request=rank_request)
    query = """
        query($code: String!, $topic: ID!) {
            conference(code: $code) {
                ranking(topic: $topic) {
                    isPublic
                    rankedSubmissions {
                        rank
                        score
                    }
                }
            }
        }
    """

    resp = graphql_client.query(
        query,
        variables={
            "code": conference.code,
            "topic": str(rank_submission.submission.topic.id),
        },
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["ranking"]["isPublic"] is True

    rank_submission_data = resp["data"]["conference"]["ranking"]["rankedSubmissions"][0]

    assert rank_submission_data["rank"] == rank_submission.rank
    assert float(rank_submission_data["score"]) == float(rank_submission.score)


def test_conference_ranking_is_not_public_admin_can_see(
    conference,
    rank_request_factory,
    rank_submission_factory,
    graphql_client,
    admin_user,
    mock_users,
):
    graphql_client.force_login(admin_user)
    rank_request = rank_request_factory(conference=conference, is_public=False)
    rank_submission = rank_submission_factory(rank_request=rank_request)
    query = """
        query($code: String!, $topic: ID!) {
            conference(code: $code) {
                ranking(topic: $topic) {
                    isPublic
                    rankedSubmissions {
                        rank
                        score
                    }
                }
            }
        }
    """

    resp = graphql_client.query(
        query,
        variables={
            "code": conference.code,
            "topic": rank_submission.submission.topic.id,
        },
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["ranking"]["isPublic"] is False

    rank_submission_data = resp["data"]["conference"]["ranking"]["rankedSubmissions"][0]

    assert rank_submission_data["rank"] == rank_submission.rank
    assert float(rank_submission_data["score"]) == float(rank_submission.score)


def test_conference_ranking_is_not_public_users_cannot_see(
    conference,
    rank_request_factory,
    rank_submission_factory,
    graphql_client,
    user,
    mock_users,
):
    graphql_client.force_login(user)
    rank_request = rank_request_factory(conference=conference, is_public=False)
    rank_submission = rank_submission_factory(
        rank_request=rank_request, submission__speaker_id=10
    )

    query = """
        query($code: String!, $topic: ID!) {
            conference(code: $code) {
                ranking(topic: $topic) {
                    isPublic
                    rankedSubmissions {
                        rank
                        score
                    }
                }
            }
        }
    """

    resp = graphql_client.query(
        query,
        variables={
            "code": conference.code,
            "topic": rank_submission.submission.topic.id,
        },
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["ranking"] is None
