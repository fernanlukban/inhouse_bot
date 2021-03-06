import itertools
import math
import os
import trueskill

# Folders utilities
base_folder = os.path.join(os.path.expanduser("~"), '.config', 'inhouse_bot')
token_location = os.path.join(base_folder, 'discord_token.txt')

if not os.path.exists(base_folder):
    os.makedirs(base_folder)

# Discord token acquisition
try:
    with open(token_location) as file:
        discord_token = file.read()
except FileNotFoundError:
    print(f'Discord token not found\n'
          f'If you don’t have one, you can create it at https://discord.com/developers/applications\n'
          f'It will be saved in clear text at {os.path.join(base_folder, "discord_token.txt")}\n'
          f'Please input the bot’s Discord token:')
    discord_token = input()
    with open(token_location, 'w+') as file:
        file.write(discord_token)


# Trueskill utilities
def win_probability(team1, team2):
    """
    :param team1: list of Rating objects
    :param team2: list of Rating objects
    :return: expected win probability of team1 over team2
    """
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denominator = math.sqrt(size * (trueskill.BETA * trueskill.BETA) + sum_sigma)
    ts = trueskill.global_env()
    return ts.cdf(delta_mu / denominator)


def trueskill_blue_side_winrate(players: dict) -> float:
    """
    Computes the expected winrate for blue side based on trueskill ratings

    :param players: [team, role] -> Player dictionary
    :return: the expected blue side winrate
    """
    return win_probability([trueskill.Rating(players[team, role].ratings[role].trueskill_mu,
                                             players[team, role].ratings[role].trueskill_sigma)
                            for team, role in players if team == 'blue'],
                           [trueskill.Rating(players[team, role].ratings[role].trueskill_mu,
                                             players[team, role].ratings[role].trueskill_sigma)
                            for team, role in players if team == 'red'])
