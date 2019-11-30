from http import HTTPStatus
from logging import getLogger
from timeit import timeit

import requests

from .requests_cache import requests_cache

logger = getLogger(__name__)


def test_requests_cache() -> None:
    def perform_request() -> None:
        with requests.Session() as session:
            response = session.get("https://example.org")
            assert HTTPStatus(response.status_code) == HTTPStatus.OK

    @requests_cache(regenerate=True)
    def perform_request_no_cache() -> None:
        return perform_request()

    @requests_cache()
    def perform_request_with_cache() -> None:
        return perform_request()

    time_no_cache = timeit(perform_request_no_cache, number=1)
    time_with_cache = timeit(perform_request_with_cache, number=1)

    logger.debug(
        "Request took {:.4f}s without cache and {:.4f}s with cache.".format(
            time_no_cache, time_with_cache
        )
    )

    # Expect at least a 10x speedup through caching requests.
    assert time_no_cache > 10 * time_with_cache