PDFLATEX = pdflatex
TLMGR = tlmgr
PYTHON3 = python3

PYTHON_SCRIPT = generate.py
PYTHON_REQ = requirements.txt
LATEX_REQ = requirements_latex.txt
DOCUMENT = \\input{variables}\\include{template}

.PHONY: install clean

install:
	pip3 install --user -r ${PYTHON_REQ}
	sudo $(TLMGR) install $(shell cat ${LATEX_REQ})
	# Keep no backups (not required, simply makes cache bigger)
	sudo $(TLMGR) option -- autobackup 0
	# Update the TL install but add nothing new
	sudo $(TLMGR) update --self --all --no-auto-install

%.pdf: %.yaml
	$(PYTHON3) ${PYTHON_SCRIPT} -i "$*.yaml" -o "$@"

clean:
	rm -rf *.aux *.log *.out

