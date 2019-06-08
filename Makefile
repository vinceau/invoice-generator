PDFLATEX = pdflatex
TLMGR = tlmgr

DEP_FILE = requirements.txt
DOCUMENT = \\input{variables}\\include{template}

.PHONY: install clean

install:
	sudo $(TLMGR) install $(shell cat ${DEP_FILE})
	# Keep no backups (not required, simply makes cache bigger)
	sudo $(TLMGR) option -- autobackup 0
	# Update the TL install but add nothing new
	sudo $(TLMGR) update --self --all --no-auto-install

%.pdf: %.tex
	$(PDFLATEX) "\\input{$*}${DOCUMENT}" -o $@

clean:
	rm -rf *.aux *.log *.out

