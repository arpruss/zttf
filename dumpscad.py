import re
import sys
from zttf.ttfile import TTFile
from struct import unpack

def glyphBox(f,g):
    data = f.get_glyph_data(g)
    if not len(data):
        return (0,0,0,0)
    return unpack(">hhhhh", data[:10])[1:]

def describeChar(c):
    if c >= 32 and c<127 and c != ord('\\') and c != ord('"'):
        return '"'+chr(c)+'"'
    else:
        return "chr(%d)" % c

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <font filename>".format(sys.argv[0]))
        sys.exit(0)

    t = TTFile(sys.argv[1])
    t = TTFile(sys.argv[1])
    if not t.is_valid:
        print("Invalid")
        sys.exit(0)
        
    f = t.faces[0]    
    glyphs = {}    
    for c in range(0, 65536):
        try:
            g = f.char_to_glyph(c+0xF000 if f.name == "Webdings" and c<256 else c)
            if g:
                glyphs[c] = g
        except:
            pass
    chars = sorted(glyphs.keys())
    """
    maxAscent = 0
    for r in (range(ord('A'),ord('Z')+1),range(ord('a'),ord('z')+1)):
        for c in r:
            if c in glyphs:
                data = f.get_glyph_data(glyphs[c])
                ascent = unpack(">hhhhh", data[:10])[4]
                print(chr(c),ascent)
                maxAscent = max(ascent,maxAscent)
    """
    ascent = f.tables[b'os2'].sTypoAscender

    fontID = re.sub(r"[^0-9A-Za-z]", "_", f.name)
    if fontID[0].isdigit():
        fontID = "_" + fontID
    print("""FONT_%s = [
 ["%s", // family
 %d], // style
 %d, // ascender
 %d, // descender
 %d, // line gap
 %f, // units_per_em
 [""" % (fontID, f.font_family,  f.tables[b'head'].mac_style, ascent, 
       f.tables[b'os2'].sTypoDescender, 
       f.tables[b'os2'].typo_line_gap,
       f.units_per_em))
    for c in chars:
        try:
            glyph = glyphs[c]
            box = glyphBox(f,glyph)
            line = " [%s,%d,%d,%d,%d,%d,%d,[" % ( describeChar(c), f.glyph_metrics[glyph][0],
                     f.glyph_metrics[glyph][1], box[0], box[1], box[2], box[3] )
            kerns=[]
            for c2 in chars:
                r = f.char_to_glyph(c2)
                if (glyph,r) in f.glyph_kern:
                    kerns.append("[%s,%d]" % (describeChar(c2), f.glyph_kern[(glyph,r)]))
            line += ','.join(kerns)+"]],"
            print(line)
        except:
            pass
    print(" ]\n];\n")
            
