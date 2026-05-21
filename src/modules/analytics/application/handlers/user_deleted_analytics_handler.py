class UserDeletedAnalyticsHandler:
    def __init__(self, analytics_repo):
        self.analytics_repo = analytics_repo

    async def handle(self, event):
        print("ANALYTICS USER DELETE EVENT RECEIVED:", event)

        self.analytics_repo.decrement_users_count()