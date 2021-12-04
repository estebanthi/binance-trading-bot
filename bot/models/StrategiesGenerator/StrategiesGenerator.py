import operator
import random
from models.StrategiesGenerator.indicators_classification.index import indicators, Flags, price_indicators
from enum import Enum


class LogicOperators(Enum):
    AND = 1
    OR = 2


class Comparators(Enum):
    GE = 1  # >=
    LE = 2  # <=


class EqualityOperators(Enum):
    EQ = 1  # ==
    NE = 2  # !=


class StrategiesGenerator:

    def generate_condition(self):
        indicator1 = random.choice(indicators)
        self.indicator2_tmp = None
        value = None

        if Flags.PRICE_COMPARABLE in indicator1.flags:
            self.indicator2_tmp = self.flip(lambda: random.choice(price_indicators))

        if Flags.SELF_COMPARABLE in indicator1.flags:
            self.indicator2_tmp = self.flip(lambda: indicator1)

        if Flags.UNIQUE_VALUES in indicator1.flags:
            value = random.choice(indicator1.values)
            equality_operator = random.choice(list(EqualityOperators))
            return [indicator1, value, equality_operator]

        comparator = random.choice(list(Comparators))

        return [indicator1, self.indicator2_tmp, comparator]

    def flip(self, fnc, **args):
        if random.randint(0, 1):
            return fnc(**args)
        if not self.indicator2_tmp:
            return fnc(**args)
        return self.indicator2_tmp
