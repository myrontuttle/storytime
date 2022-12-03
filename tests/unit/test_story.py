import os

import pytest
from pytest_mock import MockerFixture

from storytime import story


@pytest.fixture
def test_story(mocker: MockerFixture) -> story.Story:
    mocker.patch(
        "storytime.story.generate_text",
        return_value="Test Story:Text From Gpt3's Mock",
    )
    mocker.patch(
        "storytime.scene.generate_text",
        return_value="Test Scene Text From Gpt3.",
    )
    mocker.patch(
        "storytime.image_set.generate_image",
        return_value="Test Image URL From DALL-E.",
    )
    return story.Story()


def test_save_and_load_as_json(test_story: story.Story) -> None:
    """Test that a story can be saved as a JSON file and loaded back."""
    errors = []
    # Save mocked story as a JSON file
    story_filename = test_story.save_as_json()
    if not os.path.exists(story_filename):
        errors.append("Story did not save as JSON file.")
    # Load the story from the JSON file
    new_story = story.load_from_json(story_filename)
    if new_story is None:
        errors.append("Story did not load from JSON file.")
    # Cleanup the JSON file
    os.remove(story_filename)
    # Assert no error message has been registered, else print messages
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))
