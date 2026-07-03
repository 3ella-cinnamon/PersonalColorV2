"""Core domain types. The Five Elements (Wu Xing) are the 'middle variable'
across BaZi, MBTI, and Mian Xiang per the system architecture spec."""

from enum import Enum


class Element(str, Enum):
    WOOD = "wood"
    FIRE = "fire"
    EARTH = "earth"
    METAL = "metal"
    WATER = "water"


class Strategy(str, Enum):
    ATTACK = "ATTACK"
    OPTIMIZE = "OPTIMIZE"
    RETREAT = "RETREAT"


class Goal(str, Enum):
    WORK = "work"
    MONEY = "money"
    RELATIONSHIP = "relationship"


class InteractionType(str, Enum):
    """The Ten Gods relationship between the daily element and the user's
    Day Master. Drives the E_bazi range per the architecture doc."""
    RESOURCE = "resource"      # daily generates Day Master  → supportive
    WEALTH = "wealth"          # Day Master controls daily   → supportive
    COMPANION = "companion"    # same element                → neutral+
    OUTPUT = "output"          # Day Master generates daily  → neutral
    OFFICER = "officer"        # daily controls Day Master   → clash
