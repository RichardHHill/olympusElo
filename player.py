import random

# Basic Tennis Simulation
#
# Players will have a name and a strength score
#
# Each point is determined by taking an integer in [0, strength_score)
# Highest integer wins the point
#
# This method is chosen because it's simple and distinct from Elo's
# method of determining expected score
#
# If Player A is better than Player B (draws decided randomly with 50/50 odds):
# P(A >= B's strength) = (A - B) / A
# P(A > B | A < B's strength) = 0.5
# P(A > B) = P(A > B | A < B's strength) * P(A < B's strength) + P(A >= B's strength)
# P(A > B) = 0.5 * B / A + (A - B) / A
# P(A > B) = 1 - 0.5 * B / A

class Player:
    def __init__(self, name, strength):
        self.name = name
        self.strength = strength
        # Assumption: Players will rate themselves around where they should be
        self.elo = 1000 + (strength - 45) * 200
        self.wins = 0
        self.losses = 0
        self.point_wins = 0
        self.game_wins = 0
        self.set_wins = 0
    
    def __str__(self):
        return "Name: {} Strength: {} Elo: {} Wins: {} Losses: {}".format(
            self.name, self.strength, self.elo, self.wins, self.losses)

    def roll(self):
        return random.randrange(self.strength)
    
    def play_point(self, opponent):
        str1 = self.roll()
        str2 = opponent.roll()
        if str1 > str2:
            self.point_wins += 1
            return 1
        elif str1 == str2: # break tie
            if random.randrange(2) == 0:
                self.point_wins += 1
                return 1
        else:
            opponent.point_wins += 1
            return 0

    def play_game(self, opponent):
        s1 = 0
        s2 = 0
        while abs(s1 - s2) < 2 or (s1 < 5 and s2 < 5):
            if self.play_point(opponent):
                s1 += 1
            else:
                s2 += 1
        
        if s1 > s2:
            self.game_wins += 1
        else:
            opponent.game_wins += 1

        return s1 > s2

    def play_set(self, opponent):
        s1 = 0
        s2 = 0
        while abs(s1 - s2) < 2 or (s1 < 6 and s2 < 6):
            if self.play_game(opponent):
                s1 += 1
            else:
                s2 += 1

        if s1 > s2:
            self.set_wins += 1
        else:
            opponent.set_wins += 1

        return s1 > s2

    def play_match(self, opponent):
        s = self.play_set(opponent)
        s += self.play_set(opponent)

        if s == 2:
            self.wins += 1
            opponent.losses += 1
            return 1
        elif s == 0:
            self.losses += 1
            opponent.wins += 1
            return 0
        else:
            if self.play_set(opponent):
                self.wins += 1
                opponent.losses += 1
                return 1
            else:
                self.losses += 1
                opponent.wins += 1
                return 0
