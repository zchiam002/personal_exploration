"""Build every book in the series.

    python3 build.py                 # all titles, all languages they have
    python3 build.py hua-mulan       # just one
"""

import sys

import layout
import puss_in_boots, beanstalk, beauty, mulan, sleeping_beauty
import red_riding_hood

BOOKS = [puss_in_boots, beanstalk, beauty, mulan, sleeping_beauty,
         red_riding_hood]


SUFFIX = "-v2"          # v1 PDFs are kept under pdf/v1/


def main(only=None):
    for book in BOOKS:
        if only and book.SLUG not in only:
            continue
        for lang in book.TEXT:
            print("wrote", layout.build(book, lang, suffix=SUFFIX))


if __name__ == "__main__":
    main(sys.argv[1:] or None)
