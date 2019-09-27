RENDRER = pandoc

PANDOC_OPTIONS = --filter pandoc-citeproc \
		  --bibliography=${@}.bib \
		  --csl=ieee.csl \
		  --variable papersize=a4paper

all: essay

essay:
	$(RENDRER) $(PANDOC_OPTIONS) -s ${@}.md -o ${@}.pdf
