import sys
import argparse
import pathlib

if sys.version_info < (3, 9):
    raise Exception("Must be using Python 3.9+")


def parse_args():
    def parse_round_coords(arg_str):
        try:
            round_coords = [int(_) for _ in arg_str.split(',')]
            while 0 < len(round_coords) < 3:
                round_coords.append(round_coords[-1])
            if len(round_coords) != 3:
                raise ValueError
            if any(_ < 0 for _ in round_coords):
                raise ValueError
        except ValueError:
            raise argparse.ArgumentTypeError("expected one, two, or three non-negative comma-separated integers")
        return round_coords

    parser = argparse.ArgumentParser(description='Clean an OBJ file and/or work around the TTS OBJ import bug.')
    parser.add_argument('-z', '--shorten_values', dest='shorten_values', action=argparse.BooleanOptionalAction,
                        default=False,
                        help='Strip any superfluous characters in coord values (e.g. leading/trailing zeros, trailing '
                             'decimal point, or negative sign for 0).')
    parser.add_argument('-r', '--round-coords', dest='round_coords', metavar='N[,N[,N]]', type=parse_round_coords,
                        help='If one N is provided, round all coord values to N decimal places. If a second N is '
                             'provided, use the second for texture coords. If a third N is provided, use the second '
                             'and third for U and V texture coords respectively (useful for non-1:1-aspect-ratio '
                             'textures).')
    parser.add_argument('-d', '--dedupe', dest='dedupe', action=argparse.BooleanOptionalAction, default=False,
                        help='Merge duplicate vertex, normal, or UV elements, after any shortening/rounding, and remove'
                             'any not used by faces.')
    parser.add_argument('-m', '--max-face-verts', dest='max_face_verts', metavar='M', type=int, default=4,
                        help='Report an error if any face has more than M vertices.')
    parser.add_argument('-b', '--tts-bugfix', dest='tts_bugfix', action=argparse.BooleanOptionalAction, default=True,
                        help='Duplicate vertices as needed to work around the TTS OBJ import bug.')
    parser.add_argument('in_path', metavar='IN_PATH', type=pathlib.Path,
                        help='the OBJ file to read')
    parser.add_argument('out_path', metavar='OUT_PATH', type=pathlib.Path,
                        help='the OBJ file to write (silently overwrites)')
    return parser.parse_args()


def main():
    args = parse_args()
    print('args:', args)
    print('Nothing implemented yet!')
    sys.exit(1)


if __name__ == "__main__":
    main()
