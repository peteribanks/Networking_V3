from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


author = 'Banks and Fraser'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Trust_Network_Game'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def num_players(self):
        number_of_players = 4
        return number_of_players

    def create_players(self):
        players = {}
        for i in range(1, self.group.num_players() + 1):
            players[i] = self.group.get_player_by_role('player%s' %(i))
        return players


class Player(BasePlayer):
    '''this defines the characteristics of the player class including the variables'''
    endowment = models.IntegerField(blank=True, initial=0)  #amount of starting money
    cp = models.IntegerField(blank=True, initial=0) #multiplier used for investing in others
    promise = models.IntegerField(min=0, max=100, initial=0) #percent that is promised as a return. This also ensures that the numebr will between 0 and 100

    #'''this is used to define the investments for the players'''
    def investments(self):
        investment = {}
        for i in range(1, self.group.num_players() + 1):
            investment[i] = models.IntegerField(min=0, blank=True, initial=0) #investment in player 1
        return investment

    def investmentsag(self):
        investmentsag = {}
        for i in range(1, self.group.num_players() + 1):
            investmentsag[i] = models.IntegerField(min=0, blank=True, initial=0) #investment in player 1
        return investmentsag

    def return_percentage(self):
        return_amounts = {}
        for i in range(1, self.group.num_players() + 1):
            return_amounts[i] = models.IntegerField(min=0, blank=True, initial=0) #investment in player 1
        return return_amounts

    def return_points(self):
        return_points = {}
        for i in range(1, self.group.num_players() + 1):
            return_points[i] = models.FloatField(min=0, blank=True, initial=0) #investment in player 1
        return return_points

    investment_in_me_ag = models.IntegerField(blank=True, initial=0)


    final_total_money = models.FloatField(blank=True, initial=0) #this is the amount of money left over after the player has returned'''

    def network(self):
        network = {'player1': [2, 4], 'player2': [1, 3, 4], 'player3': [2, 4], 'player4': [1, 2, 3]}
        #'''this is the network if the key player1 has a list containing the
         #integers 1 and 4 it means they are networked with players 1 and four and so on'''

        return network

    def role(self):
        '''this function assigns the player ids used in multiple locations extremly important dont change ever'''
        if self.id_in_group == 1:
            return 'player1'
        if self.id_in_group == 2:
            return 'player2'
        if self.id_in_group == 3:
            return 'player3'
        if self.id_in_group == 4:
            return 'player4'





