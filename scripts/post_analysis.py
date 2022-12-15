import matplotlib.pyplot as plt
from KEGG_add import FAERS_standard_get_KEGG_info

results_dict_2 = FAERS_standard_get_KEGG_info()
#print(results_dict_2)


def read_results(results_fp):
    import ast
    with open(results_fp, 'r') as f:
        data = f.read()
    # reconstructing the data as a dictionary
    control_dict = ast.literal_eval(data)
    return(control_dict)

#results_dict_2 = read_results('/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/resdict_control.txt')

print("iter3")
print("writing")
write_obj0 = open('/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/resdict_control.txt', 'w')
write_obj0.close()
results_obj0 = open('/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/resdict_control.txt', 'a')
results_obj0.write(str(results_dict_2))
print("almost there")

# store unique classes and their number of occurences
def get_class_counts(mydict):
    class_counts = {}
    for pid in mydict:
        for drug in mydict[pid]["drugs"]:
            try:
                if drug["KEGG"]:
                    for cls in drug["KEGG"]["Classes"]:
                            if cls not in class_counts:
                                class_counts[cls] = 1
                            else:
                                class_counts[cls] += 1
            except:
                print("get_class_counts exception", pid, drug)
    return class_counts

def get_drug_counts(mydict):
    d_counts = {}
    for pid in mydict:
        for drug in mydict[pid]["drugs"]:
            try:
                d = drug['drug_name']
                if d not in d_counts:
                    d_counts[d] = 1
                else:
                    d_counts[d] += 1
            except:
                print("Drug_count none error:", pid)
    return(d_counts)


# store unique targets and their number of occurences
def get_tg_counts(mydict):
    tg_counts = {}

    for pid in mydict:
        for drug in mydict[pid]["drugs"]:
            try:
                if drug["KEGG"]:
                    for tg in drug["KEGG"]["Target"]:
                        if tg not in tg_counts:
                            tg_counts[tg] = 1
                        else:
                            tg_counts[tg] += 1
            except:
                print("tg counts exception", pid)

    return tg_counts



def get_empty_KEGG(somedict):
    no_kegg = 0
    for pid in somedict:
        try:
            for drug in somedict[pid]['drugs']:
                if drug['KEGG'] == None:
                    no_kegg += 1
        except:
            print("empty KEGG count error", pid)
    return no_kegg


def plot_top(kegg_key, num):
  # Sort the dictionary by values in descending order
  sorted_groups = sorted(kegg_key.items(), key=lambda x: x[1], reverse=True)

  # Get the keys and values from the dictionary
  keys = [x[0] for x in sorted_groups]
  values = [x[1] for x in sorted_groups]

  # Only keep the top 20 values
  keys = keys[:num]
  values = values[:num]

  # Set the x-axis labels and the y-axis range
  plt.xticks(range(len(keys)), keys, rotation=90)
  plt.ylim([0, max(values)])

  # Add a bar for each drug group, with the height of the bar
  # determined by the corresponding value in the dictionary
  plt.bar(range(len(keys)), values)

  # Show the plot
  plt.show()



print("getting kegg info")
class_ct = get_class_counts(results_dict_2)
d_ct = get_drug_counts(results_dict_2)
empty_KEGG = get_empty_KEGG(results_dict_2)
tg_ct = get_tg_counts(results_dict_2)

print("writing kegg info")
write_KEGG = open('/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/KEGG_control.txt', 'w')
write_KEGG.close()
results_obj1 = open('/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/KEGG_control.txt', 'a')
results_obj1.write(str(empty_KEGG)+"\n")
results_obj1.write(str(class_ct) + "\n\n\n")
results_obj1.write(str(d_ct) + "\n\n\n")
results_obj1.write(str(tg_ct) + "\n\n\n")

results_obj1.close()
print("done!")

#plot_top(class_ct, 20)

