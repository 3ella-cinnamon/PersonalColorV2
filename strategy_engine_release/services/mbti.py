"""MBTI → dominant cognitive function → Element.

The mapping follows the Ontological Mapping section of the architecture spec:
  Ne / Se        → Wood
  Fe             → Fire
  Si             → Earth
  Ti / Te        → Metal
  Ni / Fi        → Water
"""

from models.domain import Element


COGNITIVE_FUNCTION_ELEMENT: dict[str, Element] = {
    "Ne": Element.WOOD,
    "Se": Element.WOOD,
    "Fe": Element.FIRE,
    "Si": Element.EARTH,
    "Ti": Element.METAL,
    "Te": Element.METAL,
    "Ni": Element.WATER,
    "Fi": Element.WATER,
}

DOMINANT_FUNCTION: dict[str, str] = {
    "INTJ": "Ni", "INTP": "Ti", "ENTJ": "Te", "ENTP": "Ne",
    "INFJ": "Ni", "INFP": "Fi", "ENFJ": "Fe", "ENFP": "Ne",
    "ISTJ": "Si", "ISFJ": "Si", "ESTJ": "Te", "ESFJ": "Fe",
    "ISTP": "Ti", "ISFP": "Fi", "ESTP": "Se", "ESFP": "Se",
}


def get_dominant_function(mbti: str) -> str:
    if mbti not in DOMINANT_FUNCTION:
        raise ValueError(f"Unknown MBTI type: {mbti}")
    return DOMINANT_FUNCTION[mbti]


def mbti_to_element(mbti: str) -> Element:
    return COGNITIVE_FUNCTION_ELEMENT[get_dominant_function(mbti)]
