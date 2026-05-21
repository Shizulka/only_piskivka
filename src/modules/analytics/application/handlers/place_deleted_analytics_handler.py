class PlaceDeletedAnalyticsHandler:
    def __init__(self, analytics_repo):
        self.analytics_repo = analytics_repo

    async def handle(self, event):
        print("ANALYTICS DELETE EVENT RECEIVED:", event)

        self.analytics_repo.delete_place_statistics(event.place_id)