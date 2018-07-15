rm fontmetricsdata.scad
for x in mst/* ; do echo $x ; (python dumpscad.py $x >> fontmetricsdata.scad )  ; done
python makelist.py fontmetricsdata.scad > list.scad
cat list.scad >> fontmetricsdata.scad
