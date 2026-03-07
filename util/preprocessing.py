import re
from nltk.tokenize import TweetTokenizer

# preprocessing steps:
# 1. Replaced the linefeed characters with <LineFeed>.
# 2. Concatenated all 100 tweets of each author into one string, with an <EndOfTweet> tag added to the end of each tweet.
# 3. Lowercased the characters
# 4. Trimmed the repeated characters: Replaced repeated character sequences of length 3 or greater with sequences of length 3
# 5. Replaced URLs with <URLURL>
# 6. Replaced @username mentions (i.e., Twitter handles) with <UsernameMention>
# 7. Removed punctuations: Although we did not remove the punctuations in our pre- processing function, scikit-learns TfidfVectorizer function completely ignores punctuation.3
# 8. Stop words were detected by document frequency and removed. Any n-gram that occurred in all documents was considered a stop word and was ignored.


class Preprocessor:
    def __init__(self):
        self.tweet_tok = TweetTokenizer(
            preserve_case=False, reduce_len=True, strip_handles=False
        )
        self.URL_RE = re.compile(r"""(?ix)\b((?:https?://|www\.)\S+)\b""")
        self.MENTION_RE = re.compile(r"(?i)(?<!\w)@\w+")
        self.LF_RE = re.compile(r"\r\n|\r|\n")
        self.REPEAT_CHARS_RE = re.compile(r"(.)\1{2,}", flags=re.UNICODE)

    def tokenize_one_tweet(self, text: str) -> list[str]:
        text = self.LF_RE.sub(" <LineFeed> ", text)
        text = text.lower()
        text = self.REPEAT_CHARS_RE.sub(lambda m: m.group(1) * 3, text)
        text = self.URL_RE.sub(" <URLURL> ", text)
        text = self.MENTION_RE.sub(" <UsernameMention> ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return self.tweet_tok.tokenize(text)
