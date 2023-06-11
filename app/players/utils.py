def get_player_object(player):
    return {'id': player.id, 'name': player.name, 'cap': player.cap, 'category': player.category,
            'img': player.image_file, 'team': player.ipl_team}
