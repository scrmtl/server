import rules
import logging
import sys
stdlogger = logging.getLogger(__name__)


@rules.predicate
def is_po(user, project_object):
    try:
        project_users = project_object.project.project_users
    except ValueError:
        stdlogger.error(
            'rule is_po expected project but got type %s ',
            type(project_object))
    for project_user in project_users.all():
        if project_user.scrum_user.id == user.id:
            stdlogger.info(
                'User is member of the project %s ',
                project_object.project)
            return project_user.role.is_po
    # if user is not found in project
    return False


@rules.predicate
def is_project_team_member(user, project_object):
    try:
        project_users = project_object.project.project_users
    except ValueError:
        stdlogger.error(
            'rule is_po expected project but got type %s ',
            type(project_object))
    for project_user in project_users.all():
        if project_user.scrum_user.id == user.id:
            stdlogger.info(
                'User is member of the project %s ',
                project_object.project)
            return True
    # if user is not found in project
    return False
