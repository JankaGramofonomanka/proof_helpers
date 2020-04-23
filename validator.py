class Validator():
    """A class that represents a statement related to a thesis that we want
    to prove or disprove."""

    def __init__(self, type_of_relation, func, *args, **kwargs):
        
        self.type = type_of_relation
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def status(self):
        return self.process_status(self.func(*self.args, **self.kwargs))

    def process_status(self, status):

        if self.type == 'implied':
            # statement ==> thesis
            if status == 'false':
                return status

            return 'unknown'

        elif self.type == 'implying':
            # thesis ==> statement
            if status == 'true':
                return 'true'

            return 'unknown'

        elif self.type == 'equivalent':
            # thesis <==> statement
            return status

        elif self.type == 'opposite':
            # thesis <==> !statement
            if status == 'true':
                return 'false'
            elif status == 'false':
                return 'true'

            return 'unknown'

        elif self.type == 'contradictory':
            #    statement ==> !thesis
            # or !statement <== thesis
            if status == 'true':
                return 'false'

            return 'unknown'

        else:
            raise ValueError(
                f'invalid type of relation to the thesis: {self.type}')

    def __getitem__(self, key):
        if type(key) == int:
            return self.args[key]
        elif type(key) == str:
            return self.kwargs[key]
        else:
            raise TypeError(f'invalid key type: {key}')

    def __setitem__(self, key, value):
        if type(key) == int:
            self.args[key] = value
        elif type(key) == str:
            self.kwargs[key] = value
        else:
            raise TypeError(f'invalid key type: {key}')


def validate(*validators):
    """Returns the epistemological status of the thesis based on the statuses
    of the statements related to the thesis"""

    for validator in validators:
        status = validator.status()

        if status != 'unknown':
            return status

    return 'unknown'