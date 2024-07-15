from otree.api import *
import secrets, string

doc = """
Feedback Condition Post Experiment Part
"""


class C(BaseConstants):
    NAME_IN_URL = 'Feedback_PostGame'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    peq_bonus = models.FloatField(initial = 0.0)
    total_earning = models.FloatField(initial = 0.0)
    peq_1 = models.StringField(initial = "")
    peq_2 = models.StringField(initial = "")
    peq_3 = models.StringField(initial = "")
    peq_4 = models.StringField(initial = "")
    peq_5 = models.StringField(initial = "")
    peq_6 = models.StringField(initial = "")
    peq_7 = models.StringField(initial = "")
    peq_8 = models.StringField(initial = "")
    peq_9 = models.StringField(initial = "")
    peq_10 = models.StringField(initial = "")
    peq_11 = models.StringField(initial = "")
    peq_12 = models.StringField(initial = "")
    validation_code = models.StringField(initial = "")

# HELPER FUNCTION
def get_code(length = 16):
    # Define the alphabet: digits and letters (uppercase and lowercase)
    alphabet = string.ascii_letters + string.digits
    # Generate a random string of the specified length
    unique_id = ''.join(secrets.choice(alphabet) for _ in range(length))

    return unique_id

# PAGES
class EarningPage(Page):
    template_name = '_templates/global/EarningPage.html'
    
    @staticmethod
    def is_displayed(player):
        return player.participant.leave_flag == False and player.participant.timeout_flag == False and player.session.vars['group_player_left'] == False
    
    @staticmethod
    def vars_for_template(player):
        bonus_amount = (float(player.participant.personal_account_balance) / 20) * 0.10
        player.peq_bonus = bonus_amount

        return(dict(balance =  format(player.participant.personal_account_balance, ".2f"), bonus = format(bonus_amount, '.2f')))

class PEQ_1(Page):
    template_name = '_templates/global/PEQ_1.html'

    @staticmethod
    def live_method(player, data):
        player.peq_1 = data["inputs"][0]
    
    @staticmethod 
    def is_displayed(player):
        return player.participant.leave_flag == False and player.participant.timeout_flag == False and player.session.vars['group_player_left'] == False

class PEQ_2(Page):
    template_name = '_templates/global/PEQ_2.html'
    
    @staticmethod
    def vars_for_template(player):
        return(dict(is_baseline=False))
    
    @staticmethod
    def live_method(player, data):
        player.peq_2 = data["inputs"][0]
        player.peq_3 = data["inputs"][1]
    
    @staticmethod 
    def is_displayed(player):
        return player.participant.leave_flag == False and player.participant.timeout_flag == False and player.session.vars['group_player_left'] == False

class PEQ_3(Page):
    template_name = '_templates/global/PEQ_3.html'

    @staticmethod
    def live_method(player, data):
        player.peq_4 = data["inputs"][0]
        player.peq_5 = data["inputs"][1]
    
    @staticmethod 
    def is_displayed(player):
        return player.participant.leave_flag == False and player.participant.timeout_flag == False and player.session.vars['group_player_left'] == False

class PEQ_4(Page):
    template_name = '_templates/global/PEQ_4.html'

    @staticmethod
    def live_method(player, data):
        player.peq_6 = data["inputs"][0]
        player.peq_7 = data["inputs"][1]
    
    @staticmethod 
    def is_displayed(player):
        return player.participant.leave_flag == False and player.participant.timeout_flag == False and player.session.vars['group_player_left'] == False

class PEQ_5(Page):
    template_name = '_templates/global/PEQ_5.html'

    @staticmethod
    def live_method(player, data):
        player.peq_8 = data["inputs"][0]
        player.peq_9 = data["inputs"][1]
        player.peq_10 = data["inputs"][2]
    
    @staticmethod 
    def is_displayed(player):
        return player.participant.leave_flag == False and player.participant.timeout_flag == False and player.session.vars['group_player_left'] == False

class PEQ_6(Page):
    template_name = '_templates/global/PEQ_6.html'

    @staticmethod
    def live_method(player, data):
        player.peq_11 = data["inputs"][0]
        player.peq_12 = data["inputs"][1]

    @staticmethod 
    def is_displayed(player):
        return player.participant.leave_flag == False and player.participant.timeout_flag == False and player.session.vars['group_player_left'] == False
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.val_code = get_code()

class Validation_Code_Page(Page):    
    @staticmethod 
    def vars_for_template(player):
        game_earning = (float(player.participant.personal_account_balance) / 20) * 0.10
        total_earning = (game_earning + player.peq_bonus + 1.5) if player.participant.timeout_flag == False else 0 
        player.total_earning = total_earning
        player.validation_code = player.participant.val_code

        return(dict(leave_flag = player.participant.leave_flag, timeout_flag = player.participant.timeout_flag, group_left_flag = player.session.vars['group_player_left'],
                    personal_account_MU = format(player.participant.personal_account_balance, '.2f'), activity_earning = format(game_earning, '.2f'), 
                    peq_earning = format(player.peq_bonus, '.2f'), total_earnings = format(total_earning, '.2f'), validation_code = player.validation_code))


page_sequence = [EarningPage, PEQ_1, PEQ_2, PEQ_3, PEQ_4, PEQ_5, PEQ_6, Validation_Code_Page]
