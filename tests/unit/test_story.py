import os

import pytest

from storytime import story

STORY_FILENAME = "../stories/TestStoryTextFromGpt3sMock.json"


@pytest.fixture
def test_story(mocker) -> story.Story:
    mocker.patch(
        "storytime.story.generate_text",
        return_value="Test Story:Text From Gpt3's Mock",
    )
    mocker.patch(
        "storytime.scene.generate_text",
        return_value="Test Scene Text From Gpt3.",
    )
    return story.Story()


def test_save_and_load_as_json(test_story) -> None:
    """Test that a story can be saved as a JSON file and loaded back."""
    errors = []
    test_story.save_as_json()
    # Save mocked story as a JSON file
    if not os.path.exists(STORY_FILENAME):
        errors.append("Story did not save as JSON file.")
    # Load the story from the JSON file
    new_story = story.load_from_json(STORY_FILENAME)
    if new_story is None:
        errors.append("Story did not load from JSON file.")
    # Cleanup the JSON file
    os.remove(STORY_FILENAME)
    # Assert no error message has been registered, else print messages
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))
