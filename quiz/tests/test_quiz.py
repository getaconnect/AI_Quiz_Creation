import unittest
from quiz.quiz_generator import generate_quiz

class TestQuiz(unittest.TestCase):
    def test_quiz_generation_non_empty(self):
        # Provide sample content that is sufficient for generating a quiz.
        sample_content = (
            "This is a sample description of a business website. "
            "It offers innovative solutions for modern problems."
        )
        result = generate_quiz(sample_content)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

if __name__ == "__main__":
    unittest.main()
