import unittest
from process import split_lines

class TestStringMethods(unittest.TestCase):

  def test_basic(self):
    input_text = """83
00:08:55,911 --> 00:08:58,287
I told you to take
the test with my car.

84
00:08:58,455 --> 00:08:59,622
God. Dad.

85
00:09:03,793 --> 00:09:04,752
Thank you.
"""
    output = split_lines(input_text, [])
    self.assertEqual(output, ['I told you to take the test with my car.', 'God. Dad.', 'Thank you.'])


  def test_multi_speakers(self):
    input_text = """729
01:06:14,866 --> 01:06:16,787
-What?
-Saint-Clair.
"""
    output = split_lines(input_text, [])
    self.assertEqual(output, ['What?', 'Saint-Clair.'])


  def test_html(self):
    input_text = """895
01:26:43,156 --> 01:26:46,204
<i>Attention, travelers.
You are not required to--</i>
"""
    output = split_lines(input_text, [])
    self.assertEqual(output, ['Attention, travelers. You are not required to--'])


  def test_multiple_sentences(self):
    input_text = """856
01:16:02,416 --> 01:16:04,504
...discounts, buybacks.
All sales are final.
"""
    output = split_lines(input_text, [])
    self.assertEqual(output, ['...discounts, buybacks. All sales are final.'])


  def test_character_expressions(self):
    input_text = """154
00:14:35,708 --> 00:14:37,125
Where is he?
(MUFFLED SCREAM)
"""
    output = split_lines(input_text, [])
    self.assertEqual(output, ['Where is he?'])


  def test_character_names(self):
    input_text = """155
00:14:43,132 --> 00:14:45,217
LENORE: Stu,
where are you going?
Come back!
"""
    output = split_lines(input_text, [])
    self.assertEqual(output, ['Stu, where are you going? Come back!'])


  def test_counting(self):
    input_text = """449
00:37:33,543 --> 00:37:35,669
26... 27...
"""
    output = split_lines(input_text, [])
    self.assertEqual(output, ['26... 27...'])


if __name__ == '__main__':
    unittest.main()