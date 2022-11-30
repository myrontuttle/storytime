from typing import List, Optional

import random

import requests
from bs4 import BeautifulSoup

STORYGEN_URL = "https://storygen.page/character/"
REEDSY_BASE_URL = "https://blog.reedsy.com/character-name-generator/"
CHARACTER_GEN_URL = "https://www.character-generator.org.uk/"
JOB_BASE_URL = "https://www.onetonline.org/explore/interests/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/68.0.3440.84 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,"
    "application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
}


def random_occupation(job_interests: List[str]) -> str:
    """Set the occupation of the character."""
    url = (
        f"{JOB_BASE_URL}{job_interests[0]}/{job_interests[1]}/"
        f"{job_interests[2]}/"
    )
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    jobs = soup.findAll("td", {"data-title": "Occupation"})
    return str(random.choice(jobs).find("a").text.strip("s"))


def random_fullname(ethnicity: str, gender: str, tp_param: str) -> str:
    """Generate a random full name for the character."""
    url = (
        f"{REEDSY_BASE_URL}{tp_param}/{ethnicity}/?filter="
        f"{gender}&commit=Generate%20names"
    )
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    nc = soup.find("div", {"id": "names-container"})
    # Name
    if nc is None:
        print(f"Error with URL: {url}")
        if gender == "Male":
            fullname = "John Doe"
        else:
            fullname = "Jane Doe"
    else:
        fullname = nc.find("h3").text
    return fullname


class Character:
    """A character in a story.
    https://blog.reedsy.com/character-profile/"""

    ethnicities = [
        "english",
        "french",
        "german",
        "russian",
        "spanish",
        "italian",
        "japanese",
        "mandarin-chinese",
        "korean",
        "arabic",
        "hindi",
        "turkish",
        "swahili",
    ]

    genders = [
        "Male",
        "Female",
    ]

    heights = [
        "very short",
        "short",
        "average height",
        "tall",
        "very tall",
    ]

    weights = [
        "very thin",
        "thin",
        "average weight",
        "fat",
        "very fat",
    ]

    face_types = [
        "round",
        "oval",
        "square",
        "rectangular",
        "diamond",
        "heart",
        "triangle",
        "pear",
    ]

    educations = [
        "None",
        "Elementary School",
        "Middle School",
        "High School",
        "College",
        "Graduate School",
        "PhD",
    ]

    personality_factors = [
        "agreeable",
        "conscientious",
        "extraverted",
        "neurotic",
        "open",
    ]

    value_list = [
        "acceptance",
        "adaptability",
        "authenticity",
        "authority",
        "autonomy",
        "awareness",
        "balance",
        "beauty",
        "boldness",
        "calmness",
        "citizenship",
        "community",
        "compassion",
        "competency",
        "contribution",
        "creativity",
        "curiosity",
        "determination",
        "discipline",
        "empathy",
        "fairness",
        "faith",
        "family",
        "fame",
        "freedom",
        "friends",
        "fun",
        "gratitude",
        "growth",
        "happiness",
        "health",
        "honesty",
        "humility",
        "humor",
        "influence",
        "innovation",
        "integrity",
        "justice",
        "kindness",
        "knowledge",
        "leadership",
        "learning",
        "love",
        "loyalty",
        "moderation",
        "openness",
        "optimism",
        "patience",
        "peace",
        "pleasure",
        "popularity",
        "purpose",
        "recognition",
        "religion",
        "reputation",
        "respect",
        "responsibility",
        "security",
        "self-respect",
        "service",
        "spirituality",
        "stability",
        "status",
        "success",
        "trust",
        "trustworthiness",
        "understanding",
        "wealth",
        "wisdom",
    ]

    interest_areas = [
        "Realistic",
        "Investigative",
        "Artistic",
        "Social",
        "Enterprising",
        "Conventional",
    ]

    generic_jobs = [
        "Accountant",
        "Actor",
        "Athlete",
        "Artist",
        "Doctor",
        "Engineer",
        "Lawyer",
        "Office Worker",
        "Factory Worker",
        "Musician",
        "Politician",
        "Retail Worker",
        "Salesperson",
        "Teacher",
        "Sailor",
        "Scientist",
        "Soldier",
        "Unemployed",
        "Writer",
    ]

    def __init__(
        self,
        era: Optional[str] = None,
        ethnicity: Optional[str] = None,
        gender: Optional[str] = None,
        fullname: Optional[str] = None,
        age: Optional[int] = None,
    ) -> None:
        self.era = era
        # Select a random ethnicity if none is provided
        if ethnicity is None:
            self.ethnicity = random.choice(self.ethnicities)
        else:
            self.ethnicity = ethnicity
        # Set era-specific values
        if self.era == "Prehistoric":
            self.ethnicity = "old-norse"
            tp_param = "medieval"
            max_age = 30
        elif self.era == "Ancient":
            self.ethnicity = "old-roman"
            tp_param = "medieval"
            max_age = 35
        elif self.era == "Medieval":
            self.ethnicity = "old-english"
            tp_param = "medieval"
            max_age = 40
        elif self.era == "Renaissance":
            tp_param = "language"
            max_age = 55
        elif self.era == "Colonial":
            tp_param = "language"
            max_age = 70
        elif self.era == "Modern":
            tp_param = "language"
            max_age = 85
        elif self.era == "Contemporary":
            tp_param = "language"
            max_age = 100
        elif self.era == "Future":
            tp_param = "language"
            max_age = 110
        else:
            self.era = "Contemporary"
            tp_param = "language"
            max_age = 100
        # Set a random gender and pronoun if none provided
        if gender is None:
            self.gender = random.choice(self.genders)
        else:
            self.gender = gender
        self.pronoun = "He" if self.gender == "Male" else "She"
        # Set a random name if none is provided
        if fullname is None:
            self.fullname = random_fullname(
                self.ethnicity, self.gender, tp_param
            )
        else:
            self.fullname = fullname
        if (
            self.ethnicity == "chinese"
            or self.ethnicity == "japanese"
            or self.ethnicity == "korean"
        ):
            self.firstname = self.fullname.split(" ")[-1]
            self.lastname = self.fullname.split(" ")[0]
        elif self.ethnicity == "old-norse":
            self.firstname = self.fullname.split(" ")[0]
            self.lastname = ""
        else:
            self.firstname = self.fullname.split(" ")[0]
            self.lastname = self.fullname.split(" ")[1]
        self.name = self.firstname
        # Set a random age if none provided
        if age is None:
            self.age = random.randint(5, max_age)
        else:
            self.age = age

        # Height
        self.height = random.choice(self.heights)
        # Weight
        self.weight = random.choice(self.weights)
        # Face type
        self.face_type = random.choice(self.face_types)
        # Appearance
        if (
            self.ethnicity == "chinese"
            or self.ethnicity == "japanese"
            or self.ethnicity == "korean"
        ):
            self.hair_color = random.choice(["black", "brown"])
            self.eye_color = random.choice(["black", "brown"])
            self.skin_tone = random.choice(["olive", "light brown", "beige"])
        elif (
            self.ethnicity == "english"
            or self.ethnicity == "german"
            or self.ethnicity == "french"
            or self.ethnicity == "russian"
            or self.ethnicity == "old-english"
            or self.ethnicity == "old-norse"
        ):
            if self.age > 60:
                self.hair_color = random.choice(["white", "grey"])
            else:
                self.hair_color = random.choice(["brown", "blonde", "red"])
            self.eye_color = random.choice(
                ["brown", "blue", "green", "grey", "hazel"]
            )
            self.skin_tone = random.choice(
                ["ivory", "porcelain", "alabaster", "beige", "light"]
            )
        elif (
            self.ethnicity == "spanish"
            or self.ethnicity == "italian"
            or self.ethnicity == "old-roman"
        ):
            if self.age > 60:
                self.hair_color = random.choice(["white", "grey"])
            else:
                self.hair_color = random.choice(["brown", "black"])
            self.eye_color = random.choice(
                ["brown", "blue", "green", "grey", "hazel"]
            )
            self.skin_tone = random.choice(
                ["sienna", "honey", "tan", "olive", "almond", "bronze"]
            )
        elif (
            self.ethnicity == "arabic"
            or self.ethnicity == "hindi"
            or self.ethnicity == "turkish"
        ):
            if self.age > 60:
                self.hair_color = random.choice(["white", "grey"])
            else:
                self.hair_color = random.choice(["black", "brown"])
            self.eye_color = random.choice(["black", "brown"])
            self.skin_tone = random.choice(
                ["olive", "chestnut", "praline", "honey", "caramel", "almond"]
            )
        elif self.ethnicity == "swahili":
            if self.age > 60:
                self.hair_color = random.choice(["white", "grey"])
            else:
                self.hair_color = random.choice(["black", "brown"])
            self.eye_color = random.choice(["black", "brown"])
            self.skin_tone = random.choice(
                ["black", "cacao", "sable", "espresso", "ebony", "mahogany"]
            )
        # Psychology
        # Personality
        self.personality = {}
        for factor in self.personality_factors:
            self.personality[factor] = random.choice(
                ["not very", "a little", "moderately", "often", "very"]
            )
        # Values
        self.values = random.sample(self.value_list, 3)

        # Interests
        self.job_interests = random.sample(self.interest_areas, 3)

        # Background
        # Social Class
        self.social_class = random.choice(["lower", "middle", "upper"])
        # Education and Occupation
        if self.era == "Prehistoric":
            self.education = "minimal"
            self.occupation = random.choice(["Hunter", "Gatherer"])
        elif self.era == "Ancient":
            self.education = "minimal"
            self.occupation = random.choice(
                ["Farmer", "Carpenter", "Smith", "Merchant"]
            )
        elif self.era == "Medieval":
            self.education = random.choice(
                ["minimal", "basic", "intermediate"]
            )
            self.occupation = random.choice(
                ["Farmer", "Carpenter", "Smith", "Merchant", "Knight", "Noble"]
            )
        elif self.era == "Renaissance":
            self.education = random.choice(
                ["minimal", "basic", "intermediate", "advanced"]
            )
            self.occupation = random.choice(
                [
                    "Farmer",
                    "Carpenter",
                    "Artist",
                    "Merchant",
                    "Doctor",
                    "Lawyer",
                    "Engineer",
                ]
            )
        else:
            if self.age <= 10:
                self.education = "Elementary School"
                self.occupation = "Student"
            elif self.age <= 15:
                self.education = "Middle School"
                self.occupation = "Student"
            elif self.age <= 18:
                self.education = "High School"
                self.occupation = "Student"
            elif self.age <= 22:
                self.education = random.choice(["College", "High School"])
                self.occupation = random.choice(
                    ["Student"] + self.generic_jobs
                )
            else:
                self.education = random.choice(
                    ["College", "High School", "Trade School", "Grad School"]
                )
                if self.era == "Contemporary":
                    self.occupation = random_occupation(self.job_interests)
                else:
                    self.occupation = random.choice(self.generic_jobs)
            if self.age > 65:
                self.occupation = f"Retired {self.occupation}"

    def __str__(self) -> str:
        """Return a string representation of the character."""
        desc: str = f"{self.name}, a {self.age} year old "
        if self.age < 18:
            desc += "boy " if self.gender == "Male" else "girl "
        else:
            desc += "man " if self.gender == "Male" else "woman "
        desc += f"of {self.ethnicity} descent that values "
        desc += f"{self.values[0]}, {self.values[1]}, and {self.values[2]}"
        return desc

    def appearance(self) -> str:
        appearance = (
            f"{self.name} is {self.age} years old of "
            f"{self.ethnicity} descent with "
            f"{self.skin_tone} skin, {self.hair_color} hair, and "
            f"{self.eye_color} eyes. "
        )
        if self.weight == "very fat" or self.weight == "fat":
            if self.age < 18:
                appearance += (
                    f"{self.pronoun} is {self.height} and a bit " f"chubby."
                )
            elif self.gender == "Female":
                appearance += f"{self.pronoun} is {self.height} and plump."
            elif self.height == "very short":
                appearance += f"{self.pronoun} is tubby."
            elif self.height == "short":
                appearance += f"{self.pronoun} is stocky."
        elif self.weight == "thin" or self.weight == "very thin":
            if self.gender == "Male":
                if self.height == "tall" or self.height == "very tall":
                    appearance += f"{self.pronoun} is lanky."
                else:
                    appearance += f"{self.pronoun} is {self.height} and lean."
            elif self.gender == "Female":
                if self.height == "tall" or self.height == "very tall":
                    appearance += (
                        f"{self.pronoun} is {self.height} and " f"willowy."
                    )
                else:
                    appearance += (
                        f"{self.pronoun} is {self.height} and " f"slender."
                    )
        else:
            appearance += f"{self.pronoun} is {self.height} and {self.weight}."
        return appearance

    def background(self) -> str:
        background = (
            f"{self.name} was born in the {self.era} era and is "
            f"{self.social_class} class. "
        )
        if (
            self.era == "Prehistoric"
            or self.era == "Ancient"
            or self.era == "Medieval"
            or self.era == "Renaissance"
        ):
            if self.age <= 10:
                background += (
                    f"{self.pronoun} is training to be a"
                    f" {self.occupation}."
                )
            else:
                background += f"{self.pronoun} is a {self.occupation}."
        else:
            background += (
                f"{self.pronoun} has a {self.education} education "
                f"and is a {self.occupation}."
            )
        return background

    def psychology(self) -> str:
        psychology = (
            f"{self.name} is {self.personality['open']} "
            f"open-minded, {self.personality['conscientious']} "
            f"conscientious, {self.personality['extraverted']} "
            f"outgoing, {self.personality['agreeable']} "
            f"agreeable, and {self.personality['neurotic']} "
            f"neurotic. "
        )
        psychology += (
            f"{self.pronoun} values {self.values[0]}, "
            f"{self.values[1]}, and {self.values[2]}. "
        )
        psychology += (
            f"{self.pronoun} is interested in work that is "
            f"{self.job_interests[0]}, "
            f"{self.job_interests[1]}, and {self.job_interests[2]}."
        )
        return psychology


if __name__ == "__main__":
    c = Character("contemporary")
    print(c)
    print(c.appearance())
    print(c.background())
    print(c.psychology())
