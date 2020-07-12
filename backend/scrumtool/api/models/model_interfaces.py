class IGetProject:
    """Interface for access to project
    """
    @property
    def project(self):
        raise NotImplementedError


class IGetBoard:
    """Interface for access to board
    """
    @property
    def board(self):
        raise NotImplementedError
