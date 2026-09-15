"""Replaceable boundary for detecting requirement features."""

from typing import Protocol

from .domain import Requirement, RequirementFeatures


class FeatureExtractor(Protocol):
    def extract(self, requirement: Requirement) -> RequirementFeatures:
        ...
