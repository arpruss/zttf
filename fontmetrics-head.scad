// begin MIT licensed code (c) 2018 Alexander Pruss
BOLD = 1;
ITALIC = 2;
CONDENSED = 32;

function startswith(a,b,offset=0,position=0) =
    len(a)-offset < len(b) ? false : 
    position >= len(b) ? true :
    a[offset+position] != b[position] ? false :
    startswith(a,b,offset=offset,position=position+1);

function findsubstring(a,b,position=0) =
    len(a)-position < len(b) ? -1 :
    startswith(a,b,offset=position) ? position :
    findsubstring(a,b,position=position+1);
    
function style(a,b,n) =
    findsubstring(a,b) >= 0 ? n : 0;
    
function substring(a,start,end=undef,soFar="") =
    start >= len(a) || (end != undef && start >= end) ? soFar :
    substring(a,start+1,end=end,soFar=str(soFar,a[start]));
    
function lowercaseChar(c) = 
    c < "A" || c > "Z" ? c :
    chr(search(c,"ABCDEFGHIJKLMNOPQRSTUVWXYZ")[0]+97);
    
function lowercase(s,start=0,soFar="") =
    start >= len(s) ? soFar :
    lowercase(s,start=start+1,soFar=str(soFar,lowercaseChar(s[start])));
    
function styleNumber(s) = 
    style(s, "bold", BOLD) + 
    style(s, "italic", ITALIC) + 
    style(s, "oblique", ITALIC) +
    style(s, "condensed", CONDENSED);

function familyAndStyle(s) =
    let(lc=lowercase(s),
        n=findsubstring(lc,":style="))
    n < 0 ? [s, 0] :
    [substring(s,0,n), styleNumber(substring(lc,n+7))];
    
function findEntry(data, index) = data[search([index], data, 1, 0)[0]];
    
/*function findEntry_recursive(data, index, offset=0) =
    offset >= len(data) ? undef :
    data[offset][0] == index ? data[offset] :
    findEntry(data, index, offset=offset+1); */
    
    
function findFont(fonts, s) = findEntry(fonts, familyAndStyle(s));

function measureWithFontAt(string,font,offset) =
    let(g=findEntry(font[4],string[offset]))
    g == undef ? 0 :
    offset + 1 >= len(string) ? g[1] : // at end of string
    let(kern=findEntry(g[2], string[offset+1]))
    kern == undef ? g[1] :
    g[1] + kern[1];
    
function measureWithFont(string, font, offset=0, soFar=0) =
    offset >= len(string) ? soFar :
    measureWithFont(string,font,offset=offset+1,soFar=soFar+measureWithFontAt(string,font,offset));

function measureText(string, font="Arial", size=10., spacing=1., fonts=FONTS) = 
    let(f=findFont(FONTS, font))
    spacing * size / f[1] * measureWithFont(string, f);

function ascender(font="Arial", size=10.) =
    size;

function descender(font="Arial", size=10.) =
    let(f=findFont(FONTS, font))
    -size / f[1] * f[2];
// end MIT licensed code

