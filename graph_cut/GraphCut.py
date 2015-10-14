
import argparse
from graph_cut import CutUI

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Interactive Graph Cut",
                                     description="Interactively segment an image", add_help=True)
    parser.add_argument('-i', '--INFILE', help='Input image file to segment.', required=True)
    parser.add_argument('-o', '--OUTFILE', help='Used to save segmented images.', required=True)

    args = parser.parse_args()

    ui = CutUI.CutUI(args.INFILE)
    ui.run()
