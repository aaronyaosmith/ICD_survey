from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import re

# These pages roughly follow the page divisions as specified in the Qualtrics survey.

class Consent(Page):

    form_model = 'player'
    form_fields = ['consent18', 'consentRead', 'consentWant']

    def error_message(self, values):
        print('values is', values)
        if values["consent18"] != True or values["consentRead"] != True or values["consentWant"] != True:
            return 'Sorry, but you are not eligible for this study.'

# "You will play the role of %role%."
class Intro1(Page):
    pass

# show EXAMPLE image based on role
class Intro2(Page):
    pass

# AdvComm: Communication pages for the advisor
class AdvComm1(Page):
    def is_displayed(self):
        return self.player.is_advisor()

class AdvComm2(Page):
    def is_displayed(self):
        return self.player.is_advisor()

class AdvComm3(Page):
    def is_displayed(self):
        return self.player.is_advisor()

class AdvComm4(Page):
    def is_displayed(self):
        return self.player.is_advisor()

class AdvBegin(Page):
    template_name = 'study/Begin.html'
    def is_displayed(self):
        return self.player.is_advisor()

class AdvComm5(Page):
    def is_displayed(self):
        return self.player.is_advisor()
    
class AdvComm6(Page):
    def is_displayed(self):
        return self.player.is_advisor()

class AdvComm7(Page):
    form_model = 'group'
    form_fields = ['recommendation']

    def is_displayed(self):
        return self.player.is_advisor()

class WaitForRecommendation(WaitPage):
    template_name = 'study/WaitProgress.html'

    def is_displayed(self):
        return self.player.is_advisor() or self.player.is_estimator()
    def vars_for_template(self):
        return {
                   'advisor': self.group.get_player_by_role('advisor').participant,
                   'estimator': self.group.get_player_by_role('estimator').participant,
                   'judge': self.group.get_player_by_role('judge').participant
               }

class EstComm1(Page):
    def is_displayed(self):
        return self.player.is_estimator()

class EstComm2(Page):
    def is_displayed(self):
        return self.player.is_estimator()

class EstBegin(Page):
    template_name = 'study/Begin.html'
    def is_displayed(self):
        return self.player.is_estimator()

class EstComm3(Page):
    def is_displayed(self):
        return self.player.is_estimator()

class EstComm4(Page):
    def is_displayed(self):
        return self.player.is_estimator()

class EstComm5(Page):
    form_model = 'group'
    form_fields = ['estimate']

    def is_displayed(self):
        return self.player.is_estimator()
    def before_next_page(self):
        self.group.calculate_grid_rewards() # this function is only executed once: once the estimator advances.

class EstComm6(Page):
    def is_displayed(self):
        return self.player.is_estimator()

class WaitForEstimate(WaitPage):
    template_name = 'study/WaitProgress.html'

    def vars_for_template(self):
        return {
                   'advisor': self.group.get_player_by_role('advisor').participant,
                   'estimator': self.group.get_player_by_role('estimator').participant,
                   'judge': self.group.get_player_by_role('judge').participant
               }



class RevealGrid(Page):
    def is_displayed(self):
        return self.player.is_estimator()

class GridReward(Page):
    def is_displayed(self):
        return self.player.is_advisor() or self.player.is_estimator()

class EstInfo1(Page):
    def is_displayed(self):
        return self.player.is_estimator()
    def vars_for_template(self):
        return {
            'row2_lower': self.group.correct_answer - 10, 
            'row2_upper': self.group.correct_answer,
            'row3_lower': self.group.correct_answer + 1,
            'row3_upper': self.group.correct_answer + 10,
            'row4_lower': self.group.correct_answer + 11,
            'row4_upper': self.group.correct_answer + 99,
        }


class EstInfo2(Page):
    def is_displayed(self):
        return self.player.is_estimator()
    def vars_for_template(self):
        return {'advisor_reward': self.group.get_player_by_role('advisor').grid_reward}

class EstAppeal1(Page):
    def is_displayed(self):
        return self.player.is_estimator()

class EstAppeal2(Page):
    def is_displayed(self):
        return self.player.is_estimator()

class EstAppeal3(Page):
    form_model = 'group'
    form_fields = ['appealed']

    def is_displayed(self):
        return self.player.is_estimator()

class EstAppeal4(Page):
    def is_displayed(self):
        return self.player.is_estimator()

class JudgeInfo1(Page):
    def is_displayed(self):
        return self.player.is_judge()

class JudgeInfo2(Page):
    def is_displayed(self):
        return self.player.is_judge()

class JudgeInfo3(Page):
    def is_displayed(self):
        return self.player.is_judge()
    def vars_for_template(self):
        return {
            'row2_lower': self.group.correct_answer - 10, 
            'row2_upper': self.group.correct_answer,
            'row3_lower': self.group.correct_answer + 1,
            'row3_upper': self.group.correct_answer + 10,
            'row4_lower': self.group.correct_answer + 11,
            'row4_upper': self.group.correct_answer + 99,
            'advisor_reward': self.group.get_player_by_role('advisor').grid_reward,
            'estimator_reward': self.group.get_player_by_role('estimator').grid_reward
        }

class JudgeInfo4(Page):
    def is_displayed(self):
        return self.player.is_judge()

class JudgeInfo5(Page):
    def is_displayed(self):
        return self.player.is_judge()
    def vars_for_template(self):
        return {
            'advisor_upper_bound': self.group.correct_answer + 100,
            'estimator_lower_bound': self.group.correct_answer - 10,
            'estimator_upper_bound': self.group.correct_answer + 10,
        }

class JudgeInfo6(Page):
    def is_displayed(self):
        return self.player.is_judge()

class JudgeInfo7(Page):
    def is_displayed(self):
        return self.player.is_judge()
    def vars_for_template(self):
        return {
            'row2_lower': self.group.correct_answer - 10, 
            'row2_upper': self.group.correct_answer,
            'row3_lower': self.group.correct_answer + 1,
            'row3_upper': self.group.correct_answer + 10,
            'row4_lower': self.group.correct_answer + 11,
            'row4_upper': self.group.correct_answer + 99,
            'advisor_reward': self.group.get_player_by_role('advisor').grid_reward,
            'estimator_reward': self.group.get_player_by_role('estimator').grid_reward
        }

class Judgment(Page):
    form_model = 'group'
    form_fields = ['appeal_granted']

    def is_displayed(self):
        return self.player.is_judge()

class WaitForJudgment(WaitPage):
    template_name = 'study/WaitProgress.html'

    def vars_for_template(self):
        return {
                   'advisor': self.group.get_player_by_role('advisor').participant,
                   'estimator': self.group.get_player_by_role('estimator').participant,
                   'judge': self.group.get_player_by_role('judge').participant
               }


class AdvPostJudgment(Page):
    def is_displayed(self):
        return self.player.is_advisor()

class Blame(Page):
    template_name = "study/PostQuestions.html"

    form_model = 'group'
    def get_form_fields(self):
        if self.player.is_estimator():
            return ['e1','e2','e3','e4','e5','e6','e7','e8','e9']
        elif self.player.is_judge():
            return ['j1','j2','j3','j4','j5','j6','j7','j8','j9']
        elif self.player.is_advisor():
            return ['a1','a2','a3','a4','a5','a6','a7','a8','a9']

    def vars_for_template(self):
        return {'header': "Now we'd like to ask you to rate your level of agreement with a series of statements."}

class ManipulationChecks(Page):
    template_name = "study/PostQuestions.html"

    form_model = 'player'
    form_fields = ['m1', 'm2', 'm3']

    # Prior to conclusion, calculate total rewards
    def before_next_page(self):
        self.player.assign_rewards()
    def vars_for_template(self):
        return {'header': "Please answer the following three questions about the survey."}



class Conclusion(Page):
    def vars_for_template(self):
        return {
            'appeal_reward_minus_cost': Constants.appeal_reward - Constants.appeal_cost,
            'appeal_reward_split_minus_cost': Constants.appeal_reward_split - Constants.appeal_cost,
            'estimator_grid_reward': self.group.get_player_by_role('estimator').grid_reward,
            'advisor_grid_reward': self.group.get_player_by_role('advisor').grid_reward
        }

class Demographics1(Page):
    pass

class Demographics2(Page):
    form_model = 'player'
    form_fields = ['d1', 'd2', 'd3', 'd4', 'd5']

class Comments(Page):
    form_model = 'player'
    form_fields = ['comment']

class Finish(Page):
    form_model = 'player'
    form_fields = ['email','entered_email']

    def error_message(self, values):
        email_pattern = re.compile(r"(^$|(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$))")
        if (
                (values['entered_email'] is True and values['email'] is None) or 
                (values['entered_email'] is True and not email_pattern.match(values['email']))
           ):
            return "Invalid email address"

page_sequence = [
    Consent,
    Intro1,
    Intro2,
    AdvComm1,
    AdvComm2,
    AdvComm3,
    AdvComm4,
    AdvBegin,
    AdvComm5,
    AdvComm6,
    AdvComm7,
    WaitForRecommendation,
    EstComm1,
    EstComm2,
    EstBegin,
    EstComm3,
    EstComm4,
    EstComm5,
    EstComm6,
    WaitForEstimate,
#    RevealGrid,
    GridReward,
    EstInfo1,
    EstInfo2,
    EstAppeal1,
    EstAppeal2,
    EstAppeal3,
    EstAppeal4,
    JudgeInfo1,
#    JudgeInfo2,
    JudgeInfo3,
    JudgeInfo4,
    JudgeInfo5,
    JudgeInfo6,
    JudgeInfo7,
    Judgment,
    WaitForJudgment,
    AdvPostJudgment,
    Blame,
    ManipulationChecks,
    Conclusion,
    Demographics1,
    Demographics2,
    Comments,
    Finish
]
