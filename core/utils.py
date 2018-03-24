# -*- coding: utf-8 -*-

import re


all_roman_re = re.compile(r'[ivxIVX]+$')
abc_bullet_re = re.compile(r'[a-zA-Z]$')
digit_bullet_re = re.compile(r'([0-9]+\.)*[0-9]+$')
quotes = u'"\'“”'
non_sentence_ends = [
    'inc.', 'ltd.', 'llc.',
    'et.', 'al.', 'etc.',
    'mr.', 'ms.', 'mrs.',
    'u.s.',
]


def is_bullet(s):
    if not s.endswith('.'):
        return False
    s = s[:-1]
    return any([all_roman_re.match(s),
                abc_bullet_re.match(s),
                digit_bullet_re.match(s)])


def is_abbreviation(s_p, s, s_n):
    """
    Checks whether the word `s` is an abbreviation using its context,
    i.e. the previous word `s_p` and the next word `s_n`.
    """

    # No length restriction by default
    def _is_name(s, max_len=float('inf')):
        s = s.strip('.,:;')
        return 0 < len(s) <= max_len and s[0].isupper() and s.isalnum() and not s.isdigit()

    # Name abbreviation, e.g. John D. Smith
    if _is_name(s_p) and _is_name(s, max_len=1) and _is_name(s_n):
        return True

    return False


def is_non_sentence_end(s):
    s = s.strip(quotes).lower()
    return s in non_sentence_ends


def merge_bad_sentsplits(sentences):
    """ Merge special cases (e.g. bullets) of unwanted splits. """

    def _merge_two(sent, sent_after):
        to_merge = False
        if sent_after.strip() == '':
            to_merge = True
        else:
            toks = sent.strip().split('\n')[-1].split()
            if len(toks) > 0:
                if len(toks) == 1 and is_bullet(toks[0]):
                    to_merge = True
                elif is_non_sentence_end(toks[-1]):
                    to_merge = True
                elif len(toks) > 1:
                    toks_after = sent_after.strip().split('\n')[0].split()
                    if len(toks_after) > 0:
                        to_merge = is_abbreviation(toks[-2], toks[-1], toks_after[0])

        if to_merge:
            return [sent + sent_after]
        return [sent, sent_after]

    # Merge the unwanted splits
    merged = sentences[:1]
    for sent_after in sentences[1:]:
        sent = merged.pop()
        merged.extend(_merge_two(sent, sent_after))
    return merged


sentence_split_re = re.compile(
    ur'((?<=[^A-Z].[.?!])\s+(?=[A-Z])|(?<=[^A-Z].[.?!])\s*[\n\r]+|[\n\r]\s*[\n\r]+|'
    # Those 2 again for the case of <Text "quoted." New sent.>
    ur'(?<=[^A-Z].[.?!]["\'“”])\s+(?=[A-Z])|(?<=[^A-Z].[.?!]["\'“”])\s*[\n\r]+|[\n\r]\s*[\n\r]+|'
    # And the case of ALL-CAPS
    ur'(?<=[^a-z][.?!])\s+(?=[A-Z])|(?<=[^a-z][.?!])\s*[\n\r]+|[\n\r]\s*[\n\r]+)',
    re.UNICODE
)


def is_title(sentence):
    """
    Checks whether a sentence looks like a title.

    A title may be defined as several capitalized words, possibly separated
    with some conjunctions, determiners or prepositions. Bullets at the
    beginning of the sentence are allowed, but they aren't counted as words.
    Punctuation characters at the end aren't allowed.

    A (non-empty) sentence is considered to be a title, if it consists at most
    MAX_MAIN_WORDS_COUNT capitalized words (containing the main meaning,
    i.e. "main" words). In addition to the "main" words, some "auxiliary"
    (i.e. non-capitalized) words are also allowed, but only if they are short
    enough (i.e. up to MAX_AUX_WORD_LENGTH characters in length). The
    "auxiliary" words are assumed to be some conjunctions, determiners or
    prepositions.

    E.g.: "Terms of Service", "Terms of Use", etc.
    """
    MAX_MAIN_WORDS_COUNT = 4
    MAX_AUX_WORD_LENGTH = 4

    sentence = sentence.strip()
    if not sentence:
        return False
    if sentence[-1] in (',', ';', ':'):
        return False
    capitalized_words_count = 0
    words = sentence.split()
    for index, word in enumerate(words):
        if index == 0 and is_bullet(word):
            continue
        if word[0].isupper():  # "main" word
            capitalized_words_count += 1
        elif len(word) <= MAX_AUX_WORD_LENGTH:  # "auxiliary" word
            continue
        else:
            return False
    return 1 <= capitalized_words_count <= MAX_MAIN_WORDS_COUNT


def split_sentences(text):
    """
    Splits a block of plain text into sentences (boundaries are captured too).
    """

    sentences = sentence_split_re.split(text)
    sentences = merge_bad_sentsplits(sentences)
    # Try to additionally split sentences with titles
    sentences_with_titles = []
    for sentence in sentences:
        left_part, _, right_part = sentence.strip().partition('\n')
        if right_part and is_title(left_part):
            # Preserve original indentation
            index = sentence.find(left_part)
            left_part, right_part = (sentence[:index + len(left_part) + 1],
                                     sentence[index + len(left_part) + 1:])
            sentences_with_titles.append(left_part)
            sentences_with_titles.append(right_part)
        else:
            sentences_with_titles.append(sentence)
    return sentences_with_titles
