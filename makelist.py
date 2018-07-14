from sys import argv
import re

fonts = []
with open(argv[1]) as f:
	for line in f:
		if line.startswith("FONT_"):
			fonts.append(line.split()[0])
print("FONTS = [ " + ', '.join(fonts) + " ];\n")
