"""Controller methods in the app (MVC model)
"""
from django.views.generic.base import TemplateView

from scrumtoolHome import models


class ProductBacklog(TemplateView):
    """Website that display the product backlog

    Parameters
    ----------
    TemplateView : TemplateView
        Renders a given template, with the context
        containing parameters captured in the URL

    """
    template_name = "scrumtool/pb.html"

    def get_context_data(self, **kwargs):
        """Shows the selected product backlog

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

        return context


class SprintBacklog(TemplateView):
    """Website that display the sprint backlog

    Parameters
    ----------
    TemplateView : TemplateView
        Renders a given template, with the context
        containing parameters captured in the URL

    """
    template_name = "scrumtool/sb.html"

    def get_context_data(self, **kwargs):
        """"Shows the selected sprint backlog

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
