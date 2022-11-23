from typing import List

import random

from storytime.character import Character
from storytime.gpt3 import GPT3
from storytime.scene import Scene
from storytime.time_period import TimePeriod


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
        "Action",
        "Adventure",
        "Comedy",
        "Crime",
        "Drama",
        "Fantasy",
        "Historical",
        "Horror",
        "Mystery",
        "Paranormal",
        "Romance",
        "Science fiction",
        "Thriller",
        "Western",
    ]

    # Thematic concepts
    # https://michaelbjorkwrites.com/2019/09/26/story-themes-list-ideas-for
    # -your-novel/
    thematic_concepts = [
        # Experiences
        "Aging",
        "Childhood",
        "Coming of Age",
        "Disillusionment",
        "Friendship",
        "Growth",
        "Healing",
        "Isolation",
        "Loss",
        "Loss of Innocence",
        "Overcoming Adversity",
        "Parenthood",
        "Redemption",
        "Revenge",
        "Self-discovery",
        "Survival",
        "Tragedy",
        # Feelings
        "Apathy",
        "Compassion",
        "Despair",
        "Fear",
        "Grief",
        "Jealousy",
        "Joy",
        "Loneliness",
        "Love",
        "Regret",
        # Gender & Sexuality
        "Androgyny",
        "Femininity",
        "Gender Identity",
        "Masculinity",
        "Sexuality",
        # Human Perception
        "Dreams",
        "Identity",
        "Memory",
        "Perception vs. Reality",
        "Subjectivity",
        # Mental Health & Neurodiversity
        "Autism",
        "Bipolarity",
        "Depression",
        "Obsessive Compulsive Disorder",
        "Suicide",
        # Natural Forces
        "Death",
        "Fate",
        "Nature",
        "Passage of Time",
        # Politics & Economics
        "Capitalism",
        "Communism",
        "Conservation",
        "Democracy",
        "Fascism",
        "Freedom",
        "Justice",
        "Nationalism",
        "Peace",
        "Propaganda",
        "Radicalism",
        "Socialism",
        "War",
        # Religion & Philosophy
        "Atheism",
        "Determinism",
        "Ethics",
        "Faith",
        "Free Will",
        "Good vs. Evil",
        "Skepticism",
        "Metaphysics",
        "Nature vs. Nurture",
        "Pacifism",
        "Religion",
        "Soul / Consciousness",
        # Social Issues
        "Abuse of Power",
        "Homophobia",
        "Immigration",
        "Inequality",
        "Oppression",
        "Poverty",
        "Progress & Regress",
        "Privilege",
        "Racism",
        "Rights of the Oppressed",
        "Sexism",
        "Transphobia",
        "Working Class Struggles",
        # Society & Culture
        "Conformity",
        "Familial Obligations",
        "Honor",
        "Individualism",
        "Responsibility",
        "Tradition",
        # Technology & Science
        "Artificial Intelligence",
        "Augmented Reality",
        "Genetic Engineering",
        "Human Integration with Technology",
        "Information Privacy",
        "Weapons of Mass Destruction",
        # Virtues & Vices
        "Ambition",
        "Corruption",
        "Courage",
        "Forgiveness",
        "Mercy",
        "Power",
        "Pride",
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
        "Exposition": "The status quo or ‘ordinary world’ is established.",
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

    def __init__(self):
        """Initialize the class."""
        # Initialize GPT-3
        self.gpt3 = GPT3()

        # Select a target audience
        self.target_audience = random.choice(self.target_audiences)

        # Generate a random genre
        self.genre = random.choice(self.genres)

        # Generate 2 random thematic concepts
        self.themes = []
        for i in range(2):
            self.themes.append(random.choice(self.thematic_concepts))

        # Make a thematic statement
        # ts_prompt = f"Write a thematic statement based on the concepts of " \
        #            f" {self.themes[0]} and {self.themes[1]}."
        # self.thematic_statement = self.gpt3.gpt3_request(ts_prompt)

        # Get a random narrative structure and associated plot elements
        self.narrative_structure = random.choice(
            list(self.narrative_structures.keys())
        )
        self.plot_elements = self.narrative_structures[
            self.narrative_structure
        ]

        # Get a random time period
        self.time_period = TimePeriod()

        # Generate some characters
        self.characters = {
            "protagonist": Character(self.time_period.era),
            "antagonist": Character(self.time_period.era),
            "deuteragonist": Character(self.time_period.era),
            "confidante": Character(self.time_period.era),
            "love interest": Character(self.time_period.era),
            "foil": Character(self.time_period.era),
        }
        for i in range(random.randint(0, 5)):
            self.characters[f"tertiary {i}"] = Character(self.time_period.era)

        # Generate the synopsis
        self.synopsis = (
            f"A {self.genre} targeted at {self.target_audience}"
            f" during the {self.time_period.era} era. "
            f"{self.characters['protagonist']} must grapple with"
            f" themes of {self.themes[0]} and {self.themes[1]}. "
            f"Using a {self.narrative_structure} narrative "
            f"structure. Starting around "
            f"{self.time_period.time_of_day} during "
            f"{self.time_period.season}."
        )

        # Generate the plot as a series of acts with scenes
        self.acts = []
        for act_description in self.plot_elements.values():
            scenes: List["Scene"] = []
            total_scenes_in_act = random.randrange(2, 10, 2)
            # Generate scenes for each plot element
            for i in range(total_scenes_in_act):
                scenes.append(
                    Scene(
                        self.target_audience,
                        self.genre,
                        self.themes,
                        act_description,
                        self.time_period,
                        self.characters,
                        total_scenes_in_act,
                        scenes,
                    )
                )
            # Add the scenes to the act
            self.acts.append(scenes)

    def __str__(self):
        """Return a string representation of the story."""
        full_story = self.synopsis + "\n\n"
        for act in self.acts:
            for scene in act:
                full_story += str(scene) + "\n\n"
        return full_story


if __name__ == "__main__":
    story = Story()
    print(story)
