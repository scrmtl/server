import sys

import rules
import logging

from api.models.model_interfaces import IGetProject

stdlogger = logging.getLogger(__name__)


def getProjectUser(user, project_object):
    if not isinstance(project_object, IGetProject):
        raise TypeError("project_object is not of \
            type Project but of \
                type {0}".format(
            type(project_object)))
    for project_user in project_object.project.project_users.all():
        if project_user.scrum_user.id == user.id:
            stdlogger.info(
                'User is member of the project %s ',
                project_object.project)
            return project_user
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


is_admin = rules.is_group_member('Admin')
is_default_user = rules.is_group_member('DefaultUsers')
