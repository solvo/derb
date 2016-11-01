'''
Created on 14/9/2016
@author: natalia
'''
import json
from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp, QuestionViewPDF
from report_builder.Question.forms import IntegerQuestionForm, AnswerForm, IntegerAnswerForm
from report_builder.shortcuts import get_children


class IntegerQuestionViewAdmin(QuestionViewAdmin):
    form_class = IntegerQuestionForm
    template_name = 'admin/question_types/integer_question.html'
    name = 'integer_question'
    minimal_representation = {
        'human_readable_name': 'Numerical question',
        'help': 'Allows you to make numerical questions',
        'color': '#e86252'
    }
    evaluator = int

    def pre_save(self, object, request, form):
        children = get_children(form)

        form_data = dict(form.data)

        answer_options = {
            "maximum": self.evaluator(form_data.get('maximum')[0]),
            "minimum": self.evaluator(form_data.get('minimum')[0]),
            "steps": self.evaluator(form_data.get('steps')[0]),
            'children': children
        }
        object.answer_options = json.dumps(answer_options)
        return object

    def additional_template_parameters(self, **kwargs):
        parameters = self.get_question_answer_options()
        if not parameters:
            parameters = {}
        parameters['children'] = self.process_children(self.request, parameters, kwargs)
        return parameters

    def get_form(self, post=None, instance=None, extra=None):
        extra = self.get_question_answer_options()
        return super(IntegerQuestionViewAdmin, self).get_form(post=post, instance=instance, extra=extra)


class IntegerQuestionViewResp(QuestionViewResp):
    template_name = 'responsable/integer_question.html'
    name = 'integer_question'
    form_class = IntegerAnswerForm

    def get_form(self, post=None, instance=None, extra=None):
        answer_options_json = self.question.answer_options
        answer_options = json.loads(answer_options_json)
        if post is not None:
            form = self.form_class(post, instance=instance, extra=answer_options)
        else:
            form = self.form_class(instance=instance, extra=answer_options)
        return form


class IntegerQuestionViewPDF(QuestionViewPDF):
    name = 'integer_question'
    template_name = 'pdf/integer_question.html'
