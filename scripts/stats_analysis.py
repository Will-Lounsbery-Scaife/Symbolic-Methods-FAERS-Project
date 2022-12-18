from scipy.stats import chisquare
import matplotlib.pyplot as plt
import time

startTime = time.time()


def read_results(results_fp):
    import ast
    with open(results_fp, 'r') as f:
        data = f.read()
    # reconstructing the data as a dictionary
    control_dict = ast.literal_eval(data)
    return(control_dict)

results_dict_hw = read_results('/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/resdict_hw.txt')
results_dict_hw2 = read_results('/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/resdict_hw_2.txt')
results_dict_c1 = read_results('/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/resdict_control_1.txt')
results_dict_c2 = read_results('/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/resdict_control_2.txt')
results_dict_c3 = read_results('/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/resdict_control_3.txt')
results_dict_c_g2 = read_results('/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/resdict_hw_2.txt')

'''
mylist = []
for pid in results_dict_hw:
    for drug in results_dict_hw[pid]['drugs']:
        if drug['KEGG']:
            if len(drug['KEGG']['Pathway']) > 0:
                mylist.append(drug['KEGG']['Pathway'])

print(mylist)
'''

# store unique classes and their number of occurences
def get_class_counts(mydict):
    class_counts = {}
    for pid in mydict:
        for drug in mydict[pid]["drugs"]:
            if mydict[pid]["drugs"][drug]["Classes"]:
                try:
                    for cls in mydict[pid]["drugs"][drug]["Classes"]:
                        if cls not in class_counts:
                            class_counts[cls] = 1
                        else:
                            class_counts[cls] += 1
                except:
                    print("get_class_counts exception", pid, drug)
    #global dg_tot
    dg_tot = sum(class_counts.values())
    #dg_tot = len(class_counts)
    result_dg = {key: value for key, value in class_counts.items()}
    sorted_keys_dg = sorted(result_dg.items(), key=lambda item: item[1], reverse=True)
    formatted_items = []
    for item in sorted_keys_dg:
        class_name, level = item[0]
        total_count = item[1]
        dg_percent = total_count/dg_tot
        formatted_items.append([class_name, level, total_count, dg_percent])
    x = sum(item[3] for item in formatted_items)
    print(x)
    return formatted_items
    
    #return class_counts

# store unique classes and their number of occurences
def get_class_counts_level(mydict, level):
    class_counts = {}
    for pid in mydict:
        for drug in mydict[pid]["drugs"]:
            if mydict[pid]["drugs"][drug]["Classes"]:
                try:
                    for cls in mydict[pid]["drugs"][drug]["Classes"]:
                        if cls[0] not in class_counts:
                            class_counts[cls[0]] = 1
                        else:
                            class_counts[cls[0]] += 1
                except:
                    print("get_class_counts_level exception", pid, drug)
    global dg_tot
    dg_tot = len(class_counts)
    print(dg_tot, "level:", level)
    return class_counts

def percentage_conv(mydict):
    # Calculate the total count of all variables in the dict group
    total_count = sum(mydict.values())

    # Create a new dictionary to store the percentages
    percentages = {}

    # Iterate over the variables in the dict 
    for variable, count in mydict.items():
    # Calculate the percentage of the total count for this variable
        percentage = 100 * count / total_count
        # Add the percentage to the new dictionary
        percentages[variable] = percentage
    return percentages


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
    #global pw_tot 
    #pw_tot = len(pw_counts)
    #return pw_counts
    pw_tot = sum(pw_counts.values())
    result_pw = {key: value for key, value in pw_counts.items()}
    sorted_keys_pw = sorted(result_pw.items(), key=lambda item: item[1], reverse=True)
    formatted_items = []
    for item in sorted_keys_pw:
        pw_name, pw_count = item
        pw_percent = pw_count/pw_tot
        formatted_items.append([pw_name, pw_count, pw_percent])
    x = sum(item[2] for item in formatted_items)
    print(x)
    return formatted_items

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
    #global ud_tot
    #global d_tot
    ud_tot = len(d_counts)
    d_tot = dc
    #print(d_counts)
    #return(d_counts)
    result_d = {key: value for key, value in d_counts.items()}
    sorted_keys_d = sorted(result_d.items(), key=lambda item: item[1], reverse=True)
    formatted_items = []
    for item in sorted_keys_d:
        d_name, d_count = item
        d_percent = d_count/d_tot
        formatted_items.append([d_name, d_count, d_percent])
    x = sum(item[2] for item in formatted_items)
    print(x)
    return formatted_items

def get_data(xd, n, stats_a):
    d_hw = get_drug_counts(xd)
    pw_hw = get_pw_counts(xd)
    dg_hw = get_class_counts(xd)
    '''
    d_hw_t = sum(d_hw.values())
    result = {key: ((value / d_hw_t)*100) for key, value in d_hw.items()}
    sorted_keys = sorted(result.items(), key=lambda item: item[1], reverse=True)

    pw_hw = get_pw_counts(xd)
    pw_hw_t = sum(pw_hw.values())
    result_pw = {key: ((value / pw_hw_t)*100) for key, value in pw_hw.items()}
    sorted_keys_pw = sorted(result_pw.items(), key=lambda item: item[1], reverse=True)
    
    dg_hw = get_class_counts(xd)
    #dg_hw_t = sum(dg_hw.values())
    #result_dg = {key: ((value / dg_hw_t)*100) for key, value in dg_hw.items()}
    #sorted_keys_dg = sorted(result_dg.items(), key=lambda item: item[1], reverse=True)
    #sorted_keys_dg_tot = sorted(dg_hw.items(), key=lambda item: item[1], reverse=True)

    #result_dg = {key: value for key, value in dg_hw.items()}
    #sorted_keys_dg = sorted(result_dg.items(), key=lambda item: item[1], reverse=True)
    
    #result_dg_values = result_dg.values()
    #result_dg_sum = sum(result_dg_values)
    #print(result_dg_sum)
    '''
    stats_a.write("drugs\n")
    #for i in range(n):
    for i in range(len(d_hw)):
        stats_a.write(str(d_hw[i])+"\n")

    stats_a.write("\n\npathways\n")
    #for i in range(n):
    for i in range(len(pw_hw)):
        stats_a.write(str(pw_hw[i])+"\n")

    stats_a.write("drug groups\n")
    #for i in range(n):
    for i in range(len(dg_hw)):
        stats_a.write(str(dg_hw[i]) + "\n")

wstat = open("/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/stats.txt", 'w')
wstat.close()

with open("/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/stats.txt", 'a') as fp:
    fp.write("hw1:\n")
    get_data(results_dict_hw, 50, fp)

    fp.write("\n\n\nhw2:\n")
    get_data(results_dict_hw2, 50, fp)

    fp.write("\n\n\nc1:\n")
    get_data(results_dict_c1, 50, fp)

    fp.write("\n\n\nc2:\n")
    get_data(results_dict_c2, 50, fp)

    fp.write("\n\n\nc3:\n")
    get_data(results_dict_c3, 50, fp)

    fp.write("\n\n\nc_g2:\n")
    get_data(results_dict_c_g2, 50, fp)




def chi_sq(experimental, control):
    # Create a list of genes that have a count greater than or equal to 5 in both groups
    genes_to_include = []
    for gene in experimental:
        #if experimental[gene] >= 5:
            if gene in control:
                #if control[gene] >= 5:
                    genes_to_include.append(gene)

    #print(genes_to_include)
    # Extract the values for these genes from each group

    experimental_values = [experimental[gene] for gene in genes_to_include]
    control_values = [control[gene] for gene in genes_to_include]

    #print(experimental_values)
    #print(control_values)

    #sum_experimental = sum(experimental.values())
    #sum_control = sum(control.values())
    #print(sum_experimental)
    #print(sum_control)

    # Conduct the chi-square test
    chi2, p = chisquare(experimental_values, f_exp=control_values)

    # Print the test statistic and p-value
    print("Chi-square test statistic:", chi2)
    print("p-value:", p)

#chi_sq(pw_hw, pw_c1)

def histograms(exp, cont):
    # Create a list of values from the control dictionary
    control_values = list(cont.values())

    # Create a list of values from the experimental dictionary
    experimental_values = list(exp.values())

    # Set the number of bins for the histograms
    num_bins = 20

    # Create the histograms
    plt.hist(control_values, num_bins, alpha=0.5, label='Control')
    plt.hist(experimental_values, num_bins, alpha=0.5, label='Experimental')

    # Add a legend and labels
    plt.legend(loc='upper right')
    plt.xlabel('Value')
    plt.ylabel('Frequency')

    # Display the histograms
    plt.show()

#histograms(pw_hw, pw_c1)

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))