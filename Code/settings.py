from os import environ

SESSION_CONFIGS = [
    dict(
        name='public_goods_baseline',
        app_sequence=['Baseline_PreGame', 'Baseline_Game', 'Baseline_PostGame'],
        num_demo_participants=20,
    ),
    dict(
        name='public_goods_reward',
        app_sequence= ['Reward_PreGame', 'Reward_Game', 'Reward_PostGame'],
        num_demo_participants=20,
    ),
    dict(
        name='public_goods_feedback',
        app_sequence= ['Feedback_PreGame', 'Feedback_Game', 'Feedback_PostGame'],
        num_demo_participants=20,
    ),
    dict(
        name='public_goods_punishment',
        app_sequence= ['Punishment_PreGame', 'Punishment_Game','Punishment_PostGame'],
        num_demo_participants=20,
    ),
    dict(
        name='public_goods_both_reward_punishment',
        app_sequence= ['Reward_Punishment_PreGame','Reward_Punishment_Game', 'Reward_Punishment_PostGame'],
        num_demo_participants=20,
    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc="",

    randomize_roles = False,
    baseline_roles = ['human', 'human', 'human'],
    reward_roles = ['human', 'human', 'human'],
    feedback_roles = ['human', 'human', 'human'],
    punishment_roles = ['human', 'human', 'human'],
    reward_punishment_roles = ['human', 'human', 'human'],
)

PARTICIPANT_FIELDS = ['wait_page_arrival', 'leave_flag', 'timeout_flag', 'val_code' ,'p2_role', 'p3_role', 'p4_role', 'personal_account_balance', 'additional_question_MU']
SESSION_FIELDS = ['group_player_left']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5565470748035'

# DEBUG
DEBUG = False
