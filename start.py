import build
import sys
try:
    ch = build.get_character()
    build.display_character(ch)
except:
    sys.exit()