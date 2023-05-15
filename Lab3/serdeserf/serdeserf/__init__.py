import argparse as argp
import sys
import re
import importlib
import os


from serdeser_test import do_test
from main_class import Serdeser


def main():
    if not sys.argv[1::]:
        print("Run tests")
        do_test()
        return

    parser = argp.ArgumentParser(description="from one file to another")
    parser.add_argument("inputfile", type=str, help="Absolute path of input file")
    parser.add_argument(
        "inputformat", type=str, help="format, from which will be constructed object"
    )
    parser.add_argument("outputfile", type=str, help="Absolute path to the output file")
    parser.add_argument(
        "outputformat",
        type=str,
        help="format, to which will be serialized object from input file",
    )

    if len(sys.argv) == 2:
        with open(sys.argv[1]) as cnfg:
            args = cnfg.read()
        args = [it.group(0) for it in re.finditer(r'(?:\S+|"[^"]*")', args)]
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()

    serin = Serdeser(args.inputformat)
    obj = serin.load(args.inputfile)
    serout = Serdeser(args.outputformat)
    serout.dump(obj, args.outputfile)


if __name__ == "__main__":
    main()
