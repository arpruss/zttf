for x in mst/* ; do echo $x  ; (python dumpscad.py $x >> ~/3d/mstfonts.scad )  ; done
python makelist.py ~/3d/mstfonts.scad > list.scad
cat list.scad >> ~/3d/mstfonts.scad
