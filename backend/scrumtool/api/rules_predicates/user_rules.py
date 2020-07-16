import sys

import rules
import logging
import api.models.users as users
from api.models.model_interfaces import IGetProject

stdlogger = logging.getLogger(__name__)


def getProjectUser(ScrumUser):
    if not isinstance(ScrumUser, users.ScrumUser):
        raise TypeError("ScrumUser is not of \
            type ScrumUser but of \
                type {0}".format(
            type(ScrumUser)))
    return ScrumUser


@rules.predicate
def is_current_user(user, ScrumUser):
    scrum_user = getProjectUser(ScrumUser)
    if scrum_user == user:
        return True
    else:
        return False
