from app.dao.leagues import LeagueDAO
from app.dao.match import MatchDAO
from app.models.leagues import League
from app.models.match import Match
from app.service.snapshot import SnapshotService
from app import scheduler
from app import create_app

snapshot_service = SnapshotService()


@scheduler.task(id='abc', trigger='date', run_date='2024-03-25 11:10:22')
def submit_all_teams_for_all_leagues():
    with create_app().app_context():
        match: Match = MatchDAO.get_current_match_id_by_status()
        leagues: list[League] = LeagueDAO.get_all_active_leagues()
        print(match.id)
        print('started')

        try:
            # snapshot_service.submit_all_teams_for_league(match.id, 53)
            for league in leagues:
                print(f'League id: {league.id}')
                snapshot_service.submit_all_teams_for_league(match.id, league.id)
            return {'message': 'Cron job to submit all teams for all leagues ran successfully'}
        except Exception as e:
            return {'message': f'Failed with error: {e}'}
