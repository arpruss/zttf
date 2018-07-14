rm mstfonts.scad
for x in mst/* ; do echo $x ; (python dumpscad.py $x >> mstfonts.scad )  ; done
python makelist.py mstfonts.scad > list.scad
cat list.scad >> mstfonts.scad
