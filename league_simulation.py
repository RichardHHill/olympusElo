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

    # Only chart players who have played at least 5 games
    players = list(filter(lambda x: x.wins + x.losses > 5, players))

    win_pcts = list(map(lambda x: x.wins / (x.wins + x.losses), players))
    plt.hist(win_pcts)
    plt.title("Win Percentages")
    plt.xlabel("Win Rate (%)")
    plt.ylabel("Count")
    plt.show()

    # Compare elo estimation to how they'd actually do
    score_dif = [0] * (len(players) ** 2)
    i = 0
    for i in range(len(players)):
        for j in range(len(players)):
            if i < j:
                p1 = players[i]
                p2 = players[j]
                est_wins = 100 / (1 + 10 ** ((p2.elo - p1.elo) / 400))

                act_wins = 0
                for _ in range(100):
                    act_wins += match_scores(p1, p2)
                
                score_dif[i] = est_wins - act_wins
                
    
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

def match_scores(p1, p2, mode = None):
    if mode is None:
        mode = random.choice(["Match", "Set", "Game", "Point"])

    # start and end number of wins
    p1_points_start = p1.point_wins
    p1_games_start = p1.game_wins
    p1_sets_start = p1.set_wins
    p2_points_start = p2.point_wins
    p2_games_start = p2.game_wins
    p2_sets_start = p2.set_wins

    result = p1.play_match(p2)

    p1_points = p1.point_wins - p1_points_start
    p1_games = p1.game_wins - p1_games_start
    p1_sets = p1.set_wins - p1_sets_start
    p2_points = p2.point_wins - p2_points_start
    p2_games = p2.game_wins - p2_games_start
    p2_sets = p2.set_wins - p2_sets_start
    
    total_points = p1_points + p2_points
    total_games = p1_games + p2_games
    total_sets = p1_sets + p2_sets

    w1 = result

    if mode == "Set":
        # Winning 2-0 gives a score of 1
        # Winning 2-1 gives a score of 0.77
        w1 = w1 * 0.3 + (p1_sets / total_sets) * 0.7
    elif mode == "Game":
        w1 = w1 * 0.2 + (p1_sets / total_sets) * 0.3 + (p1_games / total_games) * 0.5
    elif mode == "Point":
        w1 = w1 * 0.1 + (p1_sets / total_sets) * 0.2 + (p1_games / total_games) * 0.3 + (p1_points / total_points) * 0.4

    return w1


def test_simple_league():
    STARTING_SIZE = 20
    K_FACTORS = [24, 28, 36, 48] 
    modes = ["Match", "Set", "Game", "Point"]

    all_players = list(
        map(lambda x: Player("p" + str(x), random.randrange(40,51)),
        range(STARTING_SIZE)))

    games_played = 0

    while games_played < 200:
        p1 = random.choice(all_players)
        p2 = pick_good_match(all_players, p1.elo)
        
        if p1 is not p2:
            #TODO other modes 
            mode_index = random.randrange(4)

            r1 = p1.elo
            r2 = p2.elo

            e1 = 1 / (1 + 10 ** ((r2 - r1) / 400))
            e2 = 1 / (1 + 10 ** ((r1 - r2) / 400))

            s1 = match_scores(p1, p2, modes[mode_index])
            s2 = 1 - s1

            p1.elo += K_FACTORS[mode_index] * (s1 - e1)
            p2.elo += K_FACTORS[mode_index] * (s2 - e2)

        games_played += 1

    summarize_season(all_players)

def survey_weight(p1, p2):
    """Helper for comparing survey ratings to weight the elo score 
    of a new player"""
    if abs(p1.survey_rating - p2.survey_rating) > 1 or p1.wins + p1.losses < 5:
        return 0
    else:
        return 2 - abs(p1.survey_rating - p2.survey_rating)

def guess_elo(players, new_player):
    """When adding a new player, guess that player's
    elo based on the elo of players with similar ratings"""

    elo_scores = np.array(list(map(lambda x: x.elo, players)))

    weights = np.array(list(map(
        lambda x: survey_weight(x, new_player), players)))

    if sum(weights) == 0:
        return new_player.elo
    else:
        weights = weights / sum(weights)

        return sum(weights * elo_scores)


def test_league_add_new():
    STARTING_SIZE = 20
    K_FACTORS = [24, 28, 36, 48] 
    modes = ["Match", "Set", "Game", "Point"]

    all_players = list(
        map(lambda x: Player("p" + str(x), random.randrange(40,51)),
        range(STARTING_SIZE)))

    games_played = 0

    while games_played < 400:
        p1 = random.choice(all_players)
        p2 = pick_good_match(all_players, p1.elo)
        
        if p1 is not p2:
            #TODO other modes 
            mode_index = random.randrange(4)

            r1 = p1.elo
            r2 = p2.elo

            e1 = 1 / (1 + 10 ** ((r2 - r1) / 400))
            e2 = 1 / (1 + 10 ** ((r1 - r2) / 400))

            s1 = match_scores(p1, p2, modes[mode_index])
            s2 = 1 - s1

            p1_new = p1.wins + p1.losses < 5
            p2_new = p2.wins + p2.losses < 5

            # New players playing against experienced players
            # have their scores updated more to help them more 
            # quickly find their elo rating
            if p1_new and not p2_new:
                mult_1, mult_2 = 2, 0.5
            elif p2_new and not p1_new:
                mult_1, mult_2 = 0.5, 2
            else:
                mult_1, mult_2 = 1, 1

            p1.elo += K_FACTORS[mode_index] * (s1 - e1) * mult_1
            p2.elo += K_FACTORS[mode_index] * (s2 - e2) * mult_2

            # Add new players randomly
            if random.randrange(15) == 0:
                new_player = Player("p" + str(len(all_players)),
                 random.randrange(40,51))

                new_player.elo = guess_elo(all_players, new_player)

                all_players.append(new_player)

        games_played += 1

    summarize_season(all_players) 

test_simple_league()
test_league_add_new()