import os

import pytest
import pytest_mock

from storytime import story


def test_save_as_json(mocker):
    """Test that a story can be saved as a JSON file."""
    mocker.patch(
        "storytime.story.generate_text",
        return_value="Test Story Text From Gpt3",
    )
    expected_file = "../stories/TestStoryTextFromGpt3.json"
    mocker.patch(
        "storytime.scene.generate_text",
        return_value="Test Scene Text From Gpt3.",
    )
    my_story = story.Story()
    my_story.save_as_json()
    assert os.path.isfile(expected_file)
