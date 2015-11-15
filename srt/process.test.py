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


  def test_quotes(self):
    input_text = """692
01:00:55,227 --> 01:00:58,400
How do you say ''sugar''
in your language?"""
    output = split_lines(input_text, [])
    self.assertEqual(output, ['How do you say sugar in your language?'])


  def test_quotes_at_boundary(self):
    input_text = """508
00:40:25,810 --> 00:40:29,233
''Deputy director, lnternal Security.''
Very impressive."""
    output = split_lines(input_text, [])
    self.assertEqual(output, ['Deputy director, Internal Security. Very impressive.'])


  def test_contractions(self):
    input_text = """1
00:01:44,542 --> 00:01:46,379
-Mr. Mills, how are you?
-l'm fine."""
    output = split_lines(input_text, [])
    self.assertEqual(output, ['Mr. Mills, how are you?',  'I\'m fine.'])


  def test_counting(self):
    input_text = """449
00:37:33,543 --> 00:37:35,669
26... 27...
"""
    output = split_lines(input_text, [])
    self.assertEqual(output, ['26... 27...'])


  def test_ls_to_is(self):
    input_text = """526
00:24:54,238 --> 00:24:56,910
Well, if l'd had the number
where you were staying...
"""
    output = split_lines(input_text, [])
    self.assertEqual(output, ['Well, if I\'d had the number where you were staying...'])


  def test_ls_to_is2(self):
    input_text = """101
00:07:43,844 --> 00:07:47,602
-lt'll be perfect. Just like old times.
-Better. No one gets killed.
"""
    output = split_lines(input_text, [])
    self.assertEqual(output, ['It\'ll be perfect. Just like old times.', 'Better. No one gets killed.'])


  def test_ls_to_is3(self):
    input_text = """104
00:08:22,046 --> 00:08:24,676
Ma'am, if you don't mind,
l suggest you keep moving.
"""
    output = split_lines(input_text, [])
    self.assertEqual(output, ['Ma\'am, if you don\'t mind, I suggest you keep moving.'])


  def sanity_check(self):
    input_text="""65
00:06:12,704 --> 00:06:15,543
-How's Kimmy?
-Good. She's good.

66
00:06:15,668 --> 00:06:17,839
Yeah? She sleep over yet?

67
00:06:18,090 --> 00:06:20,595
Well, let's say we're working on it.
"""
    output = split_lines(input_text, [])
    self.assertEqual(output, ['How\'s Kimmy?', 'Good.  She\'s good.', 'Yeah?  She sleep over yet?', 'Well, let\'s just say we\'re working on it.'])

@unittest.skip('Sentence tests')
class TestSentenceMethods(unittest.TestCase):
  def test_sentence_breakup(self):
    input_text="""406
00:30:32,040 --> 00:30:33,220
Their relationship

407
00:30:33,320 --> 00:30:35,180
was mostly centered
around their daughter.

408
00:30:35,280 --> 00:30:36,740
But I think...

409
00:30:36,840 --> 00:30:38,740
he wanted more than friendship."""

if __name__ == '__main__':
    unittest.main()