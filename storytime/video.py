import logging
import os

from moviepy.editor import AudioFileClip, concatenate_audioclips
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from PIL import Image, ImageDraw, ImageFont

from storytime.story import (
    Story,
    get_save_path,
    get_story_image_dir,
    load_from_json,
)

VIDEO_HEIGHT = 480
VIDEO_WIDTH = 854
TITLE_FONT_SIZE = 40
SUBTITLE_FONT_SIZE = 30
BYLINE_FONT_SIZE = 20

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


def create_video(story: Story) -> None:
    """Creates a video from a story"""
    logger.info("Loading audio clips")
    audio_files = story.get_narration_file_list()
    audio_clips = [AudioFileClip(audio_file) for audio_file in audio_files]
    audio_durations = [audio_clip.duration for audio_clip in audio_clips]
    full_audio_clip = concatenate_audioclips(audio_clips)
    # If that has problems, try this:
    # https://stackoverflow.com/questions/64341771/moviepy-mix-multiple-audio-files

    # Create Images
    # Create a title card image if it doesn't already exist
    title_card_path = os.path.join(
        get_story_image_dir(story.title), "Title.png"
    )
    if not os.path.exists(title_card_path):
        logger.info("Creating title card")
        create_title_card(
            story.title,
            story.subtitle,
            f"Written by {story.author}. Illustrated by {story.illustrator}.",
            title_card_path,
        )
    outro_card_path = os.path.join(
        get_story_image_dir(story.title), "Outro.png"
    )
    if not os.path.exists(outro_card_path):
        logger.info("Creating outro card")
        create_outro_card(outro_card_path)
    # Get the image files
    image_dir = get_story_image_dir(story.title)
    image_files = [
        f"{image_dir}{label}.png" for label in story.image_set.images
    ]
    image_files.insert(0, title_card_path)
    # Resize the images to VIDEO_HEIGHT x VIDEO_HEIGHT if they're not already
    logger.info("Resizing images")
    for image_file in image_files:
        image = Image.open(image_file)
        if image.size != (VIDEO_HEIGHT, VIDEO_HEIGHT):
            image = image.resize((VIDEO_HEIGHT, VIDEO_HEIGHT))
            image.save(image_file)
    # Calculate the duration of each image based on the audio durations
    image_durations = [audio_durations[0]]  # The first image is the title
    for i in range(1, len(audio_durations) - 1, 3):
        image_durations.append(sum(audio_durations[i : i + 3]))
    image_durations.append(audio_durations[-1])  # The last image is the outro
    full_images_clip = ImageSequenceClip(
        image_files,
        durations=image_durations,
    )

    # Create the video by joining the audio and images clips
    logger.info("Creating video")
    full_video_clip = full_images_clip.set_audio(full_audio_clip)
    video_save_file = os.path.join(get_save_path(), f"{story.title}.mp4")
    full_video_clip.write_videofile(video_save_file, fps=24)


def create_title_card(
    title: str,
    subtitle: str,
    byline: str,
    save_path: str,
) -> None:
    """Creates a title card for a video"""
    img = Image.new("RGB", (VIDEO_HEIGHT, VIDEO_HEIGHT), color="black")
    fonts_dir = os.path.join(os.path.dirname(save_path), "..", "..", "fonts")
    font_path = os.path.join(fonts_dir, "MangabeyRegular-rgqVO.otf")
    # get a font for the title and subtitle
    title_fnt = ImageFont.truetype(
        font_path,
        TITLE_FONT_SIZE,
    )
    subtitle_fnt = ImageFont.truetype(
        font_path,
        SUBTITLE_FONT_SIZE,
    )
    byline_fnt = ImageFont.truetype(
        font_path,
        BYLINE_FONT_SIZE,
    )
    d = ImageDraw.Draw(img)
    title_y = VIDEO_HEIGHT / 2 - TITLE_FONT_SIZE - 10
    subtitle_y = VIDEO_HEIGHT / 2 + 10
    byline_y = VIDEO_HEIGHT / 2 + SUBTITLE_FONT_SIZE + 20
    d.text((10, title_y), title, font=title_fnt, fill=(255, 255, 255))
    d.text((10, subtitle_y), subtitle, font=subtitle_fnt, fill=(255, 255, 255))
    d.text((10, byline_y), byline, font=byline_fnt, fill=(255, 255, 255))
    img.save(save_path)


def create_outro_card(
    save_path: str,
) -> None:
    """Creates an outro card for a video"""
    img = Image.new("RGB", (VIDEO_HEIGHT, VIDEO_HEIGHT), color="black")
    fonts_dir = os.path.join(os.path.dirname(save_path), "..", "..", "fonts")
    font_path = os.path.join(fonts_dir, "MangabeyRegular-rgqVO.otf")
    # get a font for the title and subtitle
    end_fnt = ImageFont.truetype(
        font_path,
        SUBTITLE_FONT_SIZE,
    )
    d = ImageDraw.Draw(img)
    end_y = VIDEO_HEIGHT / 2 - SUBTITLE_FONT_SIZE - 10
    thankyou_y = VIDEO_HEIGHT / 2 + 10
    d.text((10, end_y), "The End", font=end_fnt, fill=(255, 255, 255))
    d.text(
        (10, thankyou_y),
        "Thank you for watching",
        font=end_fnt,
        fill=(255, 255, 255),
    )
    img.save(save_path)


if __name__ == "__main__":
    test_story = load_from_json(
        os.path.join(get_save_path(), "TorysJourneyofLoveandFriendship.json")
    )
    create_video(test_story)
