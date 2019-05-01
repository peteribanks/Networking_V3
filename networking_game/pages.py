from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

#MyPage is now Information1
class Information1(Page):
    '''this is just an intro page it takes the promised percentage and informs the player about their own characteristics
    such as their amount of starting money and multiplier'''
    form_model = 'player'
    form_fields = ['promise']

#WaitPage1 First WaitPage between Information1 and Information2
class WaitPage1(WaitPage):
    '''wait page so that information can all be collected before pages that use
    them. such as investment and return investment'''
    def after_all_players_arrive(self):
        pass


class WaitPage2(WaitPage):
    def after_all_players_arrive(self):
        players = self.group.create_players()

        for playernum, player in players.items():
            total_investments = 0
            for i in range(1, self.group.num_players() + 1):
                total_investments += player.investments()[i]
            for i in range(1, self.group.num_players() + 1):
                player.investments()[playernum] = player.endowment - total_investments

        for playernum, player in players.items():
            for i in range(1, self.group.num_players() + 1):
                if playernum != i and player.investments()[i] != None:
                    player.investmentsag()[i] = player.investments()[i] * player.cp



class WaitPage3(WaitPage):

    def after_all_players_arrive(self):
        players = self.group.create_players()

        for playernum, player in players.items():
            for i in range(1, (self.group.num_players() + 1)):
                if playernum != i:
                    player.return_points()[i] = ((players[i].investmentag[playernum] * player.return_percentage()[i]) / 100)
                else:
                    player.return_points()[i] = 0


class MyPageWaitPage(Page):
    '''this is only used on the first page to assign the multiplier and and starting money'''
    timeout_seconds = 1 #amount of time spent on page. player shouldnt even realize this page happened
    def before_next_page(self):
        '''if you want to change the parameters for the endowment or starting money do that here'''
        self.player.cp = random.randint(1,10)
        self.player.endowment = random.randint(50, 500)

class FinalPage(Page):
    '''page that prints results for player'''
    def vars_for_template(self):
        '''tells django the python variables that it will be using'''

        players = self.group.create_players() #list of players
        Final_Page_Var = {} #creates a dictonary of variables

        for playernum, player in players.items():
            string = 'promise%s' % (playernum) #defined promises for each player
            Final_Page_Var[string] = player.promise

        for playernum, player in players.items():
            strings = {}

            for i in range(1, self.group.num_players() + 1):
                strings[i] = 'player%s_return%s' % (playernum, i) # investment in player 1

        for stringnum, string in strings.items():
            for i in range(1, self.group.num_players() + 1):
                Final_Page_Var[string] = player.return_percentage()[i]

        for playernum, player in players.items():
            string1 = 'p%snetworks' % (playernum)
            string2 = 'player%s' % (playernum)
            Final_Page_Var[string1] = self.player.network()[string2]

        for playernum, player in players.items():
            strings = {}
            for i in range(1, self.group.num_players() + 1):
                strings[i] = 'player%s_return%s' % (playernum, i)

        for stringnum, string in strings.items():
            for i in range(1, self.group.num_players() + 1):
                Final_Page_Var[string] = player.return_points()[i]





        return Final_Page_Var

class Invest(Page):
    '''this page is used to defined the investment stage'''
    def vars_for_template(self):
        '''collects the player ids'''
        players = self.group.create_players() #list of players
        Final_Page_Var = {} #creates a dictonary of variables

        for playernum, player in players.items():
            string = 'promise%s' %(playernum) #pulls promises and adds them to dictonary
            Final_Page_Var[string] = player.promise

        for playernum, player in players.items():
            string = 'player%scp' %(playernum) #pulls promises and adds them to dictonary
            Final_Page_Var[string] = player.cp

        for playernum, player in players.items():
            string1 = 'p%snetworks' % (playernum)
            string2 = 'player%s' % (playernum)
            Final_Page_Var[string1] = self.player.network()[string2]


        return Final_Page_Var #return django variables



    form_model = 'player'
    form_fields = ['investment1', 'investment2', 'investment3', 'investment4']



    def error_message(self, values):

        investment1 = values['investment1']
        investment2 = values['investment2']
        investment3 = values['investment3']
        investment4 = values['investment4']
        #investments = [investment1, investment2, investment3, investment4]

        if investment1 == None:
            investment1 = 0

        if investment2 == None:
            investment2 = 0

        if investment3 == None:
            investment3 = 0

        if investment4 == None:
            investment4 = 0


        if investment1 + investment2 + investment3 + investment4 > self.player.endowment:
            return 'You invested more money than you have'

class InvestmentReturn(Page):
    '''takes back how much money someone wants to return'''


    form_model = 'player'
    form_fields = ['return1', 'return2', 'return3', 'return4']



    def vars_for_template(self):

        players = self.group.create_players() #list of players
        Final_Page_Var = {} #creates a dictonary of variables

        for playernum, player in players.items():
            for i in range(1, self.group.num_players() + 1):
                player.investment_in_me_ag += players[i].investmentsag[playernum]

        for playernum, player in players.items():
            string1 = 'p%snetworks' % (playernum)
            string2 = 'player%s' % (playernum)
            Final_Page_Var[string1] = self.player.network()[string2]

        for playernum, player in players.items():
            for i in range(1, self.group.num_players() + 1):
                strings = {}
                strings[i] = 'player%s_investment%s' % (playernum, i)

        for stringnum, string in strings.items():
            for i in range(1, self.group.num_players() + 1):
                Final_Page_Var[string] = player.investments()[i]

        for playernum, player in players.items():
            for i in range(1, self.group.num_players() + 1):
                strings = {}
                strings[i] = 'player%s_investment%ag' % (playernum, i)

        for stringnum, string in strings.items():
            for i in range(1, self.group.num_players() + 1):
                Final_Page_Var[string] = player.investmentsag()[i]

        for playernum, player in players.items():
            string1 = 'p%snetworks' % (playernum)
            string2 = 'player%s' % (playernum)
            Final_Page_Var[string1] = self.player.network()[string2]



        return Final_Page_Var


    def before_next_page(self):
        '''defines the players final money by taking the amount of money invest minus the amount given back'''
        self.player.final_total_money = self.player.investment_in_me_ag - self.player.return_pts1 - self.player.return_pts2 - self.player.return_pts3 - self.player.return_pts4

    def error_message(self, values):
        '''throws up an error message if the player is trying to return more money than they have'''
        return1 = values['return1']
        if return1 == None:
            return1 = 0
        return2 = values['return2']
        if return2 == None:
            return2 = 0
        return3 = values['return3']
        if return3 == None:
            return3 = 0
        return4 = values['return4']
        if return4 == None:
            return4 = 0





#tells django what order to show the pages in
page_sequence = [
    MyPageWaitPage,
    Information1,
    WaitPage1,
    Invest,
    WaitPage2,
    InvestmentReturn,
    WaitPage3,
    FinalPage
]