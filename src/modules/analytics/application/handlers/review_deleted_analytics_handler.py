class ReviewDeletedAnalyticsHandler:
    def __init__(self, analytics_repo):
        self.analytics_repo = analytics_repo

    async def handle(self, event):
        print("ANALYTICS REVIEW DELETE EVENT RECEIVED:", event)

        self.analytics_repo.decrement_reviews_count(event.place_id)