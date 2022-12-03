import logging

from storytime.character import Character
from storytime.story import Story
from storytime.time_period import TimePeriod
from storytime.video import create_video

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

story_types = {
    "fairy tale": "Fairy tales are short and interesting tales, featuring "
    "folkloric fantasy characters."
}


def generate_story(
    story_type: str,
    with_images: bool,
) -> Story:
    """Generates a story from the archetype."""
    if story_type == "fairy tale":
        time_period = TimePeriod(era="Medieval")
        characters = {
            "protagonist": generate_character("princess"),
            "antagonist": generate_character("witch"),
            "deuteragonist": generate_character("prince"),
            "confidante": generate_character("wizard"),
            "love interest": generate_character("knight"),
            "foil": generate_character("queen"),
            "tertiary 1": generate_character("king"),
        }
        story = Story(
            target_audience="children",
            genre="fantasy",
            themes=["love", "friendship"],
            narrative_structure="Five-Act",
            time_period=time_period,
            characters=characters,
            area="medieval",
            with_images=with_images,
            medium="digital art",
            style="pixar",
        )
    else:
        logger.error(
            f"Story type: {story_type} not found. Generating random " f"story."
        )
        story = Story()
    return story


character_types = {
    "princess": "A princess",
    "prince": "A prince",
    "king": "A king",
    "queen": "A queen",
    "wizard": "A wizard",
    "witch": "A witch",
    "knight": "A knight",
}


def generate_character(character_type: str) -> Character:
    """Generates a character from the archetype."""
    if character_type == "princess":
        character = Character(
            era="Medieval",
            ethnicity="old-english",
            gender="Female",
            age=14,
        )
    elif character_type == "prince":
        character = Character(
            era="Medieval",
            ethnicity="old-english",
            gender="Male",
            age=10,
        )
    elif character_type == "king":
        character = Character(
            era="Medieval",
            ethnicity="old-english",
            gender="Male",
            age=40,
        )
    elif character_type == "queen":
        character = Character(
            era="Medieval",
            ethnicity="old-english",
            gender="Female",
            age=35,
        )
    elif character_type == "wizard":
        character = Character(
            era="Medieval",
            ethnicity="old-english",
            gender="Male",
            age=62,
        )
    elif character_type == "witch":
        character = Character(
            era="Medieval",
            ethnicity="old-english",
            gender="Female",
            age=66,
        )
    elif character_type == "knight":
        character = Character(
            era="Medieval",
            ethnicity="old-english",
            gender="Male",
            age=25,
        )
    else:
        logger.error(
            f"Character type: {character_type} not found. Generating "
            f"random character."
        )
        character = Character()
    return character


if __name__ == "__main__":
    fairy_tale = generate_story(
        "fairy tale",
        with_images=True,
    )
    fairy_tale.save_as_json()
    fairy_tale.download_image_set()
    fairy_tale.add_narration()
    create_video(fairy_tale)
    print(fairy_tale)
