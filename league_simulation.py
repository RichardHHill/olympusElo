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
    plt.title("Win Percentages")
    plt.xlabel("Win Rate (%)")
    plt.ylabel("Count")
    plt.show()

    # Compare elo estimation to how they'd actually do
    score_dif = [0] * (len(players) ** 2)
    i = 0
    for p1 in players:
        for p2 in players:
            if p1 is not p2:
                est_wins = 100 / (1 + 10 ** ((p2.elo - p1.elo) / 400))

                act_wins = 0
                for _ in range(100):
                    act_wins += p1.play_match(p2)
                
                score_dif[i] = est_wins - act_wins
                i += 1
    
    plt.hist(score_dif)
    plt.title("Accuracy of Elo Prediction")
    plt.xlabel("Expected/Actual Difference (%)")
    plt.ylabel("Count")
    plt.show()

def match_weight(elo1, elo2):
    if abs(elo1 - elo2) > 300:
        return 0
    else:
        return 300 - abs(elo1 - elo2)

def pick_good_match(players, opponent_elo):
    """Pick a random opponent with probabilities weighted
    to those closer in skill"""

    weights = np.array(list(map(lambda x: match_weight(x.elo, opponent_elo), players)))
    weights = weights / sum(weights)

    return np.random.choice(players, p = weights)

def test_simple_league():
    STARTING_SIZE = 20
    K_FACTOR = 32
    modes = ["Match", "Set", "Game", "Point"]

    all_players = list(
        map(lambda x: Player("p" + str(x), random.randrange(40,51)),
        range(STARTING_SIZE)))

    games_played = 0

    while games_played < 10000:
        p1 = random.choice(all_players)
        p2 = pick_good_match(all_players, p1.elo)
        
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