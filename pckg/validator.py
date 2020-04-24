class Validator():
    """A class that represents a statement related to a thesis that we want
    to prove or disprove."""

    def __init__(self, type_of_relation, func, *args, **kwargs):
        # <func> should be a function that returns a string [status] or a
        # tuple ([status], [info]), where 'status' is one of the strings
        # "true", "false", "unknown" - the epistemological status of the
        # statement that <self> represents, 'info' should be information
        # about what is the reason for 'status' to be what it is
        
        self.type = type_of_relation

        # TODO: copy the function
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def status(self):

        result = self.func(*self.args, **self.kwargs)
        if type(result) == tuple:
            status, info = result
        else:
            status = result
            info = 'no info'

        return self.process_status(status), info

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
        status, info = validator.status()

        if status != 'unknown':
            return status, info

    return 'unknown', "no info"