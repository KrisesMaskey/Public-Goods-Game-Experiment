from otree.api import *
import time, random, json, secrets, string

doc = """
PGG Feedback Condition
"""


class C(BaseConstants):
    NAME_IN_URL = 'Feedback_Game'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 40


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    group_contribution = models.FloatField(initial=0.0)
    split = models.FloatField(initial=0.0)
    contribution_cnter = models.IntegerField(initial = 0)   
    contribution_map = models.StringField(initial = '')


class Player(BasePlayer):
    round_contribution = models.FloatField(initial=0.0)
    allowance_balance =  models.FloatField(initial=20.0)
    label_to_id_map = models.StringField(initial="")
    id_to_label_map = models.StringField(initial="")


# MODULE FUNCTIONS
def get_condition(p1, p2, p3):
    bots_count = sum([p1 == 'bot', p2 == 'bot', p3 == 'bot'])
    conditions = {0: 1, 1: 2, 2: 3, 3: 4}
    return conditions[bots_count]

def get_code(length = 16):
    # Define the alphabet: digits and letters (uppercase and lowercase)
    alphabet = string.ascii_letters + string.digits
    # Generate a random string of the specified length
    unique_id = ''.join(secrets.choice(alphabet) for _ in range(length))
    return unique_id

def waiting_too_long(player):
    participant = player.participant
    return (time.time() - participant.wait_page_arrival) > 600

def group_by_arrival_time_method(subsession, waiting_players):
    if len(waiting_players) >= 4:
        return waiting_players[:4]
    for player in waiting_players:
        if waiting_too_long(player):
            # make a single-player group.
            player.participant.leave_flag = True
            player.participant.val_code = get_code()
            return [player]


# PAGES
class WaitingPage(WaitPage):
    group_by_arrival_time = True
    template_name = '_templates/global/WaitingPage.html'
    
    @staticmethod
    def after_all_players_arrive(group):
        players = group.get_players()
        
        if(len(players) > 1):
            for player in players:
                other_players = [p.id_in_group for p in players if p.id_in_group != player.id_in_group]
                
                p_map = {
                    'B': other_players[0],
                    'C': other_players[1],
                    'D': other_players[2]
                }
                reverse_map = {v: k for k, v in p_map.items()}
                
                player.label_to_id_map = json.dumps(p_map)
                player.id_to_label_map = json.dumps(reverse_map)
                player.participant.p2_role = random.choice(['human', 'bot']) if player.session.config['randomize_roles'] else player.session.config['feedback_roles'][0]
                player.participant.p3_role = random.choice(['human', 'bot']) if player.session.config['randomize_roles'] else player.session.config['feedback_roles'][1]
                player.participant.p4_role = random.choice(['human', 'bot']) if player.session.config['randomize_roles'] else player.session.config['feedback_roles'][2]

    
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 and player.participant.leave_flag == False
    
    @staticmethod
    def vars_for_template(player):
        return(dict(is_baseline = False))

    
class RolePage(Page):
    timeout_seconds = 10
    template_name = '_templates/global/RolePage.html'

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 and player.participant.leave_flag == False
    
    @staticmethod
    def vars_for_template(player):
        return(dict(p2_role = player.participant.p2_role, p3_role = player.participant.p3_role, p4_role = player.participant.p4_role, is_baseline = False, condition = get_condition(player.participant.p2_role, player.participant.p3_role, player.participant.p4_role)))
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.personal_account_balance = 50
        player.participant.timeout_flag = False
        player.session.vars['group_player_left'] = False


class GIExamplePage(Page):
    timeout_seconds = 75
        
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 and player.participant.leave_flag == False
        

class GameInterface(Page):
    timeout_seconds = 20
    template_name = '_templates/global/GameInterface.html'

    @staticmethod
    def is_displayed(player):
        return player.participant.leave_flag == False and player.participant.timeout_flag == False and player.session.vars['group_player_left'] == False

    @staticmethod
    def vars_for_template(player):
        return(dict(p2_role = player.participant.p2_role, p3_role = player.participant.p3_role, p4_role = player.participant.p4_role, balance = format(player.participant.personal_account_balance, '.2f')))
    
    @staticmethod
    def live_method(player, data):
        if(data["type"] == 'game-page'):
            group = player.group
            player.round_contribution = float(data["inputs"][0])
            player.allowance_balance -= player.round_contribution
            group.group_contribution += player.round_contribution
            group.contribution_cnter += 1

            return({0: {'type':'contribution-submitted','progress': group.contribution_cnter}})
        
    @staticmethod
    def before_next_page(player, timeout_happened):
        # Logic if player drops out -----
        if timeout_happened:
            player.participant.timeout_flag = True
            player.participant.personal_account_balance = 0
            player_list = player.group.get_players()
            for p in player_list:
                p.participant.val_code = get_code()
            player.session.vars['group_player_left'] = True
        
        if player.round_number > 1:
            previous_round_player = player.in_round(player.round_number - 1)
            player.label_to_id_map = previous_round_player.label_to_id_map
            player.id_to_label_map = previous_round_player.id_to_label_map
        
        group = player.group
        contribution_map = {}
        for p in group.get_players():
            contribution_map[p.id_in_group] = p.round_contribution
        group.contribution_map = json.dumps(contribution_map)

        
class RoundWaitPage_1(WaitPage):
    body_text = 'Please wait for other participants...'
    
    @staticmethod
    def is_displayed(player):
        return player.participant.leave_flag == False and player.participant.timeout_flag == False and player.session.vars['group_player_left'] == False
    
    @staticmethod
    def after_all_players_arrive(group):
        group.split = ((group.group_contribution * 1.6) / 4)
        for p in group.get_players():
            p.participant.personal_account_balance = p.participant.personal_account_balance + group.split + p.allowance_balance


class RoundSummaryPage_1(Page):
    timeout_seconds = 10
    template_name = '_templates/global/RoundSummaryPage_1.html'

    @staticmethod
    def is_displayed(player):
        return player.participant.leave_flag == False and player.participant.timeout_flag == False and player.session.vars['group_player_left'] == False
    
    @staticmethod
    def js_vars(player):
        return(dict(group_contribution = player.group.group_contribution))
    
    @staticmethod
    def vars_for_template(player):
        return(dict(p2_role = player.participant.p2_role, p3_role = player.participant.p3_role, p4_role = player.participant.p4_role, remaining_balance = format(player.allowance_balance, '.2f'), group_contribution = format((player.group.group_contribution * 1.6), '.2f'), split = format(player.group.split, '.2f'), current_balance = format(player.participant.personal_account_balance, '.2f')))        
        

class FeedbackPage(Page):
    timeout_seconds = 15

    @staticmethod
    def is_displayed(player):
        return (player.participant.leave_flag == False) and (player.participant.timeout_flag == False) and player.session.vars['group_player_left'] == False
    
    @staticmethod
    def vars_for_template(player):
        contribution_map = json.loads(player.group.contribution_map)
        p_map = json.loads(player.label_to_id_map)
        contribution_list = [contribution_map[str(p_map[l])] for l in ["B", "C", "D"]]
        return(dict(p2_role = player.participant.p2_role, p3_role = player.participant.p3_role, p4_role = player.participant.p4_role,
                    player_contribution = player.round_contribution, contribution = contribution_list))


class RoundWaitPage_2(WaitPage):
    body_text = 'Please wait for other participants...'
    
    @staticmethod
    def is_displayed(player):
        return player.participant.leave_flag == False and player.participant.timeout_flag == False and player.session.vars['group_player_left'] == False


class RoundSummaryPage_2(Page):
    timeout_seconds = 15

    @staticmethod
    def is_displayed(player):
        return player.participant.leave_flag == False and player.participant.timeout_flag == False and player.session.vars['group_player_left'] == False
    
    @staticmethod
    def vars_for_template(player):
        round_earning = player.allowance_balance + player.group.split
                                    
        return(dict(remaining_balance = format(player.allowance_balance, '.2f'), split = format(player.group.split, '.2f'), 
                    current_balance = format(round_earning, '.2f')))


page_sequence = [WaitingPage, GIExamplePage, RolePage, GameInterface, RoundWaitPage_1, RoundSummaryPage_1, FeedbackPage, RoundWaitPage_2, RoundSummaryPage_2]
