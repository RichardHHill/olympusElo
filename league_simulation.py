import random
import numpy as np
import matplotlib.pyplot as plt
from player import Player


# Simulation of how our elo system would play out

# Players at launch

def summarize_season(players):
    """After playing games, summarize the elo scores
    of players and their significance versus their strengths
    as players
    
    We would like to see each player end up with a healthy number
    of wins and losses, which means they're matched with appropriate
    partners"""

    for player in players:
        print(player)

    win_pcts = list(map(lambda x: x.wins / (x.wins + x.losses), players))
    plt.hist(win_pcts)
    plt.show()

def test_simple_league():
    STARTING_SIZE = 20
    K_FACTOR = 32
    modes = ["Match", "Set", "Game", "Point"]

    all_players = list(
        map(lambda x: Player("p" + str(x), random.randrange(40,51)),
        range(STARTING_SIZE)))

    games_played = 0

    while games_played < 1000:
        p1 = random.choice(all_players)
        p2 = random.choice(all_players)
        
        if p1 is not p2:
            #TODO other modes 
            recording_mode = "Match"

            r1 = p1.elo
            r2 = p2.elo

            e1 = 1 / (1 + 10 ** ((r2 - r1) / 400))
            e2 = 1 / (1 + 10 ** ((r1 - r2) / 400))

            if p1.play_match(p2):
                s1 = 1
                s2 = 0
                p1.wins += 1
                p2.losses += 1
            else:
                s1 = 0
                s2 = 1
                p1.losses += 1
                p2.wins += 1

            p1.elo += K_FACTOR * (s1 - e1)
            p2.elo += K_FACTOR * (s2 - e2)

        games_played += 1

    summarize_season(all_players)

test_simple_league()  