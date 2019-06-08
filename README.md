# Invoice Generator

For automatically generating invoices.

# Installation

Install [https://www.tug.org/texlive/quickinstall.html](texlive) first. Then run:

```bash
make install
```

This will install the dependencies required for building.

# Usage

Modify the fields in `variables.tex` and `invoice.tex` appropriately.

To generate the invoice, run:

```bash
make invoice.pdf
```

If your invoice is saved as `invoice123.tex` then to build it you would run `make invoice123.pdf`.

