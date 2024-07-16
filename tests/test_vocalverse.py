import unittest
from unittest.mock import patch, MagicMock
import io

# Import functions from vocalverse.py
from vocalverse import get_language_code, text_to_speech, text_to_speech_file_export, translate_text

class TestTranscribeModule(unittest.TestCase):

    def test_get_language_code(self):
        self.assertEqual(get_language_code('english'), 'en')
        self.assertEqual(get_language_code('ENGLISH'), 'en')
        self.assertEqual(get_language_code('fr'), 'fr')
        self.assertEqual(get_language_code('nonexistentlanguage'), 'nonexistentlanguage')

    def test_text_to_speech(self):
        with patch('vocalverse.gTTS') as mock_gtts, patch('pygame.mixer') as mock_mixer:
            # Mocking gTTS and pygame.mixer
            mock_gtts.return_value = MagicMock()
            mock_mixer.music.get_busy.return_value = False
            text_to_speech('Hello', 'english')
            mock_gtts.assert_called_with(text='Hello', lang='en')
            mock_mixer.music.load.assert_called()
            mock_mixer.music.play.assert_called()

    def test_text_to_speech_file_export(self):
        with patch('vocalverse.gTTS') as mock_gtts:
            mock_tts_instance = MagicMock()
            mock_gtts.return_value = mock_tts_instance

            result = text_to_speech_file_export('Hello', 'english', 'test_file', 'mp3')
            self.assertEqual(result, 'test_file.mp3')
            mock_tts_instance.save.assert_called_with('test_file.mp3')

    def test_translate_text(self):
        with patch('vocalverse.translator.translate') as mock_translate:
            mock_translate.return_value.text = 'Hola'
            result = translate_text('Hello', 'english', 'spanish')
            self.assertEqual(result, 'Hola')
            mock_translate.assert_called_with('Hello', src='en', dest='es')

if __name__ == '__main__':
    unittest.main()
