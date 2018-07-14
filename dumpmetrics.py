import sys
from zttf.ttfile import TTFile


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <font filename>".format(sys.argv[0]))
        sys.exit(0)

    t = TTFile(sys.argv[1])
    if not t.is_valid:
        print("Invalid")
        sys.exit(0)
        
    f = t.faces[0]    
    glyphs = {}    
    for c in range(0,65536):
        try:
            g = f.char_to_glyph(c)
            if g:
                glyphs[c] = g
        except:
            pass
    chars = sorted(glyphs.keys())

    print("Family "+f.font_family)
    print("Name "+f.name)
    print("Ascender "+str(f.ascender))
    print("Descender "+str(f.descender))
    print("Units "+str(f.units_per_em))
    print("MacStyle "+str(f.tables[b'head'].mac_style))
    for c in chars:
        glyph = f.char_to_glyph(c)
        print("Width %d %d %d" % (c, f.glyph_metrics[glyph][0], f.glyph_metrics[glyph][1]))
        for c2 in chars:
            r = f.char_to_glyph(c2)
            if (glyph,r) in f.glyph_kern:
                print("Kern %d %d %d" % (c, c2, f.glyph_kern[(glyph,r)]))
            
