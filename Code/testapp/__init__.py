from otree.api import *
import time

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'testapp'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class TestPage(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.wait_page_arrival = time.time()
        player.participant.personal_account_balance = 0.0
        player.participant.leave_flag = False
        player.participant.timeout_flag = False
        player.session.vars['group_player_left'] = False


page_sequence = [TestPage]
