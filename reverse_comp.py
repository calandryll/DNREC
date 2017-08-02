from Bio.Seq import Seq
import csv

handle = open('mapping.txt', 'rU')
mfile = list(csv.reader(handle, delimiter = '\t'))
ofile = open('reverse.txt', 'w')

ofile.write('Complement\tReverse_Complement\tReverse\n')

for i in range(len(mfile)):
	comp = Seq(mfile[i][1]).complement()
	reve_comp = Seq(mfile[i][1]).reverse_complement()
	reve = mfile[i][1][::-1]
	ofile.write('%s\t%s\t%s\n' % (comp, reve_comp, reve))