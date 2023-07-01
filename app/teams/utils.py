def get_team_object(team):
    return {'id': team.id, 'name': team.name, 'players': team.players, 'user': team.user_id}
