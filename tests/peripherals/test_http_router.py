import unittest
from requiem_testing.peripherals.http import HTTPMethod
from requiem_testing.peripherals.http import HTTPRequest
from requiem_testing.peripherals.http import HTTPResponse
from requiem_testing.peripherals.http import AsyncHTTPRouter


class TestAsyncHTTPRouterFixture(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self._router = AsyncHTTPRouter()
        async def _do_nothing_request_handler(request: HTTPRequest) -> HTTPResponse:
            return HTTPResponse(200, "OK", {}, b"")
        self._do_nothing_request_handler = _do_nothing_request_handler

class TestAsyncHTTPRouterPostMethodSpecificLogic(TestAsyncHTTPRouterFixture):

    async def test_should_be_able_to_add_request_handler_for_path_and_post_method_specifically(self):
        self._router.add_handler_for_post("/a/b/c", self._do_nothing_request_handler)
        handler_returned_for_post = self._router.get_handler_for_path("/a/b/c", HTTPMethod.POST)
        # since it was added for post, when using another method like GET, they should return None since it isn't a match
        handler_returned_for_get = self._router.get_handler_for_path("/a/b/c", HTTPMethod.GET)
        self.assertIs(self._do_nothing_request_handler, handler_returned_for_post)
        self.assertIsNone(handler_returned_for_get)

    async def test_should_get_value_error_when_request_handler_has_already_been_added_for_method_any(self):
        self._router.add_handler_for_any("9/8/7", self._do_nothing_request_handler)
        with self.assertRaises(ValueError):
            self._router.add_handler_for_post("9/8/7", self._do_nothing_request_handler)

class TestAsyncHTTPRouterGetMethodSpecificLogic(TestAsyncHTTPRouterFixture):

    async def test_should_be_able_to_add_request_handler_for_path_and_get_method_specifically(self):
        self._router.add_handler_for_get("/1/2/3", self._do_nothing_request_handler)
        handler_returned_for_get = self._router.get_handler_for_path("/1/2/3", HTTPMethod.GET)
        handler_returned_for_post = self._router.get_handler_for_path("/1/2/3", HTTPMethod.POST)
        self.assertIs(self._do_nothing_request_handler, handler_returned_for_get)
        self.assertIsNone(handler_returned_for_post)


    async def test_should_get_value_error_when_request_handler_has_already_been_added_for_method_any(self):
        # When a request handler has been added for the path and ANY request method, it should not
        # be possible to add a request handler for a specific method like GET for it.
        self._router.add_handler_for_any("/path/to/thing1", self._do_nothing_request_handler)
        with self.assertRaises(ValueError):
            self._router.add_handler_for_get("/path/to/thing1", self._do_nothing_request_handler)
