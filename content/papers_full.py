"""Full length practice papers, modelled on each board's past papers.

Each paper has the real paper's total marks, time allowed and structure, which
mskbuild/papercheck.py checks against the official figures at build time.
"""
from content.papers_j277 import PAPERS as J277
from content.papers_aqa import PAPERS as AQA
from content.papers_edexcel import PAPERS as EDEXCEL
from content.papers_h446 import PAPERS as H446
from content.papers_r093 import PAPERS as R093
from content.papers_da import PAPERS as DA

FULL_PAPERS = J277 + AQA + EDEXCEL + H446 + R093 + DA
