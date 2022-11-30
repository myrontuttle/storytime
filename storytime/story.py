from typing import Dict, List, Optional

import logging
import os.path
import random

import jsonpickle

from storytime.character import Character
from storytime.gpt3 import generate_text
from storytime.image_set import ImageSet
from storytime.scene import Scene
from storytime.time_period import TimePeriod

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


def load_from_json(filename: str) -> "Story":
    """Load a story from a JSON file."""
    with open(filename) as read_file:
        new_story = jsonpickle.decode(read_file.read())
    return new_story


def get_save_path():
    dir_path = os.getcwd()
    dir_name = os.path.basename(dir_path)
    parent_path = os.path.dirname(dir_path)
    par_dir = os.path.basename(parent_path)
    if dir_name == "storytime":
        if par_dir == "storytime":
            # Save the story in the parent directory
            save_path = os.path.join(parent_path, "stories", "")
        else:
            # Save the story in the current directory
            save_path = os.path.join(dir_path, "stories", "")
    elif dir_name == "unit":
        grandparent_path = os.path.dirname(parent_path)
        save_path = os.path.join(grandparent_path, "stories", "")
    else:
        save_path = os.path.join(dir_path, "stories", "")
    return save_path


class Story:
    """A story is a collection of scenes."""

    # Audiences
    target_audiences = [
        "boys",
        "girls",
        "children",
        "young men",
        "young girls",
        "teenagers",
        "men",
        "women",
        "families",
    ]

    # Genres
    # https://storygrid.com/genres-of-writing/
    genres = [
        "action",
        "adventure",
        "comedy",
        "crime",
        "drama",
        "fantasy",
        "historical",
        "horror",
        "mystery",
        "paranormal",
        "romance",
        "science fiction",
        "thriller",
        "western",
    ]

    # Thematic concepts
    # https://michaelbjorkwrites.com/2019/09/26/story-themes-list-ideas-for
    # -your-novel/
    thematic_concepts = [
        # experiences
        "aging",
        "childhood",
        "coming of age",
        "disillusionment",
        "friendship",
        "growth",
        "healing",
        "isolation",
        "loss",
        "loss of innocence",
        "overcoming adversity",
        "parenthood",
        "redemption",
        "revenge",
        "self-discovery",
        "survival",
        "tragedy",
        # feelings
        "apathy",
        "compassion",
        "despair",
        "fear",
        "grief",
        "jealousy",
        "joy",
        "loneliness",
        "love",
        "regret",
        # gender & sexuality
        "androgyny",
        "femininity",
        "gender identity",
        "masculinity",
        "sexuality",
        # human perception
        "dreams",
        "identity",
        "memory",
        "perception vs. reality",
        "subjectivity",
        # mental health & neurodiversity
        "autism",
        "bipolarity",
        "depression",
        "obsessive compulsive disorder",
        "suicide",
        # natural forces
        "death",
        "fate",
        "nature",
        "passage of time",
        # politics & economics
        "capitalism",
        "communism",
        "conservation",
        "democracy",
        "fascism",
        "freedom",
        "justice",
        "nationalism",
        "peace",
        "propaganda",
        "radicalism",
        "socialism",
        "war",
        # religion & philosophy
        "atheism",
        "determinism",
        "ethics",
        "faith",
        "free will",
        "good vs. evil",
        "skepticism",
        "metaphysics",
        "nature vs. nurture",
        "pacifism",
        "religion",
        "soul / consciousness",
        # social issues
        "abuse of power",
        "homophobia",
        "immigration",
        "inequality",
        "oppression",
        "poverty",
        "progress & regress",
        "privilege",
        "racism",
        "rights of the oppressed",
        "sexism",
        "transphobia",
        "working class struggles",
        # society & culture
        "conformity",
        "familial obligations",
        "honor",
        "individualism",
        "responsibility",
        "tradition",
        # technology & science
        "artificial intelligence",
        "augmented reality",
        "genetic engineering",
        "human integration with technology",
        "information privacy",
        "weapons of mass destruction",
        # virtues & vices
        "ambition",
        "corruption",
        "courage",
        "forgiveness",
        "mercy",
        "power",
        "pride",
    ]

    # Five act structure plot elements
    five_act_plot_elements = {
        "Exposition": "The characters and setting are introduced as well as "
        "an inciting incident.",
        "Rising Action": "The events set up the climax.",
        "Climax": "The story turns and the fullest energy of the protagonist "
        "is portrayed.",
        "Falling Action": "Events following the climax.",
        "Resolution": "The story ends and the conflict is resolved.",
    }

    # Freytag's Pyramid plot elements
    freytag_plot_elements = {
        "Introduction": "The status quo is established; an inciting incident "
        "occurs.",
        "Rising Action": "The protagonist actively pursues their goal. The "
        "stakes heighten.",
        "Climax": "There is a point of no return, from which the "
        "protagonist can no longer go back to the status quo.",
        "Fall": "In the aftermath of the climax, tension builds, and the "
        "story heads inevitably towards catastrophe.",
        "Catastrophe": "The protagonist is brought to their lowest point. "
        "Their greatest fears have come true.",
    }

    # The Hero's Journey plot elements
    hero_journey_plot_elements = {
        "The Ordinary World": "The protagonist is introduced. The "
        "reader is given a bit of personal history, "
        "setting, and cultural context. Something in "
        "the hero’s life makes them feel they are "
        "being pulled in different directions and "
        "causing stress.",
        "The Call to Adventure": "Something shakes up the situation, and the "
        "hero feels called to make a change, "
        "which usually involves leaving home.",
        "Refusal of the Call": "The protagonist fears the unknown and "
        "considers turning away from the adventure.  "
        "Or another character tries to dissuade the "
        "hero from proceeding.",
        "Meeting with the Mentor": "The protagonist comes across someone ("
        "often a stranger, elder, or spirit) who "
        "gives them training, equipment, "
        "or advice that will help on the journey.",
        "Crossing the First Threshold": "The protagonist commits to leaving "
        "the World where they started and "
        "enters a new region or condition "
        "with unfamiliar rules and values.",
        "Tests, Allies, and Enemies": "The protagonist is tested and sorts "
        "out allegiances in the Unfamiliar or "
        "Special World.",
        "Approach to the Inmost Cave": "The protagonist and their new-found "
        "allies prepare for the major "
        "challenge in the Special World.",
        "The Ordeal": "The protagonist arrives in a central space in the "
        "Unfamiliar World and faces death or their greatest "
        "fear. The protagonist emerges from this moment of "
        "reckoning changed in some way.",
        "Reward": "The protagonist takes possession of the treasure they "
        "have won in the ordeal. There may be celebration, "
        "but there is also danger of losing the treasure again.",
        "The Road Back": "The protagonist must complete the adventure and "
        "leave the Special World to bring their treasure "
        "back home. They realize that achieving their goal "
        "is not the final hurdle.",
        "Resurrection": "The protagonist is severely tested once more as "
        "they near home in the climax.  The hero is changed "
        "by a last sacrifice, another moment of death and "
        "rebirth which prepares them to be a leader upon "
        "their return.",
        "Return with the Elixir": "The protagonist returns home, bearing the "
        "treasure. The treasure has the power to "
        "transform the world, as the hero has been "
        "transformed. The hero is hailed as a "
        "leader by their kinsmen or community and "
        "so begins a new (and better) life and "
        "world.",
    }

    # Three act structure plot elements
    three_act_plot_elements = {
        "Exposition": "The status quo or 'ordinary world' is established.",
        "Inciting Incident": "An event happens that sets the story in motion.",
        "Plot Point One": "The protagonist decides to tackle the challenge "
        "head-on.",
        "Rising Action": "The protagonist attempts to resolve the "
        "problem initiated by the first turning point, "
        "only to find themselves in ever worsening "
        "situations.",
        "Midpoint": "The protagonist reaches the lowest point of the story. "
        "An event that upends the protagonist’s mission.",
        "Plot Point Two": "The protagonist must not only learn new skills "
        "but arrive at a higher sense of awareness of who "
        "they are and what they are capable of, in order "
        "to deal with their predicament, which in turn "
        "changes who they are.",
        "Pre Climax": "The protagonist must pull themself together and choose "
        "between decisive action and failure.",
        "Climax": "The protagonist must make a choice that will change their "
        "life forever.",
        "Denouement": "All loose ends are tied up, the consequences of the "
        "climax are revealed, and a new status quo is "
        "established.",
    }

    # Dan Harmon Story Circle plot elements
    harmon_plot_elements = {
        "Comfort Zone": "The status quo is established.",
        "The Want": "The protagonist wants something.",
        "Unfamiliar Situation": "The protagonist must do something new in "
        "their pursuit of the thing they want.",
        "Adapt": "Faced with some challenges, the protagonist struggles then "
        "begins to succeed.",
        "Find": "The protagonist gets what they want.",
        "Take": "The protagonist pays a heavy price for what they wanted.",
        "Return": "The protagonist returns to their familiar situation armed "
        "with a new truth.",
        "Change": "The protagonist has changed.",
    }

    # Fichtean Curve plot elements
    fichtean_plot_elements = {
        "Crisis 1": "The protagonist is introduced in the middle of a crisis.",
        "Crisis 2": "Some flaw in the protagonist's character leads them into "
        "another crisis",
        "Crisis 3": "The protagonist is faced with a third crisis, "
        "which forces them to face their character flaw.",
        "Crisis 4": "The protagonist is faced with a fourth crisis.",
        "Climax": "The protagonist must learn from their previous mistakes "
        "to overcome the final crisis or be completely defeated by "
        "it.",
        "Resolution": "The protagonist either learns from their mistakes and "
        "overcomes their flaw or continues with something else "
        "fundamentally changed.",
    }

    # Save the cat story elements
    save_the_cat_plot_elements = {
        "Opening Image": "A visual representation of the story's theme is "
        "described.",
        "Set-up": "The protagonist is introduced and their goal is stated.",
        "Theme Stated": "As part of the setup, the theme is hinted at. "
        "There is a truth that the protagonist will "
        "discover by the end.",
        "Catalyst": "The protagonist is given a reason to act.",
        "Debate": "The protagonist debates whether or not to act.",
        "Break into Two": "The protagonist decides to act.",
        "B Story": "The protagonist's goal is complicated by a secondary "
        "goal. This is a subplot that should highlight the theme.",
        "Fun and Games": "The protagonist tries several times to achieve "
        "their goal based on the genre.",
        "Midpoint": "A plot twist occurs that ups the stakes and makes the "
        "hero’s goal harder to achieve — or makes them focus on "
        "a new, more important goal.",
        "Bad Guys Close In": "The protagonist's goal is threatened.",
        "All is Lost": "The protagonist is defeated as they lose everything "
        "they've gained so far, and things are looking bleak.",
        "Dark Night of the Soul": "Having just lost everything, "
        "the protagonist is at their lowest point "
        "before discovering some 'new information' "
        "that reveals exactly what they need to do "
        "to take another crack at success. (This "
        "new information is often delivered "
        "through the B-Story).",
        "Break into Three": "Armed with this new information, the protagonist "
        "decides to act once more.",
        "Finale": "The protagonist confronts the antagonist or whatever the "
        "source of the primary conflict is. The truth that eluded "
        "them at the start of the story is now clear, allowing them "
        "to resolve their story and achieve their goal.",
        "Final Image": "The final image of the story's theme is visually "
        "represented. It is the final moment or scene that "
        "crystallizes how the character has changed. It’s a "
        "reflection, in some way, of the opening image.",
    }

    # Narrative structures
    # https://www.storyboardthat.com/articles/e/narrative-structures
    # https://blog.reedsy.com/guide/story-structure/
    narrative_structures = {
        "Five-Act": five_act_plot_elements,
        "Freytag's Pyramid": freytag_plot_elements,
        "Hero's Journey": hero_journey_plot_elements,
        "Three-Act": three_act_plot_elements,
        "Dan Harmon Story Circle": harmon_plot_elements,
        "Fichtean Curve": fichtean_plot_elements,
        "Save the Cat": save_the_cat_plot_elements,
    }

    MAX_SCENES_PER_ACT = 2  # Should be even for scene and sequel
    MAX_TERTIARY_CHARACTERS = 3  # In addition to 6 primary characters

    def __init__(
        self,
        target_audience: Optional[str] = None,
        genre: Optional[str] = None,
        themes: Optional[List[str]] = None,
        narrative_structure: Optional[str] = None,
        time_period: Optional[TimePeriod] = None,
        characters: Dict[str, Character] = None,
        area: Optional[str] = None,
        with_images: bool = False,
        medium: Optional[str] = None,
        style: Optional[str] = None,
    ) -> None:
        """Generate a story based on the target audience and genre."""
        # Select a target audience if none is provided
        if target_audience is None:
            self.target_audience = random.choice(self.target_audiences)
        else:
            self.target_audience = target_audience

        # Select a random genre if none is provided
        if genre is None:
            self.genre = random.choice(self.genres)
        else:
            self.genre = genre

        # Generate 2 random thematic concepts if none are provided
        if themes is None:
            self.themes = []
            for i in range(2):
                self.themes.append(random.choice(self.thematic_concepts))
        else:
            self.themes = themes

        # Make a thematic statement
        # ts_prompt = f"Write a thematic statement based on the concepts of " \
        #            f" {self.themes[0]} and {self.themes[1]}."
        # self.thematic_statement = self.gpt3.generate_text(ts_prompt)

        # Get a random narrative structure if none is provided
        if narrative_structure is None:
            self.narrative_structure = random.choice(
                list(self.narrative_structures.keys())
            )
        else:
            self.narrative_structure = narrative_structure
        # Get associated plot elements for narrative structure
        self.plot_elements = self.narrative_structures[
            self.narrative_structure
        ]

        # Get a random time period if none is provided
        if time_period is None:
            self.time_period = TimePeriod()
        else:
            self.time_period = time_period

        # Generate some characters
        if characters is None:
            self.characters = {
                "protagonist": Character(self.time_period.era),
                "antagonist": Character(self.time_period.era),
                "deuteragonist": Character(self.time_period.era),
                "confidante": Character(self.time_period.era),
                "love interest": Character(self.time_period.era),
                "foil": Character(self.time_period.era),
            }
            for i in range(random.randint(0, self.MAX_TERTIARY_CHARACTERS)):
                self.characters[f"tertiary {i}"] = Character(
                    self.time_period.era
                )
        else:
            self.characters = characters

        # Generate the synopsis
        self.synopsis = (
            f"A {self.genre} story targeted at {self.target_audience}"
            f" during the {self.time_period.era} era. "
            f"{self.characters['protagonist']} must grapple with"
            f" themes of {self.themes[0]} and {self.themes[1]}. "
            f"Using a {self.narrative_structure} narrative "
            f"structure. Starting around "
            f"{self.time_period.time_of_day} during "
            f"{self.time_period.season}."
        )

        # Write a title
        self.title = generate_text(
            f"Write a title for {self.synopsis}", max_tokens=30
        ).strip()
        if ":" in self.title:
            self.subtitle = self.title.split(":")[1].strip()
            self.title = self.title.split(":")[0].strip()

        # Generate the plot as a series of acts with scenes
        self.acts = []
        for act_description in self.plot_elements.values():
            scenes: List["Scene"] = []
            if self.MAX_SCENES_PER_ACT == 2:
                total_scenes_in_act = 2
            else:
                total_scenes_in_act = random.randrange(
                    2,
                    self.MAX_SCENES_PER_ACT,
                    2,
                )
            logger.info(
                f"Generating {total_scenes_in_act} scenes for "
                f"{act_description}."
            )
            # Generate scenes for each plot element
            for i in range(total_scenes_in_act):
                scenes.append(
                    Scene(
                        target_audience=self.target_audience,
                        genre=self.genre,
                        themes=self.themes,
                        act_description=act_description,
                        time_period=self.time_period,
                        characters=self.characters,
                        total_scenes_in_act=total_scenes_in_act,
                        previous_scenes=scenes,
                        area=area,
                    )
                )
            # Add the scenes to the act
            self.acts.append(scenes)

        # Add images if requested
        if with_images:
            self.with_images = with_images
            # TODO: Define medium and style for image set based on genre and
            #  era
            self.image_set = ImageSet(
                medium=medium,
                style=style,
            )
            # Generate an image for each scene
            for act in self.acts:
                for scene in act:
                    label = (
                        f"A{self.acts.index(act) + 1}S"
                        f"{act.index(scene) + 1}"
                    )
                    self.image_set.add_scene_image(label, scene)

    def __str__(self):
        """Return a string representation of the story."""
        full_story = self.synopsis + "\n\n"
        for act in self.acts:
            full_story += f"Act {self.acts.index(act) + 1}\n"
            for scene in act:
                full_story += f"Scene {act.index(scene) + 1}\n"
                full_story += str(scene) + "\n\n"
        return full_story

    def save_as_json(self) -> str:
        """Save a JSON representation of the story."""
        save_path = get_save_path()
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        filename = (
            f"{save_path}"
            f"{''.join(c for c in self.title if c.isalnum())}.json"
        )
        with open(filename, "w") as write_file:
            write_file.write(jsonpickle.encode(self, keys=True, indent=4))
        logger.info(f"Story written to {filename}")
        return filename

    def download_image_set(self):
        """Download images for the story."""
        if self.with_images:
            story_image_dir = os.path.join(
                get_save_path(),
                f"{''.join(c for c in self.title if c.isalnum())}Images",
                "",
            )
            if not os.path.exists(story_image_dir):
                os.mkdir(story_image_dir)
            self.image_set.save_images(story_image_dir)


if __name__ == "__main__":
    # story = Story()
    # story.save_as_json()
    story = load_from_json(os.path.join(get_save_path(), "TheLadysWar.json"))
    story.download_image_set()
