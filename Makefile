PDFLATEX = pdflatex
TLMGR = tlmgr

DEP_FILE = requirements.txt

.PHONY: install clean

install:
	sudo $(TLMGR) install $(shell cat ${DEP_FILE})
	# Keep no backups (not required, simply makes cache bigger)
	sudo $(TLMGR) option -- autobackup 0
	# Update the TL install but add nothing new
	sudo $(TLMGR) update --self --all --no-auto-install


clean:
	rm -rf *.aux *.log *.out

