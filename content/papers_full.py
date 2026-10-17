"""Full length practice papers, modelled on each board's past papers.

Each paper has the real paper's total marks, time allowed and structure, which
mskbuild/papercheck.py checks against the official figures at build time.
"""
from content.papers_j277 import PAPERS as J277
from content.papers_aqa import PAPERS as AQA
from content.papers_edexcel import PAPERS as EDEXCEL

FULL_PAPERS = J277 + AQA + EDEXCEL
