"""
Middleware used to lowercase the email of the user.
"""

import json


class EmailUsernameLowercaseMiddleware:
    """
    Middleware used to lowercase the username of the user.

    Motivation:
    The username is case-sensitive, but the email is not.
    We use the email as a username, so we need to lowercase it.
    """

    @staticmethod
    def username_email_in_request(request):
        """
        Check if the username or email is in the request.
        :param request: Request an object
        :return: True if the username or email is in the request, False otherwise
        """
        return b"csrfmiddlewaretoken" not in request.body and (
            b"username" in request.body or b"email" in request.body
        )

    def __init__(self, get_response):
        """
        Constructor of the middleware.
        :param get_response: Get response method
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Call method of the middleware.
        :param request: Request an object
        :return: Response object with lowercase data
        """
        # Username or email in request
        if EmailUsernameLowercaseMiddleware.username_email_in_request(request):
            # Decode the request and convert it to a json
            decoded_request = request.body.decode("utf8").replace("'", '"')
            json_request = json.loads(decoded_request)

            # Lowercase the username and email
            if b"username" in request.body:
                json_request["username"] = json_request["username"].lower()

            if b"email" in request.body:
                json_request["email"] = json_request["email"].lower()

            # Encode the request and convert it to a jso)
            encoded_request = json.dumps(json_request).encode("utf8")
            request._body = encoded_request

            response = self.get_response(request)
            return response

        # Normal request and response
        response = self.get_response(request)
        return response
