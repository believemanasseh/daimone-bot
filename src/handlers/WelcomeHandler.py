class WelcomeHandler:
    @classmethod
    def handle(cls, username):
        return f"""
            Welcome to daimones bot, {username}! Please, how can I be of service?
        """
