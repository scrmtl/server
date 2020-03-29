"""Controller methods in the app (MVC model)
"""
from django.views.generic.base import TemplateView

from scrumtoolHome import models


class HomePageView(TemplateView):
    """Has all Homepage functionality

    Parameters
    ----------
    TemplateView : TemplateView
        [description]

    """
    template_name = "scrumtool/index.html"

    def get_context_data(self, **kwargs):
        """Shows index.html website

        Parameters
        ----------
        request : HttpRequest
            The request object used to generate this response.

        Returns
        -------
        HttpResponse
            Answer element according to the request
        """
        context = super().get_context_data(**kwargs)
        context['backlog'] = models.ProductBacklog.objects.all()
        context['sb'] = models.SprintBacklog.objects.all()
        context['tasks'] = models.TaskCard.objects.all()

        return context
