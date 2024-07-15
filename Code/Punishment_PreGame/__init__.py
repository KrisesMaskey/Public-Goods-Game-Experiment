from otree.api import *
import time, json

doc = """
Punishment Condition Pre-Experiment Part
"""


class C(BaseConstants):
    NAME_IN_URL = 'Punishment_PreGame'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    accept_consent_flag = models.BooleanField(initial = False)
    mturk_id = models.StringField(initial= '')
    age = models.IntegerField(initial=None)
    gender = models.StringField(initial='')
    race = models.StringField(initial='')
    location = models.StringField(initial='')
    failed_quiz_1_count = models.IntegerField(initial= 0)
    failed_quiz_2_count = models.IntegerField(initial= 0)


# PAGES
class ProceedPage(Page):
    template_name = "_templates/global/ProceedPage.html"


class ConsentForm(Page):
    template_name = '_templates/global/Consent_Form.html'

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.accept_consent_flag = True


class ID(Page):
    template_name = '_templates/global/MTURK_ID.html'
    
    @staticmethod
    def live_method(player, data):
        if(data["type"] == 'mturk-id'):
            player.mturk_id = data["id"]


class PreliminaryQuestions(Page):
    template_name = '_templates/global/Preliminary_Questions.html'

    @staticmethod
    def live_method(player, data):
        if(data["type"] == 'preliminary-questions'):
            player.age = data["age"]
            player.gender = data["gender"]
            player.race = data["race"]
            player.location = data["location"]


class Instructions(Page):
    @staticmethod
    def live_method(player, data):
        if(data['type'] == 'quiz-submit'):
            dat = json.loads(data["answers"])
            res = ["a2", "a1", "a1", "a2"] == dat
            if(res == False):
                player.failed_quiz_1_count += 1
            
            return({player.id_in_group: {"type": "quiz-result", "response": res, "cnt": player.failed_quiz_1_count}})

class Quiz_1_Failed(Page):
    template_name = '_templates/global/Quiz_Failed_Twice.html'

    @staticmethod
    def is_displayed(player):
        return True if(player.failed_quiz_1_count>1) else False
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.leave_flag = True

class Stage_2(Page):
    @staticmethod
    def live_method(player, data):
        if(data['type'] == 'quiz-submit'):
            dat = json.loads(data["answers"])
            res = ["a3", "a1", "a2", "a3"] == dat
            if(res == False):
                player.failed_quiz_2_count += 1
            
            return({player.id_in_group: {"type": "quiz-result", "response": res, "cnt": player.failed_quiz_2_count}})
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.wait_page_arrival = time.time()
        player.participant.leave_flag = False
        player.participant.timeout_flag = False
        player.participant.personal_account_balance = 0
        player.session.vars['group_player_left'] = False


class Quiz_2_Failed(Page):
    template_name = '_templates/global/Quiz_Failed_Twice.html'

    @staticmethod
    def is_displayed(player):
        return True if(player.failed_quiz_2_count>1) else False
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.leave_flag = True

page_sequence = [ProceedPage, ConsentForm, ID, PreliminaryQuestions, Instructions, Quiz_1_Failed, Stage_2, Quiz_2_Failed]
