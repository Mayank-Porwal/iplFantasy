from app.models.prediction import Prediction


class PredictionDAO:
    @staticmethod
    def get_predicted_team_for_current_match(match_id: int, user_id: int, team_id: int, league_id: int) -> int | None:
        prediction: Prediction = Prediction.query.filter_by(match_id=match_id,
                                                            user_id=user_id,
                                                            team_id=team_id,
                                                            league_id=league_id).first()

        return prediction.prediction if prediction else None

    @staticmethod
    def set_prediction(data: dict) -> None:
        prediction = Prediction.query.filter_by(match_id=data['match_id'],
                                                user_id=data['user_id'],
                                                team_id=data['team_id'],
                                                league_id=data['league_id']).first()
        if prediction:
            prediction.prediction = data['prediction']
        else:
            prediction = Prediction(**data)
        prediction.save()
