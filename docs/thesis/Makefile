BASEDIR=$(CURDIR)
SOURCEDIR=$(BASEDIR)/source
OUTPUTDIR=$(BASEDIR)/output
STATICDIR=$(BASEDIR)/static

BIBFILE=$(SOURCEDIR)/references.bib

help:
	@echo ' 																	  '
	@echo 'Makefile for the Markdown thesis                                       '
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make pdf                         generate a PDF file  			  '
	@echo ' 																	  '
	@echo 'get local templates with: pandoc -D latex/html/etc	  				  '
	@echo 'or generic ones from: https://github.com/jgm/pandoc-templates		  '

pdf:
	pandoc $(BASEDIR)/meta.yaml $(SOURCEDIR)/*.md \
	-o $(OUTPUTDIR)/thesis.pdf \
	--template=$(SOURCEDIR)/template.tex \
	--top-level-division=chapter \
	-N \
	--pdf-engine=xelatex \
	--filter pandoc-fignos \
	--filter pandoc-tablenos \
	--filter pandoc-secnos \
	--filter pandoc-citeproc \
	--verbose

.PHONY: pdf
