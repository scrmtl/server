import sys

import rules
import logging

from api.models.model_interfaces import IGetProject
from api import models

stdlogger = logging.getLogger(__name__)


def getProjectUser(user, project_object):
    if not isinstance(project_object, IGetProject):
        raise TypeError(f"project_object is not of " +
                        f"type Project but of type {type(project_object)}")
    project_users = project_object.project.project_users
    project = project_object.project
    stdlogger.info(
        f"Is user {user} member in project: {project_object.project}")
    project_user = models.ProjectUser.objects.filter(
        project=project,
        plattform_user=user)

    if project_user.exists():
        stdlogger.info(f"--> Yes")
        return project_user.first()
    else:
        stdlogger.info(f"--> No")
        return None


@rules.predicate
def is_po_in_project(user, project_object):
    project_user = getProjectUser(user, project_object)
    if project_user is None:
        return False
    else:
        return project_user.role.is_po


@rules.predicate
def is_sm_in_project(user, project_object):
    project_user = getProjectUser(user, project_object)
    if project_user is None:
        return False
    else:
        return project_user.role.is_sm


@rules.predicate
def is_dev_in_project(user, project_object):
    project_user = getProjectUser(user, project_object)
    if project_user is None:
        return False
    else:
        return project_user.role.is_dev


@rules.predicate
def is_project_team_member(user, project_object):
    project_user = getProjectUser(user, project_object)
    if project_user is None:
        return False
    else:
        return True


@rules.predicate
def is_own_profile(user, platform_user_object):
    if platform_user_object is None:
        return False
    if user.id == platform_user_object.id:
        return True
    else:
        return False


@rules.predicate
def is_own_vote(user, vote_object):
    if vote_object is None:
        return False
    if user.id == vote_object.user.id:
        return True
    else:
        return False


is_admin = rules.is_group_member('admin')
is_default_user = rules.is_group_member('standard')

can_change_user = is_admin | is_own_profile
