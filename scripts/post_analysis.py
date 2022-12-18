import matplotlib.pyplot as plt
from KEGG_add import FAERS_standard_get_KEGG_info
from ID_search import add_FAERS_standard_data_to_dictionary

tdict = add_FAERS_standard_data_to_dictionary(1)

#results_dict_control_3 = FAERS_standard_get_KEGG_info(tdict[0], tdict[1])
#results_dict_control_1 = FAERS_standard_get_KEGG_info(tdict[0], tdict[1])
results_dict_control_2 = FAERS_standard_get_KEGG_info(tdict[0], tdict[1])

#print(results_dict_2)

dg_tot = 0
pw_tot = 0
d_tot = 0
ud_tot = 0
tg_tot = 0
nk_tot = 0


def read_results(results_fp):
    import ast
    with open(results_fp, 'r') as f:
        data = f.read()
    # reconstructing the data as a dictionary
    control_dict = ast.literal_eval(data)
    return(control_dict)

#results_dict_control_3 = read_results('/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/resdict_control_3.txt')
#results_dict_control_1 = read_results('/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/resdict_control.txt')


write_obj0 = open('/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/resdict_control_g2.txt', 'w')
write_obj0.close()
results_obj0 = open('/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/resdict_control_g2.txt', 'a')
results_obj0.write(str(results_dict_control_2))


# store unique classes and their number of occurences
def get_class_counts(mydict):
    class_counts = {}
    for pid in mydict:
        for drug in mydict[pid]["drugs"]:
            try:
                if mydict[pid]["drugs"][drug]["Classes"]:
                    for cls in mydict[pid]["drugs"][drug]["Classes"]:
                        if cls not in class_counts:
                            class_counts[cls] = 1
                        else:
                            class_counts[cls] += 1
            except:
                print("get_class_counts exception", pid, drug)
    global dg_tot
    dg_tot = len(class_counts)
    return class_counts

def get_drug_counts(mydict):
    d_counts = {}
    dc = 0
    for pid in mydict:
        for drug in mydict[pid]["drugs"]:
            dc += 1
            try:
                d = drug
                if d not in d_counts:
                    d_counts[d] = 1
                else:
                    d_counts[d] += 1
            except:
                print("Drug_count none error:", pid)
    global ud_tot
    global d_tot
    ud_tot = len(d_counts)
    d_tot = dc
    #print(d_counts)
    return(d_counts)


# store unique targets and their number of occurences
def get_tg_counts(mydict):
    tg_counts = {}
    for pid in mydict:
        for drug in mydict[pid]["drugs"]:
            if mydict[pid]["drugs"][drug]["Target"]:
                try:
                    for tg in mydict[pid]["drugs"][drug]["Target"]:
                        if tg not in tg_counts:
                            tg_counts[tg] = 1
                        else:
                            tg_counts[tg] += 1
                except:
                    print("tg counts exception", pid)
    global tg_tot
    tg_tot = len(tg_counts)
    return tg_counts

# store unique pathways and their number of occurences
def get_pw_counts(mydict):
    pw_counts = {}
    for pid in mydict:
        for drug in mydict[pid]["drugs"]:
            if mydict[pid]["drugs"][drug]["Pathway"]:
                try:
                    for pw in mydict[pid]["drugs"][drug]["Pathway"]:
                        if pw not in pw_counts:
                            pw_counts[pw] = 1
                        else:
                            pw_counts[pw] += 1
                except:
                    print("pw counts exception", pid)
    global pw_tot 
    pw_tot = len(pw_counts)
    return pw_counts

def get_empty_KEGG(somedict):
    nk_ct = set([])
    yk_ct = set()
    no_kegg = 0
    for pid in somedict:
        for drug in somedict[pid]['drugs']:
                if somedict[pid]['drugs'][drug]['D_number'] == None:
                    no_kegg += 1
                    nk_ct.add(drug)
                else:
                    x = []
                    x.append(somedict[pid]['drugs'][drug]['D_number'])
                    x.append(drug)
                    yk_ct.add(tuple(x))
        #except:
        #    print("empty KEGG count error", pid)
    global nk_tot
    nk_tot = len(nk_ct)
    #x = str(yk_ct).replace("'", "")
    x = list(yk_ct)
    y = str(x).replace("'", "")
    #print(y)
    #print(x)
    print(nk_tot)
    #print(list(x))
    return nk_ct


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
    plt.tight_layout()
    plt.title("Control")

    # Show the plot
    #plt.show()


class_ct = get_class_counts(results_dict_control_2)
d_ct = get_drug_counts(results_dict_control_2)
empty_KEGG = get_empty_KEGG(results_dict_control_2)
tg_ct = get_tg_counts(results_dict_control_2)
pw_ct = get_pw_counts(results_dict_control_2)

write_KEGG = open('/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/KEGG_control_g2.txt', 'w')
write_KEGG.close()
results_obj_c = open('/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/KEGG_control_g2.txt', 'a')
results_obj_c.write("drug groups:\n" + str(class_ct) + "\n\n\n")
results_obj_c.write("drugs:\n" + str(d_ct) + "\n\n\n")
results_obj_c.write("targets:\n" + str(tg_ct) + "\n\n\n")
results_obj_c.write("pathways:\n" + str(pw_ct) + "\n\n\n")
results_obj_c.close()


print("control total drugs:", d_tot)
print("control total unique drugs", ud_tot)
nkp = float(nk_tot)/float(d_tot)
print("control no kegg:", nk_tot)
print("control percent of unkegged drugs:", nkp)
#print("control no kegg drug names:", empty_KEGG)
print("control total unique drug groups", dg_tot)
print("control total unique targets", tg_tot)
print("control total unique pathways:", pw_tot)

'''
# Data to plot
labels = ['Unique Drugs', 'No KEGG Entry']
sizes = [889, 45]
# Create the pie chart
plt.pie(sizes, labels=labels)

# Show the plot
#plt.show()
'''

plot_top(d_ct, 20)
#plt.show()
