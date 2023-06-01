import sys
import subprocess
import arxivtools
import arxiv


bibentry = {}
TEXT_FILE = open("reprints.bib", "w")
N = len(sys.argv)
for i in range(1, N):
    ar = arxivtools.getpdfarxivID(sys.argv[i])
    if ar:
        is_arxiv = True
        search = arxiv.Search(id_list=[ar])
        paper = next(search.results())
        bibentry = arxivtools.getbibentry(paper, ar, search)
        btex = arxivtools.bibentrytobibtex(bibentry)
        print(btex["bibtex"], file=TEXT_FILE)
        cmd = "cp " + sys.argv[i] + " " + btex["name"] + ".pdf"
        subprocess.call(cmd, shell=True)
    else:
        print("failed to find arXiv ID")
