from otree.api import *
import json, time

doc = """
Public Goods Game Baseline Pre-Experiment Part
"""


class C(BaseConstants):
    NAME_IN_URL = 'Baseline'
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
    failed_quiz_count = models.IntegerField(initial= 0)


# PAGES
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
    template_name = '_templates/global/Instructions.html'

    @staticmethod
    def live_method(player, data):
        if(data['type'] == 'quiz-submit'):
            dat = json.loads(data["answers"])
            res = ["a2", "a1", "a1", "a2"] == dat
            if(res == False):
                player.failed_quiz_count += 1
            
            return({player.id_in_group: {"type": "quiz-result", "response": res, "cnt": player.failed_quiz_count}})
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.wait_page_arrival = time.time()
        player.participant.leave_flag = False
        player.participant.timeout_flag = False
        player.participant.personal_account_balance = 0
        player.participant.additional_question_MU = 0
        player.session.vars['group_player_left'] = False

class QuizFailed(Page):
    template_name = '_templates/global/Quiz_Failed_Twice.html'

    @staticmethod
    def is_displayed(player):
        return True if(player.failed_quiz_count>1) else False
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.leave_flag = True

page_sequence = [ConsentForm, ID, PreliminaryQuestions, Instructions, QuizFailed]
