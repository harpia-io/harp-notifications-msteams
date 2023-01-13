import pymsteams


class NotificationProcessor(object):
    def __init__(self, teams_webhook):
        self.teams_webhook = teams_webhook
        self.teams_message = self.create_connector()

    def create_connector(self):
        teams_message = pymsteams.connectorcard(self.teams_webhook)

        return teams_message

    def send_notification(self, title: str, text: str, button_url: dict = None, facts: dict = None):
        self.teams_message.title(title)

        if text:
            self.teams_message.text(text)
        else:
            self.teams_message.text("More details about alerts:")

        if button_url:
            for key, value in button_url.items():
                self.teams_message.addLinkButton(key, value)

        if facts:
            message_section = pymsteams.cardsection()
            for key, value in facts.items():
                message_section.addFact(key, value)

            self.teams_message.addSection(message_section)

        self.teams_message.send()
