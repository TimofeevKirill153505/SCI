import unittest
import re

import text_analysis as t_a


class MyTest(unittest.TestCase):
    def test_sentence_expr(self):
        self.assertTrue(re.match(t_a.sentence_template, "I am a simple sentence."))
        self.assertTrue(re.match(t_a.sentence_template, "I am a sentence with numbers, also i have a 1 comma."))
        self.assertTrue(re.match(t_a.sentence_template,"Am i a simple sentence?"))
        self.assertTrue(re.match(t_a.sentence_template, "What? There is another sentence?!"))
        self.assertEqual(len(re.findall(t_a.sentence_template, "I am the first sentence. And i am the second one.")), 2)


    def test_word_expr(self):
        self.assertTrue(re.match(t_a.word_template, "word"))
        self.assertTrue(re.match(t_a.word_template, "a124"))
        self.assertFalse(re.match(t_a.word_template,"123"))
        self.assertEqual(len(re.findall(t_a.word_template, "1 first second 3 fourth.")), 3)
    

    def test_analyze_sentences(self):
        tupl = (False, 5, 22)
        sentence_match = re.findall(t_a.sentence_template ,"first second four five six?!")
        self.assertEqual(t_a.analyze_sentence(sentence_match[0]), tupl)

        tupl = (True, 4, 23)
        sentence_match = re.findall(t_a.sentence_template ,"Apple, pie, thing, a1b2o3b4a5.")
        self.assertEqual(t_a.analyze_sentence(sentence_match[0]), tupl)
    