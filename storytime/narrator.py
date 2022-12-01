"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import logging

from google.cloud import texttospeech

MAX_INPUT_LENGTH = 5000
INTRO_BREAK = '<speak><break time="2s"/>'
OUTRO_BREAK = '<break time="2s"/></speak>'

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


class Narrator:
    """Narrator class for synthesizing speech from text."""

    def __init__(self, language_code="en-US"):
        """Instantiates a client."""
        self.client = texttospeech.TextToSpeechClient()
        # Build the voice request, select the language code ("en-US") and

        # Select the type of audio file you want returned
        self.audio_config = texttospeech.AudioConfig(
            {
                "audio_encoding": texttospeech.AudioEncoding.MP3,
            }
        )

    def synthesize_speech(
        self,
        text_input: str,
        voice_gender: str,
        output_file: str,
    ):
        """Synthesizes speech from the input string of text or ssml.

        Note: ssml must be well-formed according to:
            https://www.w3.org/TR/speech-synthesis/
        """
        max_length = MAX_INPUT_LENGTH - len(INTRO_BREAK) - len(OUTRO_BREAK)
        if len(text_input) > max_length:
            logger.warning(
                f"Input text is too long, truncating to max "
                f"length: {max_length}."
            )
            text_input = text_input[:max_length]
        ssml_text = INTRO_BREAK + text_input + OUTRO_BREAK
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(
            {
                "ssml": ssml_text,
            }
        )

        # the ssml voice gender ("neutral")
        if voice_gender == "MALE":
            ssml_gender = texttospeech.SsmlVoiceGender.MALE
        elif voice_gender == "FEMALE":
            ssml_gender = texttospeech.SsmlVoiceGender.FEMALE
        else:
            ssml_gender = texttospeech.SsmlVoiceGender.NEUTRAL
        voice = texttospeech.VoiceSelectionParams(
            {
                "language_code": "en-US",
                "ssml_gender": ssml_gender,
            }
        )

        # Perform the text-to-speech request on the text input with the
        # selected voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=self.audio_config,
        )

        # The response's audio_content is binary.
        with open(output_file, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print(f"Audio content written to file '{output_file}'")


if __name__ == "__main__":
    narrator = Narrator()
    narrator.synthesize_speech(
        text_input="This is a test of the narrator class.",
        voice_gender="MALE",
        output_file="TestOutput.mp3",
    )
