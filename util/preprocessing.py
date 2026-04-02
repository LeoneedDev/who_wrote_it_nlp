# preprocessing steps:
# 1. Concatenated all 100 tweets of each author into one string, with an <EndOfTweet> tag added to the end of each tweet (if applicable).
# 2. Replaced the linefeed characters with <LineFeed>.
# 3. Lowercased the characters
# 4. Trimmed the repeated characters: Replaced repeated character sequences of length 3 or greater with sequences of length 3
# 5. Replaced URLs with <URLURL>
# 6. Replaced @username mentions (i.e., Twitter handles) with <UsernameMention>
# 7. Removed punctuations: Although we did not remove the punctuations in our pre- processing function, scikit-learns TfidfVectorizer function completely ignores punctuation.3

import re
from nltk.tokenize import TweetTokenizer
from numpy import ndarray
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


class TweetPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, user_id_col: str = "user_id", text_col: str = "text", gender_col: str = "gender_label"):
        self.tweet_tok = TweetTokenizer(
            preserve_case=False,
            reduce_len=True,
            strip_handles=False
        )
        self.user_id_col = user_id_col
        self.text_col = text_col
        self.gender_col = gender_col

        self.URL_RE = re.compile(r"""(?ix)\b((?:https?://|www\.)\S+)\b""")
        self.MENTION_RE = re.compile(r"(?i)(?<!\w)@\w+")
        self.LF_RE = re.compile(r"\r\n|\r|\n")
        self.REPEAT_CHARS_RE = re.compile(r"(.)\1{2,}", flags=re.UNICODE)

    def _concat_tweets(self, tweets) -> str:
        tweets = [str(t) for t in tweets]
        if not tweets:
            return ""
        return " <EndOfTweet> ".join(tweets) + " <EndOfTweet>"

    def _preprocess(self, text: str) -> str:
        text = self.LF_RE.sub(" <LineFeed> ", text)
        text = text.lower()
        text = self.REPEAT_CHARS_RE.sub(lambda m: m.group(1) * 3, text)
        text = self.URL_RE.sub(" <URLURL> ", text)
        text = self.MENTION_RE.sub(" <UsernameMention> ", text)
        text = re.sub(r"\s+", " ", text).strip()

        tokens = self.tweet_tok.tokenize(text)
        return " ".join(tokens)

    def fit(self, x=None, y=None):
        return self

    def transform(self, x):
        if hasattr(x, "apply"):
            return x.apply(self._preprocess)

        return [self._preprocess(str(t)) for t in x]

    def concatenate(self, df: pd.DataFrame):
        if isinstance(df, pd.DataFrame):
            if self.user_id_col not in df.columns:
                raise KeyError(f"Missing required column: {self.user_id_col}")
            if self.text_col not in df.columns:
                raise KeyError(f"Missing required column: {self.text_col}")
            if self.gender_col not in df.columns:
                raise KeyError(f"Missing required column: {self.gender_col}")

            df = df.groupby(self.user_id_col).agg({
                self.text_col: self._concat_tweets,
                self.gender_col: "first"
            }).reset_index()

            return df
        else:
            print("Input is not a DataFrame. Skipping concatenation step.")
            return None
