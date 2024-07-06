""" This module is used to record sound and process it to text. """
import os
import speech_recognition as sr


class SoundRecorder:
    """
    This class is used to record sound and process it to text.
    """
    @staticmethod
    def process_audio(audio_file: str) -> str | None:
        """
        This method is used to process audio file to text.
        :param audio_file: str
        :return: str | None
        """
        r = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_ans = r.record(source)
        try:
            sentence = r.recognize_google(audio_ans)
            # print("You said : ", sentence)
            return sentence
        except Exception as e:
            print(f'Error processing {audio_file}: {e}')
            return None

    @staticmethod
    def get_answers(path_to_answers: str) -> dict[str, str] | dict[str, None]:
        """
        This method is used to get answers from audio files.
        :param path_to_answers: str
        :return: dict
        """
        answers = {}
        try:
            assert os.path.exists(path_to_answers)
            audio_files = [path_to_answers]
        except AssertionError:
            print("Path does not exist")
            print(os.listdir(path_to_answers))
            return answers
        sentence = SoundRecorder.process_audio(audio_files[0])
        print("Answer heard: ", sentence)
        answers['Q'] = sentence
        return answers
