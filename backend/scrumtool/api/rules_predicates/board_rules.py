import rules
import logging

from api.models.model_interfaces import IGetBoard

from api.rules_predicates.project_rules import is_po_in_project, \
    is_dev_in_project, is_admin

stdlogger = logging.getLogger(__name__)


def getBoardType(user, board_object):
    if not isinstance(board_object, IGetBoard):
        raise TypeError("board_object is not of \
            type Board but of \
                type {0}".format(
            type(board_object)))

    stdlogger.info('Board type is %s ', board_object.board_type)
    return board_object.board_type


@rules.predicate
def is_pb_board(user, board_object):
    board_type = getBoardType(user, board_object)
    if board_type == 'PB':
        return True
    else:
        return False


@rules.predicate
def is_sp_board(user, board_object):
    board_type = getBoardType(user, board_object)
    if board_type == 'SP':
        return True
    else:
        return False


@rules.predicate
def is_ab_board(user, board_object):
    board_type = getBoardType(user, board_object)
    if board_type == 'AB':
        return True
    else:
        return False


can_change_pb_board = is_pb_board & is_po_in_project
can_change_sp_board = is_sp_board & (is_po_in_project | is_dev_in_project)
can_change_ab_board = is_ab_board & is_admin

can_change_board = can_change_ab_board | \
    can_change_pb_board | \
    can_change_sp_board
