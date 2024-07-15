from otree.api import *
import time, random, json, secrets, string

doc = """
Baseline Experiment
"""


class C(BaseConstants):
    NAME_IN_URL = 'Baseline_Game'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 40


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    wait_dict = models.StringField(initial = '')
    group_contribution = models.FloatField(initial=0.0)
    split = models.FloatField(initial=0.0)
    contribution_cnter = models.IntegerField(initial = 0)      


class Player(BasePlayer):
    additional_question_1 = models.StringField(initial="")
    additional_question_2 = models.StringField(initial="")
    additional_question_3 = models.StringField(initial="")
    round_contribution = models.FloatField(initial=0.0)
    allowance_balance =  models.FloatField(initial=20.0)


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
    
    @staticmethod
    def after_all_players_arrive(group):
        players = group.get_players()

        for player in players:
            player.participant.p2_role = random.choice(['human', 'bot']) if player.session.config['randomize_roles'] else player.session.config['baseline_roles'][0]
            player.participant.p3_role = random.choice(['human', 'bot']) if player.session.config['randomize_roles'] else player.session.config['baseline_roles'][1]
            player.participant.p4_role = random.choice(['human', 'bot']) if player.session.config['randomize_roles'] else player.session.config['baseline_roles'][2]
 
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 and player.participant.leave_flag == False
    

    body_text= '''
        <style>
            div, li{
                color: #02006c;
            }
            .card-body{
                margin: 0;
                padding: 0;
            }
        </style>
        <script>
            function startTimer() {
                let timer = document.getElementById('timer');
                let seconds = 0;
                let minutes = 0;
                const interval = setInterval(() => {
                    seconds++;
                    if (seconds == 60) {
                        seconds = 0;
                        minutes++;
                    }
                    let displaySeconds = seconds < 10 ? '0' + seconds : seconds;
                    let displayMinutes = minutes < 10 ? '0' + minutes : minutes;
                    timer.textContent = 'Time since waiting: ' + displayMinutes + ':' + displaySeconds;

                }, 1000);
            }

            window.onload = startTimer;
        </script>
        <div id='waitDiv'>
            <ul>
                <li>The activity will start as soon as all other participants have joined your group.</li>
                <li>A beep will alert you when everyone has arrived, and the activity will start <strong style="color: red">immediately</strong>.</li>
                <li><strong style="color:red;">Do not leave this page while waiting</strong>, otherwise we will not be able to compensate you.</li>
                <li>You can earn a bonus up to $9.24 if you finish the activity.</li>
                <li>If your group does not complete in 10 minutes, you will get a completion code and be paid your show-up fee of $1.50.</li>
            </ul>
            <div id="timer" style="display:flex; align-items:center; justify-content:center; margin-top:2rem">Time since waiting: 00:00</div>
        </div>
    '''
    
class RolePage(Page):
    timeout_seconds = 10
    template_name = '_templates/global/RolePage.html'

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 and player.participant.leave_flag == False
    
    @staticmethod
    def vars_for_template(player):
        return(dict(p2_role = player.participant.p2_role, p3_role = player.participant.p3_role, p4_role = player.participant.p4_role, is_baseline = True, condition = get_condition(player.participant.p2_role, player.participant.p3_role, player.participant.p4_role)))
    

class PGQ_1(Page):
    timeout_seconds = 180

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 and player.participant.leave_flag == False
    
    @staticmethod
    def vars_for_template(player):
        return(dict(p2_role = player.participant.p2_role, p3_role = player.participant.p3_role, p4_role = player.participant.p4_role))
    
    @staticmethod
    def live_method(player, data):
        player.additional_question_1 = data["inputs"][0]

class PGQ_2(Page):
    timeout_seconds = 180

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 and player.participant.leave_flag == False
    
    @staticmethod
    def vars_for_template(player):
        return(dict(p2_role = player.participant.p2_role, p3_role = player.participant.p3_role, p4_role = player.participant.p4_role))
    
    @staticmethod
    def live_method(player, data):
        player.additional_question_2 = json.dumps(data["inputs"])

class PGQ_3(Page):
    timeout_seconds = 240

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 and player.participant.leave_flag == False
    
    @staticmethod
    def vars_for_template(player):
        return(dict(p2_role = player.participant.p2_role, p3_role = player.participant.p3_role, p4_role = player.participant.p4_role))
    
    @staticmethod
    def live_method(player, data):
        player.additional_question_3 = json.dumps(data["inputs"])

    @staticmethod
    def before_next_page(player, timeout_happened):
        if(timeout_happened):
            player.participant.additional_question_MU = 0
        else:
            player.participant.additional_question_MU = random.randint(0, 20)

class InterfaceExamplePage(WaitPage):
    template_name = 'Baseline_Game/InterfaceExamplePage.html'
    
    @staticmethod
    def is_displayed(player):
        return player.round_number == -1

class GIExamplePage(Page):   
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 and player.participant.leave_flag == False
    
    @staticmethod
    def live_method(player, data):
        group = player.group
        if group.wait_dict == "": 
            group.wait_dict = """{"test": 1}"""
        
        wt = group.wait_dict
        wait_dict = json.loads(wt)
        if(str(player.id_in_group) not in wait_dict):
            wait_dict[player.id_in_group] = 1
        
        group.wait_dict = json.dumps(wait_dict)

        if(len(wait_dict) == 5):
            return {0: {"type": "next-page"}}
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.personal_account_balance = 0
        player.participant.timeout_flag = False
        
class GameInterface(Page):
    timeout_seconds = 30

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
        if timeout_happened:
            player.participant.timeout_flag = True
            player.participant.personal_account_balance = 0
            player.participant.additional_question_MU = 0
            player_list = player.group.get_players()
            for p in player_list:
                p.participant.val_code = get_code()
            player.session.vars['group_player_left'] = True
        
class RoundWaitPage(WaitPage):
    body_text = 'Please wait for other participants...'
    
    @staticmethod
    def is_displayed(player):
        return player.participant.leave_flag == False and player.participant.timeout_flag == False and player.session.vars['group_player_left'] == False
    
    @staticmethod
    def after_all_players_arrive(group):
        group.split = ((group.group_contribution * 1.6) / 4)
        for p in group.get_players():
            p.participant.personal_account_balance = p.participant.personal_account_balance + group.split + p.allowance_balance


class RoundSummaryPage(Page):
    timeout_seconds = 15

    @staticmethod
    def is_displayed(player):
        return player.participant.leave_flag == False and player.participant.timeout_flag == False and player.session.vars['group_player_left'] == False
    
    @staticmethod
    def js_vars(player):
        return(dict(group_contribution = player.group.group_contribution))
    
    @staticmethod
    def vars_for_template(player):
        return(dict(p2_role = player.participant.p2_role, p3_role = player.participant.p3_role, p4_role = player.participant.p4_role, contribution = format(player.round_contribution, '.2f'), remaining_balance = format(player.allowance_balance, '.2f'), group_contribution = format((player.group.group_contribution * 1.6), '.2f'), split = format(player.group.split, '.2f'), current_balance = format(player.participant.personal_account_balance, '.2f')))


page_sequence = [WaitingPage, RolePage, PGQ_1, PGQ_2, PGQ_3, GIExamplePage, GameInterface, RoundWaitPage, RoundSummaryPage]
