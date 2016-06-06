from django.views.generic import TemplateView


class SubmitView(TemplateView):
    template_name = "submission/submit.html"
