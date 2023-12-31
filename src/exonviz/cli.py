"""
Module that contains the command line app, so we can still import __main__
without executing side effects
"""

import argparse
import re
import sys
import gzip
from importlib import resources

from typing import List, Dict, Any
from .draw import draw_exons
from .exon import Exon
from .mutalyzer import fetch_exons, fetch_variants, build_exons

from .draw import _config


def get_MANE() -> Dict[str, str]:
    fname = str(resources.files("exonviz.data").joinpath("mane.txt.gz"))
    with gzip.open(fname, "rt") as fin:
        mane = dict()
        for line in fin:
            gene, transcript = line.strip("\n").split("\t")
            mane[gene] = transcript
    return mane


def check_input(transcript: str) -> str:
    """Check the input from the user, and rewrite when needed"""
    # If it looks like there is no variant
    if re.match(r"^\w+\.\d+$", transcript):
        return f"{transcript}:c.="

    # If it looks like the user forgot the version number, there isn't much we can do
    if re.match(r"^\w+$", transcript):
        msg = "Please specify the version of the transcript you are interested in: "
        raise RuntimeError(msg + transcript)

    return transcript


def make_exons(transcript: str, config: Dict[str, Any]) -> List[Exon]:
    """Make or fetch the requested exons"""

    # If the transcript is actually the gene name, substitute the MANE transcript
    MANE = get_MANE()
    transcript = MANE.get(transcript, transcript)
    if transcript in MANE:
        transcript = MANE[transcript]
    else:
        # Does the transcript format make sense?
        transcript = check_input(transcript)

    exons = fetch_exons(transcript)
    variants = fetch_variants(transcript)

    return build_exons(exons, variants, config)


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Description of command.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("transcript", help="Transcript (with version) to visualise")

    for key, value, description in _config:
        # Booleans are a special case
        if type(value) == bool:
            action = "store_false" if value else "store_true"
            parser.add_argument(
                f"--{key}", default=value, action=action, help=description
            )
        else:
            parser.add_argument(
                f"--{key}",
                type=type(value),
                default=value,
                help=description,
            )

    return parser


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()

    # Make the configuration for the drawing
    config = dict()
    for key, *_ in _config:
        config[key] = getattr(args, key)

    # Try to talk to mutalyzer
    try:
        exons = make_exons(args.transcript, config)
    except RuntimeError as e:
        print(e, file=sys.stderr)
        exit(1)

    for exon in exons:
        print(exon, file=sys.stderr)

    plot = draw_exons(
        exons,
        config=config,
    )
    print(plot)


if __name__ == "__main__":
    main()
