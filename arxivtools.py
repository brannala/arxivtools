import re
import hashlib
from PyPDF2 import PdfReader


# regular expression matching arXiv IDs such as arXiv:1807.09116v1
ARXIV_REGEX = (
    r".*arXiv\:([0-9a-zA-Z.]+)\s+"
    )

# compiled regular expression
# Options M: match ^ $ on multiple lines S: meta . match all chars including \n
arxiv_re = re.compile(ARXIV_REGEX, re.M|re.S)


# reformat data for authors
def getauthors(arxivid, sr):
    pa = next(sr.results())
    raw_authors = str(pa.authors).split("'")
    authorlist = []
    for a1 in raw_authors:
        ma1 = re.match(r"\w+\s+(\w+[.]?)?\w+", a1)
        if ma1:
            authorlist.append(a1)
    authors = ", ".join(authorlist)
    return authors


# extract arxiv ID from text of pdf file
def getpdfarxivID(pdfname):
    reader = PdfReader(pdfname)
    for j in range(0, len(reader.pages)-1):
        pagej = reader.pages[j]
        ptext = pagej.extract_text()
        ar = arxiv_re.match(ptext)
        if ar:
            arxivID = ar.group(1)
            print("extracted arXiv ID: " + arxivID)
            return arxivID
    return False


# get properties for biblio from arxiv site
def getbibentry(paper, arxivid, search):
    bibentry = {}
    bibentry["title"] = str(paper.title)
    bibentry["author"] = getauthors(arxivid, search)
    bibentry["journal"] = "Arxiv"
    bibentry["volume"] = " "
    bibentry["year"] = str(paper.published.year)
    bibentry["pages"] = " "
    return bibentry


# convert bibentry to bibtex format
def bibentrytobibtex(bibentry):
    h = hashlib.sha256(bytes(bibentry["title"], "utf-8"))  # uniq hash of title
    hd = h.hexdigest()[0:5]  # first 5 chars of hash
    newname = (
        # new uniq file name of orig name with short hash appended
        bibentry["author"].split()[-1] + "_" + bibentry["year"] + "_" + hd
    )
    bibtex = "@article{" + newname + ",\n"
    bibtex += "year = {" + bibentry["year"] + "},\n"
    bibtex += "volume = {" + bibentry["volume"] + "},\n"
    bibtex += "pages = {" + bibentry["pages"] + "},\n"
    bibtex += "author = {" + bibentry["author"] + "},\n"
    bibtex += "title = {" + bibentry["title"] + "},\n"
    bibtex += "journal = {" + bibentry["journal"] + "},\n"
    bibtex += "}"
    return {"name": newname, "bibtex": bibtex}
