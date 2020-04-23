import unittest

from .validator import Validator, validate

class TestValidator(unittest.TestCase):

    def setUp(self):
        def true():
            return "true"

        def unknown():
            return "unknown"

        def false():
            return "false"

        self.functions = {"true": true, "unknown": unknown, "false": false}

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
            validator = Validator(relation_to_thesis, self.functions[status])

            self.assertEqual(validator.process_status(status), thesis_status)
            self.assertEqual(validator.status(), thesis_status)

    def test_validate(self):

        test_data = [
            # statement statuses
            (("true", "unknown", "unknown", "unknown"),     "true"),
            (("unknown", "true", "unknown", "unknown"),     "true"),
            (("unknown", "unknown", "unknown", "true"),     "true"),
            (("false", "unknown", "unknown", "unknown"),    "false"),
            (("unknown", "unknown", "false", "unknown"),    "false"),
            (("unknown", "unknown", "unknown", "false"),    "false"),
            (("unknown", "unknown", "unknown", "unknown"),  "unknown"),
        ]

        for info in test_data:

            statuses = info[0]
            thesis_status = info[1]

            validators = []
            for status in statuses:

                validator = Validator("equivalent", self.functions[status])
                validators.append(validator)

            result = validate(*validators)
            self.assertEqual(result, thesis_status)