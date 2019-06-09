# Invoice Generator

For automatically generating invoices.

## Dependencies

This project relies on the following:

* [`texlive`](https://www.tug.org/texlive/quickinstall.html)
* [`python3`](https://www.python.org/downloads/)

## Installation

To install the required packages, run:

```bash
make install
```

## Usage

Modify the fields in `variables.yaml` and `invoice.yaml` appropriately.

To generate the invoice, run:

```bash
make invoice.pdf
```

If your invoice is saved as `invoice123.yaml` then to build it you would run `make invoice123.pdf`.


This depends on the [`invoice`](https://ctan.org/pkg/invoice) package. For more information on defining complicated invoices read the [`invoice` documentation](http://mirrors.ctan.org/macros/latex/contrib/invoice/invoice.pdf). You can modify the invoice output by modifying the `invoice.tex` and the`template.tex` files.
