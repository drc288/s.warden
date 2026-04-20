from dataclasses import FrozenInstanceError

import pytest

from src.modules.incidents.domain.value_object import Confidence


class TestConfidenceRange:
    def test_accepts_zero(self):
        assert Confidence(0.0).value == 0.0

    def test_accepts_one(self):
        assert Confidence(1.0).value == 1.0

    def test_accepts_mid_range(self):
        assert Confidence(0.5).value == 0.5

    def test_rejects_below_zero(self):
        with pytest.raises(ValueError, match="Confidence"):
            Confidence(-0.1)

    def test_rejects_above_one(self):
        with pytest.raises(ValueError, match="Confidence"):
            Confidence(1.5)


class TestConfidenceIsHigh:
    def test_exactly_threshold_is_high(self):
        assert Confidence(0.7).is_high is True

    def test_just_below_threshold_is_not_high(self):
        assert Confidence(0.69).is_high is False

    def test_above_threshold_is_high(self):
        assert Confidence(0.71).is_high is True

    def test_low_value_is_not_high(self):
        assert Confidence(0.1).is_high is False

    def test_max_value_is_high(self):
        assert Confidence(1.0).is_high is True


class TestConfidenceImmutability:
    def test_frozen_prevents_mutation(self):
        c = Confidence(0.8)
        with pytest.raises(FrozenInstanceError):
            c.value = 0.9
