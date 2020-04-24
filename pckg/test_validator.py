import unittest

from .validator import Validator, validate

class TestValidator(unittest.TestCase):


    def get_constant_func(self, result):
        def func():
            return result

        return func

    def test_validator(self):
        
        test_data = [
            # statement     <==>        thesis
            ('true',    'equivalent',   'true'),
            ('unknown', 'equivalent',   'unknown'),
            ('false',   'equivalent',   'false'),

            # statement     <==>    !thesis
            ('true',    'opposite', 'false'),
            ('unknown', 'opposite', 'unknown'),
            ('false',   'opposite', 'true'),

            # statement     ==>     thesis
            ('true',    'implying', 'true'),
            ('unknown', 'implying', 'unknown'),
            ('false',   'implying', 'unknown'),

            # statement     <==     thesis
            ('true',    'implied',  'unknown'),
            ('unknown', 'implied',  'unknown'),
            ('false',   'implied',  'false'),

            #    statement      ==>         !thesis
            # or !statement     <==         thesis
            ('true',    'contradictory',    'false'),
            ('unknown', 'contradictory',    'unknown'),
            ('false',   'contradictory',    'unknown'),
        ]

        for info in test_data:
            status = info[0]
            thesis_status = info[2]
            relation_to_thesis = info[1]

            func = self.get_constant_func(status)
            validator = Validator(relation_to_thesis, func)

            self.assertEqual(validator.process_status(status), thesis_status)

            result = validator.status()
            self.assertEqual(result[0], thesis_status)
            self.assertEqual(result[1], "no info")

    def test_validate(self):

        test_data = [
            # statement statuses                                        info
            #                                               thesis status
            (("true", "unknown", "unknown", "unknown"),     "true",     0),
            (("unknown", "true", "unknown", "unknown"),     "true",     1),
            (("unknown", "unknown", "unknown", "true"),     "true",     3),
            (("false", "unknown", "unknown", "unknown"),    "false",    0),
            (("unknown", "unknown", "false", "unknown"),    "false",    2),
            (("unknown", "unknown", "unknown", "false"),    "false",    3),
            (("unknown", "unknown", "unknown", "unknown"),  "unknown",
                                                                "no info"),
        ]

        for info in test_data:

            statuses = info[0]
            thesis_status = info[1]
            expected_info = info[2]

            validators = []
            for i in range(len(statuses)):
                func = self.get_constant_func((statuses[i], i))

                validator = Validator("equivalent", func)
                validators.append(validator)

            status, validation_info = validate(*validators)
            self.assertEqual(status, thesis_status)
            self.assertEqual(validation_info, expected_info)

    def test_info(self):

        def n_is_biggest(*numbers, n):
            for number in numbers:
                if n < number:
                    return 'false', f'n < {number}'

            return 'true'

        for n in range(7):
            validator = Validator("implied", n_is_biggest, *range(8), n=n)
            status, info = validator.status()

            self.assertEqual(status, 'false')
            self.assertEqual(info, f'n < {n + 1}')

