import atexit
import json
import os

from switchbot import SwitchBot


def prepare_switchbot(email, password, credential_filename):
    if not os.path.exists(credential_filename):
        switchbot = SwitchBot(email)
        switchbot.authenticate(password)
    else:
        with open(credential_filename, "r", encoding="utf-8") as input_file:
            switchbot = SwitchBot(json.load(input_file))

    @atexit.register
    def store_credential():
        if switchbot.authenticated:
            with open(credential_filename, "w", encoding="utf-8") as output_file:
                json.dump(switchbot.cognito_tokens, output_file)
        else:
            if os.path.exists(credential_filename):
                os.unlink(credential_filename)

    return switchbot


switchbot = prepare_switchbot(
    email="your@account.com",
    password="yourpassword",
    credential_filename="credential.json",
)
