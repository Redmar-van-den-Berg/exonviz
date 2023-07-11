[![Continous integration](https://github.com/Redmar-van-den-Berg/exonviz/actions/workflows/ci.yml/badge.svg)](https://github.com/Redmar-van-den-Berg/exonviz/actions/workflows/ci.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

# Exonviz
Visualise exons
------------------------------------------------------------------------
## Usage
Pass either a transcript (with version!), or a valid HGVS description to exonviz to generate a figure.
### Options
Since each gene is different, you will probably want to play around with the options to get the perfect figure for your favorite gene.

```bash

usage: exonviz [-h] [--max-width MAX_WIDTH] [--height HEIGHT] [--non-coding]
               [--gap GAP]
               transcript

Description of command.

positional arguments:
  transcript            Transcript (with version) to visualise

optional arguments:
  -h, --help            show this help message and exit
  --max-width MAX_WIDTH
                        Maximum width of the figure (default: inf)
  --height HEIGHT       Exon height (default: None)
  --non-coding          Show non coding regions (default: False)
  --gap GAP             Gap between the exons (default: None)
```

## Examples
### SDHD
Using the default settings, which does not include non-coding regions of the exon.

`exonviz "NG_012337.3(NM_003002.4):c.274G>T" > SDHD.svg`

![Figure of SDH exons](examples/SDHD.svg)

### DMD
Since DMD has many exons, we specify a maximum width for the figure

`exonviz "NM_004006.3:c.=" --max-width 1024 > DMD.svg`

![Figure of DMD exons](examples/DMD.svg)

# PLP1
Include the non coding regions in the figure for PLP1

`exonviz "NM_000533.5" --non-coding > PLP1.svg`

![Figure of PLP1 exons](examples/PLP1.svg)

# NF1
Set the maximum width of the figure to the approximate size of the largest exon

`exonviz "ENST00000358273.9" --non-coding --max-width 3300 > NF1-202.svg`

![Figure of NF1 exons](examples/NF1-202.svg)

# ATXN1, show non coding, increase the maximum width and height of the picture, and
# increase the gap between exons
exonviz ENST00000436367.6 --non-coding --max-width 4000 --height 150 --gap 50 > ATXN1.svg
