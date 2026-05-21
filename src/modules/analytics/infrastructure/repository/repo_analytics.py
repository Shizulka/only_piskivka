from src.modules.analytics.infrastructure.analytics_models import PlaceStatisticsModel, UserStatisticsModel


class AnalyticsRepository:
    def __init__(self, db):
        self.db = db

    def save_place_statistics(self, place_statistics):
        model = PlaceStatisticsModel(
            external_place_id=place_statistics.external_place_id,
            location=place_statistics.location,
            status=place_statistics.status,
            total_reviews=place_statistics.total_reviews
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return model
    
    def delete_place_statistics(self, place_id: int):
        statistics = (
            self.db.query(PlaceStatisticsModel)
            .filter(PlaceStatisticsModel.external_place_id == place_id)
            .first()
        )

        if statistics:
            self.db.delete(statistics)
            self.db.commit()

        return True
    
    def increment_reviews_count(self, place_id: int):
        statistics = (
            self.db.query(PlaceStatisticsModel)
            .filter(PlaceStatisticsModel.external_place_id == place_id)
            .first()
    )

        if statistics:
            statistics.total_reviews += 1
            self.db.commit()
            self.db.refresh(statistics)

        return statistics
    
    def decrement_reviews_count(self, place_id: int):
        statistics = (
            self.db.query(PlaceStatisticsModel)
            .filter(PlaceStatisticsModel.external_place_id == place_id)
            .first()
        )

        if statistics and statistics.total_reviews > 0:
            statistics.total_reviews -= 1
            self.db.commit()
            self.db.refresh(statistics)

        return statistics
    
    def increment_users_count(self):
        statistics = self.db.query(UserStatisticsModel).first()

        if not statistics:
            statistics = UserStatisticsModel(total_users=0)
            self.db.add(statistics)
            self.db.commit()
            self.db.refresh(statistics)

        statistics.total_users += 1
        self.db.commit()
        self.db.refresh(statistics)

        return statistics
    
    def decrement_users_count(self):
        statistics = self.db.query(UserStatisticsModel).first()

        if statistics and statistics.total_users > 0:
            statistics.total_users -= 1
            self.db.commit()
            self.db.refresh(statistics)

        return statistics