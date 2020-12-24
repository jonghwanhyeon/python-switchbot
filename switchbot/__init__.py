"""Main classes."""
from functools import cached_property, partial

from pycognito import Cognito
from requests import Session
from requests.auth import AuthBase

from .utils import sanitize_id, url_for


SwitchBotCognito = partial(
    Cognito, user_pool_id="us-east-1_x1fixo5LC", client_id="19n6vlutv8316utiqq66urakk3"
)


class SwitchBotAuth(AuthBase):
    """Class to handle Cognito authentication."""

    def __init__(self, switchbot):
        """Create authentication object."""
        self.switchbot = switchbot

    def __call__(self, request):
        """Add authenticalion header."""
        if "l9ren7efdj" in request.url:
            expired = self.switchbot.cognito.check_token()
            token = self.switchbot.cognito.access_token
        elif "vxhewp40e8" in request.url:
            token = self.switchbot.user_token
        else:
            raise ValueError(f"Invalid url: {request.url}")

        request.headers["Authorization"] = token

        return request


class Device:
    """Eevice class."""

    def __init__(self, session, id):
        """Create device object."""
        self.session = session
        self.id = sanitize_id(id)

        self._refresh()

    def _refresh(self):
        response = self.session.post(
            url_for("refresh_device"), json={"items": [self.id]}
        )

        self._type = response.data["deviceType"]
        self._state = response.data["status"]["power"]

    def _up_to_date(func):
        def inner(self, *args, **kwargs):
            self._refresh()
            return func(self, *args, **kwargs)

        return inner

    @property
    @_up_to_date
    def state(self):
        """Current state."""
        return self._state

    @property
    @_up_to_date
    def type(self):
        """Device type."""
        return self._type

    def turn(self, state):
        """Set device state."""
        assert state.lower() in ("off", "on")
        self.session.post(
            url_for("turn_device"),
            json={
                "items": [
                    {
                        "deviceID": self.id,
                        "deviceType": self._type,
                        "cmdType": "command",
                        "parameter": "default",
                        "deviceCmd": f"turn{state.title()}",
                        "version": 1,
                        "platform": "widget",
                    }
                ]
            },
        )

    def toggle(self):
        """Toggle device state."""
        self.turn("on" if self.state == "off" else "off")


class SwitchBot:
    """Main SwitchBot class."""

    def __init__(self, email_or_tokens=None, **kwargs):
        """Create SwitchBot object."""
        email, tokens = kwargs.get("email"), kwargs.get("tokens")
        if isinstance(email_or_tokens, str):
            email = email_or_tokens
        elif isinstance(email_or_tokens, dict):
            tokens = email_or_tokens

        email_passed, tokens_passed = email is not None, tokens is not None
        if email_passed and tokens_passed:
            raise ValueError("Either email or tokens should be passed")

        if email_passed:
            self.cognito = SwitchBotCognito(username=email)
        elif tokens_passed:
            self.cognito = SwitchBotCognito(**tokens)
        else:
            raise ValueError("Neither email nor tokens are passed")

        self.session = self._prepare_session()

    def authenticate(self, password):
        """Authenticate with SwitchBot."""
        self.cognito.authenticate(password)

    def device(self, id):
        """Return individual device by ID."""
        return Device(self.session, id)

    @cached_property
    def user_token(self):
        """Return user token."""
        response = self.session.get(url_for("query_user"))

        return response.data["openApiToken"]["token"]

    @property
    def authenticated(self):
        """Currently authenticated."""
        return bool(self.cognito.access_token)

    @property
    def cognito_tokens(self):
        """Return Cognito tokens."""
        return {
            "id_token": self.cognito.id_token,
            "refresh_token": self.cognito.refresh_token,
            "access_token": self.cognito.access_token,
        }

    def _prepare_session(self):
        def handle_response(response, *args, **kwargs):
            data = {key.lower(): value for key, value in response.json().items()}

            assert data["statuscode"] == 100

            data = data["body"]
            data = data["items"] if "items" in data else data

            response.data = (
                data[0] if isinstance(data, list) and (len(data) == 1) else data
            )

            return response

        session = Session()
        session.auth = SwitchBotAuth(self)
        session.headers.update({"Content-Type": "application/json"})
        session.hooks["response"].append(handle_response)
        return session
