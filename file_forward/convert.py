import datetime

class AbbreviatedDate:
    """
    Convert abbreviated date string.
    """

    def __init__(self, assumed_year=None):
        if assumed_year is None:
            assumed_year = datetime.date.today().year
        self._assumed_year = assumed_year

    def get_assumed_year(self):
        if self._assumed_year is None:
            return datetime.date.today().year
        return self._assumed_year

    @property
    def assumed_year(self):
        return self.get_assumed_year()

    def __call__(self, year_string, month_string, day_string):
        """
        Abbreviated date parts strings.
        """
        


def month_from_abbr(string, format='%b'):
    return datetime.datetime.strptime(string, format).month

