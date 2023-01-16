# library imports
from impact_factor.core import Factor

# project imports


class JournalImpactFactorFinder:
    """
    A class responsible to find the data related to the impact factor of a journal
    """

    def __init__(self):
        pass

    @staticmethod
    def find(journal_name: str):
        try:
            return Factor().search('nature')
        except Exception as error:
            return KeyError("Could not find IF for {}, because: {}".format(journal_name,
                                                                           error))
