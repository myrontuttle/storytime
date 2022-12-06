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
    "folkloric fantasy characters.",
    "science fiction comedy": "Science fiction comedy is a genre of "
    "science fiction that combines science fiction with comedy.",
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
            themes=["friendship", "dreams"],
            narrative_structure="Five-Act",
            time_period=time_period,
            characters=characters,
            area="medieval",
            with_images=with_images,
            medium="digital art",
            style="pixar",
        )
    elif story_type == "science fiction comedy":
        time_period = TimePeriod(era="Future")
        characters = {
            "protagonist": generate_character("ensign"),
            "antagonist": generate_character("captain"),
            "deuteragonist": generate_character("engineer"),
            "confidante": generate_character("chief medical officer"),
            "love interest": generate_character("lieutenant"),
            "foil": generate_character("technician"),
            "tertiary 1": generate_character("crewman"),
        }
        story = Story(
            target_audience="teenagers",
            genre="science fiction comedy",
            themes=["coming of age", "artificial intelligence"],
            narrative_structure="Five-Act",
            time_period=time_period,
            characters=characters,
            area="space",
            with_images=with_images,
            medium="digital art",
            style="photorealistic",
        )
    else:
        logger.error(
            f"Story type: {story_type} not found. Generating random " f"story."
        )
        story = Story()
    return story


def generate_character(character_type: str) -> Character:
    """Generates a character from the archetype."""
    if character_type == "princess":
        character = Character(
            era="Medieval",
            ethnicity="old-english",
            gender="Female",
            age=14,
            occupation="princess",
        )
    elif character_type == "prince":
        character = Character(
            era="Medieval",
            ethnicity="old-english",
            gender="Male",
            age=10,
            occupation="prince",
        )
    elif character_type == "king":
        character = Character(
            era="Medieval",
            ethnicity="old-english",
            gender="Male",
            age=40,
            occupation="king",
        )
    elif character_type == "queen":
        character = Character(
            era="Medieval",
            ethnicity="old-english",
            gender="Female",
            age=35,
            occupation="queen",
        )
    elif character_type == "wizard":
        character = Character(
            era="Medieval",
            ethnicity="old-english",
            gender="Male",
            age=62,
            occupation="wizard",
        )
    elif character_type == "witch":
        character = Character(
            era="Medieval",
            ethnicity="old-english",
            gender="Female",
            age=66,
            occupation="witch",
        )
    elif character_type == "knight":
        character = Character(
            era="Medieval",
            ethnicity="old-english",
            gender="Male",
            age=25,
            occupation="knight",
        )
    elif character_type == "ensign":
        character = Character(
            era="Future",
            ethnicity="spanish",
            gender="Male",
            age=25,
            occupation="ensign",
        )
    elif character_type == "captain":
        character = Character(
            era="Future",
            ethnicity="german",
            gender="Male",
            age=35,
            occupation="captain",
        )
    elif character_type == "engineer":
        character = Character(
            era="Future",
            ethnicity="hindi",
            gender="Female",
            age=26,
            occupation="engineer",
        )
    elif character_type == "chief medical officer":
        character = Character(
            era="Future",
            ethnicity="korean",
            gender="Female",
            age=40,
            occupation="chief medical officer",
        )
    elif character_type == "lieutenant":
        character = Character(
            era="Future",
            ethnicity="swahili",
            gender="Female",
            age=27,
            occupation="lieutenant",
        )
    elif character_type == "technician":
        character = Character(
            era="Future",
            ethnicity="english",
            gender="Male",
            age=24,
            occupation="technician",
        )
    elif character_type == "crewman":
        character = Character(
            era="Future",
            ethnicity="japanese",
            gender="Male",
            age=32,
            occupation="crewman",
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
        "science fiction comedy",
        with_images=True,
    )
    fairy_tale.save_as_json()
    fairy_tale.download_image_set()
    fairy_tale.add_narration()
    create_video(fairy_tale)
    print(fairy_tale)
