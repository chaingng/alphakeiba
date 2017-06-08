from keiba_datasets import KeibaDatasets
from numpy import array

keiba = KeibaDatasets()
list = keiba.sanrenpuku()

# for line in list:
#     print line
#     print line[:3]
#     print line[3:]
#     break

num_array = array(list)

print num_array[:,:3]
print num_array[:,3]
