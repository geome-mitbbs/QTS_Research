import csv

def dict_array_to_csv(dict_list,filename,fields=None):
    with open(filename, 'w', newline='') as csvfile:
        if fields == None:
            fields = dict_list[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        for d in dict_list:
            writer.writerow(d)


