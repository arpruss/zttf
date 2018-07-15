rm fontmetricdata.scad
for x in mst/* ; do echo $x ; (python dumpscad.py $x >> fontmetricdata.scad )  ; done
python makelist.py fontmetricdata.scad > list.scad
cat list.scad >> fontmetricdata.scad
cat fontmetrics-head.scad fontmetricdata.scad > fontmetrics.scad
