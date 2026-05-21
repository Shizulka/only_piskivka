class UserRegisteredAnalyticsHandler:
    def __init__(self, analytics_repo):
        self.analytics_repo = analytics_repo

    async def handle(self, event):
        print("ANALYTICS USER EVENT RECEIVED:", event)

        self.analytics_repo.increment_users_count()