"""Controller methods in the app (MVC model)
"""
from django.views.generic.base import TemplateView


class Login(TemplateView):
    """Website that display the sprint backlog

    Parameters
    ----------
    TemplateView : TemplateView
        Renders a given template, with the context
        containing parameters captured in the URL

    """
    template_name = "scrumtool/login.html"

    def get_context_data(self, **kwargs):
        """Shows login.html website

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
        return context
