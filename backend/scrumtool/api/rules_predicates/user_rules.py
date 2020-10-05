import sys

import rules
import logging
import api.models.users as users
from api.models.model_interfaces import IGetProject

stdlogger = logging.getLogger(__name__)


def getProjectUser(PlatformUser):
    if not isinstance(PlatformUser, users.PlatformUser):
        raise TypeError("PlatformUser is not of \
            type PlatformUser but of \
                type {0}".format(
            type(PlatformUser)))
    return PlatformUser


@rules.predicate
def is_current_user(user, PlatformUser):
    plattform_user = getProjectUser(PlatformUser)
    if plattform_user == user:
        return True
    else:
        return False
