from typing import Dict, List, Optional

import random

from storytime import gpt3
from storytime.character import Character
from storytime.gpt3 import generate_text
from storytime.location import Location
from storytime.time_period import TimePeriod

SUFFIXES = {1: "st", 2: "nd", 3: "rd"}


def ordinal(num):
    # I'm checking for 10-20 because those are the digits that
    # don't follow the normal counting scheme.
    if 10 <= num % 100 <= 20:
        suffix = "th"
    else:
        # the second parameter is a default.
        suffix = SUFFIXES.get(num % 10, "th")
    return str(num) + suffix


class Scene:
    """Sequence of interactions between one or more characters and/or
    objects in a location.
    """

    scene_parts = {
        "goal": "a specific and clearly defined goal that the protagonist "
        "wants to achieve is presented.",
        "conflict": "a problem or set of obstacles is presented that the "
        "protagonist faces on the way to reaching their goal.",
        "disaster": "a disaster occurs to the protagonist that "
        "prevents them from achieving their goal.",
    }

    sequel_parts = {
        "reaction": "the protagonist's reaction to the disaster of the "
        "previous scene is shown.",
        "dilemma": "a dilemma that the protagonist faces is illustrated.",
        "decision": "the protagonist's decision to deal with the dilemma is "
        "shown.",
    }

    scene_types = {
        "scene": scene_parts,
        "sequel": sequel_parts,
    }

    # https://www.advancedfictionwriting.com/articles/writing-the-perfect
    # -scene/
    # https://www.helpingwritersbecomeauthors.com/how-to-structure-scenes/
    def __init__(
        self,
        target_audience: str,
        genre: str,
        themes: List[str],
        act_description: str,
        time_period: TimePeriod,
        characters: Dict[str, Character],
        total_scenes_in_act: int,
        previous_scenes: Optional[List["Scene"]] = None,
    ):
        self.previous_scenes = previous_scenes
        self.scene_number = len(previous_scenes) + 1 if previous_scenes else 1
        scene_number_ordinal = ordinal(self.scene_number)
        self.total_scenes_in_act = total_scenes_in_act
        self.scene_type = "scene"
        if previous_scenes and previous_scenes[-1].scene_type == "scene":
            self.scene_type = "sequel"

        # Include the protagonist and a random set of characters in the scene.
        self.characters = {"protagonist": characters["protagonist"]}
        char_in_scene = random.randrange(2, len(characters.keys()))
        for i in range(char_in_scene):
            char = random.choice(list(characters.keys()))
            if char not in self.characters:
                self.characters[char] = characters[char]

        # Randomly change the location from the prior scene
        if previous_scenes is None or len(previous_scenes) == 0:
            self.location = Location(time_period.era)
        else:
            if random.random() > 0.6:
                self.location = Location.new_locale(
                    previous_scenes[-1].location
                )
            elif random.random() > 0.9:
                self.location = Location.new_area(previous_scenes[-1].location)
            else:
                self.location = previous_scenes[-1].location

        # Advance the time of day and randomly change the season and era
        if previous_scenes is None or len(previous_scenes) == 0:
            self.time_period = time_period
        else:
            self.time_period = TimePeriod.advance_time_of_day(
                previous_scenes[-1].time_period
            )
            if random.random() > 0.7:
                self.time_period = TimePeriod.advance_season(self.time_period)
            if random.random() > 0.95:
                self.time_period = TimePeriod.advance_era(self.time_period)

        # Write the scene from scene prompts
        self.scene_text: List[str] = []
        self.scene_setup = (
            f"As part of a {genre} appealing to "
            f"{target_audience} with the themes of "
            f"{themes[0]} and {themes[1]}, in the "
            f"{scene_number_ordinal} scene of a "
            f"{total_scenes_in_act} scene act where "
            f"{act_description}"
        )
        # Add previous scene to scene setup
        if previous_scenes is not None and len(previous_scenes) > 0:
            if (
                previous_scenes[-1].scene_text is not None
                and len(previous_scenes[-1].scene_text) > 0
            ):
                # TODO: Consider adding a summary of the previous scene
                self.scene_setup += (
                    f" The previous scene ended with: "
                    f"{previous_scenes[-1].scene_text[-1]}"
                )
        # Add location and time of day to scene setup
        self.scene_setup += (
            f" This scene takes place in a "
            f"{self.location.locale} "
            f"in a {self.location.area} area during "
            f"{self.time_period.time_of_day} of "
            f"{self.time_period.season} in the"
            f" {self.time_period.era} era."
        )
        # Add characters to scene setup
        for char in list(self.characters.keys()):
            self.scene_setup += f" {self.characters[char]} is the {char}."
        # Add scene types to scene prompt and generate scene text
        for part in self.scene_types[self.scene_type]:
            scene_prompt = self.scene_setup
            scene_prompt += (
                f"Write a part of the scene where"
                f" {self.scene_types[self.scene_type][part]} "
                f"Start with a paragraph that describes what "
                f"the characters experience externally and "
                f"then write one or more paragraphs that "
                f"describes how the characters react to what "
                f"happened beginning with their feelings, "
                f"then any reflexive actions, followed by "
                f"any rational actions and dialogue."
            )
            new_scene_text = generate_text(
                scene_prompt,
                max_tokens=(gpt3.MAX_TOKENS - int(len(scene_prompt) / 4)),
            )
            self.scene_text.append(new_scene_text)

    def __str__(self) -> str:
        full_scene: str = ""
        for text in self.scene_text:
            full_scene += "------" + "\n"  # Scene part separator
            full_scene += str(text) + "\n"
        return full_scene
