from app.models.ipl_teams import IplTeams


class IplTeamsDAO:
    @staticmethod
    def create_ipl_team(ipl_team_data: dict) -> None:
        ipl_team: IplTeams = IplTeams(**ipl_team_data)
        ipl_team.save()

    @staticmethod
    def get_ipl_team_by_id(ipl_team_id: int) -> IplTeams | dict:
        ipl_team: IplTeams = IplTeams.query.filter_by(id=ipl_team_id).first()
        return ipl_team if ipl_team else {}

    @staticmethod
    def get_id_to_team_name_map() -> dict[int, str]:
        ipl_teams: list[tuple] = IplTeams.query.with_entities(IplTeams.id, IplTeams.code).all()
        return {index: code for index, code in ipl_teams}

    @staticmethod
    def get_team_logo_to_team_id_map() -> dict[int, str]:
        ipl_teams: list[tuple] = IplTeams.query.with_entities(IplTeams.id, IplTeams.image).all()
        return {index: image for index, image in ipl_teams}

    @staticmethod
    def get_id_from_team_name(name: str) -> int:
        ipl_team: IplTeams = IplTeams.query.filter_by(code=name.upper()).first()
        return ipl_team.id if ipl_team else -1

    @staticmethod
    def get_active_ipl_team_ids() -> list[int]:
        ipl_teams: list = IplTeams.query.filter_by(is_active=True).with_entities(IplTeams.id).all()
        return [ipl_team_id[0] for ipl_team_id in ipl_teams]
