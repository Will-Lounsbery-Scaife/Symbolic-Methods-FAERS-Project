import requests
import ID_search_hw
import copy
import traceback


# strings for KEGG request URLs
KEGG_find_base = 'https://rest.kegg.jp/find/drug/'
KEGG_get_base = 'https://rest.kegg.jp/get/'



# function to generate the appropriate URLs for KEGG API queries
# uses the find request to search a drug string, then determines the d-number of the drug for the get-url 
def KEGG_find_query(drug_string):
    poss1 = 0
    find_url = KEGG_find_base + drug_string
    find_req = requests.get(find_url)
    a = find_req.text.split("\n")
    b = []
    for l in a:
        b.append(l.split("\t"))
    b.pop()
    # iterate through find entries to find INN names, extract the d number
    # if multiple entries contain INN, store the first one with matching start
    for found_entry in b:
        #print("here1", found_entry[1].lower())
        #print("here2", drug_string)

        if "INN" in found_entry[1] and found_entry[1].lower().startswith(drug_string.lower()):
            get_url = KEGG_get_base + found_entry[0]
            x = found_entry[0].split(":")
            d_number = x[1]
            # put d number at end of get URL
            return [find_url, get_url, d_number]

    for found_entry in b:
        if "INN" in found_entry[1]:
            get_url = KEGG_get_base + found_entry[0]
            x = found_entry[0].split(":")
            d_number = x[1]
            poss1 = [find_url, get_url, d_number]
            break
    # if no "INN" entries found, store first that has drug name not preceded by non-whitespace chars
    for found_entry in b:
        if found_entry[1].lower().startswith(drug_string.lower()):
            d_number = found_entry[0].split(":")[1]
            x = [find_url, KEGG_get_base + b[0][0], d_number]
            #print("case3", d_number)
            return x
    #for found_entry in b:
    # otherwise, just store first entry
    #if poss1: return poss1
    #print("otherwise", drug_string, b[0][0].split(":")[1])
    if poss1 != 0: return poss1
    return [find_url, KEGG_get_base + b[0][0], b[0][0].split(":")[1]]

# send get request to Kegg and store drug targets, pathway, and class
# send get request to Kegg and store drug targets, pathway, and class
def KEGG_get_query(get_URL):
    
    target = []
    pathway = []
    class_info = []
    get_req = requests.get(get_URL)
    klines = get_req.iter_lines()
    # booleans to keep track of if a line stores info on pathway, class, or target
    is_targ = 0
    is_path = 0
    is_class = 0
    # iterate through get response
    for line in klines:
        dec = line.decode("utf-8")
        #if dec.startswith("STR_MAP"): print(dec)
        # line has class info
        if dec.startswith("CLASS"):
            is_class = 1
            is_path = 0
            is_targ = 0
        if dec[2:9]=="PATHWAY":
            is_path = 1
            is_targ = 0
            is_class = 0
        # line does not have class info
        elif dec.startswith("REMARK"):
            is_class = 0
            is_targ = 0
            is_path = 0
        # line has target info
        elif dec.startswith("TARGET"):
            is_targ = 1
            is_class = 0
            is_path = 0
        # line has pathway info, not target info
        elif dec.startswith("STR_MAP"):
            is_targ = 0
            is_path = 0
            is_class = 0
        elif dec.startswith("BRITE") or dec.startswith("METABOLISM") or dec.startswith("REMARK") or dec.startswith("EFFICACY"):
            is_targ = 0
            is_path = 0
            is_class = 0
        # line no longer has path info
        elif dec.startswith("INTERACTION"):
            is_targ = 0
            is_class =0
            is_path = 0
        # if the line corresponds to a field of interest, store it
        if is_class == 1: 
            # gets the name and dg-number of the KEGG drug classes 
            class_info.append(dec[12:])
        elif is_targ == 1: target.append(dec[12:])
        elif is_path == 1: 
            p = dec[12:].split("(")
            o = p[0].split(" ")
            pathway.append(o[0])
    # store drug groups
    class_list = set()
    for ind in range(len(class_info)):
        if class_info[ind].startswith(" DG"):
            y = class_info[ind].strip(" ").split(" ")[0]
            x = tuple([y, 1])
            class_list.add(x)
        elif class_info[ind].startswith("  DG"):
            y = class_info[ind].strip(" ").split(" ")[0]
            x = tuple([y, 2])
            class_list.add(x)
        elif class_info[ind].startswith("   DG"):
            y = class_info[ind].strip(" ").split(" ")[0]
            x = tuple([y, 3])
            class_list.add(x)
        elif class_info[ind].startswith("    DG"):
            y = class_info[ind].strip(" ").split(" ")[0]
            x = tuple([y, 4])
            class_list.add(x)
    return(target, pathway, class_list)


# update dictionary with info from KEGG API requests
# copy for testing
def FAERS_standard_get_KEGG_info():
    mycase = 1
    results_dict = ID_search_hw.add_FAERS_standard_data_to_dictionary(mycase)
    F_KEGG_copy = copy.deepcopy(results_dict)
    dcount = 0
    icount = 1
    kegg_find_results = 0
    kegg_get_results = 0
    drug_storage = {}
    for reportID in F_KEGG_copy:
        print(reportID, icount)
        icount += 1
        for drug in F_KEGG_copy[reportID]['drugs']:
            dcount += 1
            print(dcount)
            dname = drug.copy()['drug_name']
            # if we've already found this drug, just grab its info
            if dname in drug_storage:
                #current_drug = copy.deepcopy(drug_storage[dname])
                #drug = copy.deepcopy(drug_storage[dname])
                #current_drug = drug_storage[dname].copy()
                #drug = current_drug.copy()
                print("duplicate", drug)
                print("original:", drug_storage[dname])
                #drug = copy.deepcopy(drug_storage[dname])
                #print("now drug")
                index = F_KEGG_copy[reportID]['drugs'].index(drug)
                dup_drug = copy.deepcopy(drug_storage[dname])
                print("copy", dup_drug)
                F_KEGG_copy[reportID]['drugs'][index] = copy.deepcopy(drug_storage[dname])
                

                continue
            if type(drug['KEGG']) == dict:
                a = copy.deepcopy(drug['KEGG'])
            else:
                a = drug['KEGG']
            # fix for "ibrutinib"
            if drug['drug_name'] == 'ibrutinib':
                kegg_get_results = KEGG_get_query('https://rest.kegg.jp/get/dr:D03936')
                a['get_URL'] = 'https://rest.kegg.jp/get/dr:D03936'
                a['D_number'] = 'D03936'
                a['Target'] = kegg_get_results[0]
                a['Pathway'] = kegg_get_results[1]
                a['Classes'] = kegg_get_results[2]
                drug['KEGG'] = a
                drug_storage[dname] = copy.deepcopy(drug)
                #current_drug = copy.deepcopy(drug_storage[dname])
                #drug = copy.deepcopy(current_drug)
                continue
            # fix for "Streptococcus pneumoniae" vaccine
            if drug['drug_name'].startswith('Streptococcus pneumoniae'):
                kegg_get_results = KEGG_get_query('https://rest.kegg.jp/get/dr:D10455')
                a['get_URL'] = 'https://rest.kegg.jp/get/dr:D10455'
                a['D_number'] = 'D10455'
                a['Target'] = kegg_get_results[0]
                a['Pathway'] = kegg_get_results[1]
                a['Classes'] = kegg_get_results[2]
                drug['KEGG'] = a
                drug_storage[dname] = copy.deepcopy(drug)
                continue
            # fix for "insulin, regular, human"
            if drug['drug_name'] == 'insulin, regular, human':
                kegg_find_results = KEGG_find_query('insulin human')
                kegg_get_results = KEGG_get_query(kegg_find_results[1])
                a['get_URL'] = kegg_find_results[1]
                a['D_number'] = kegg_find_results[2]
                a['Target'] = kegg_get_results[0]
                a['Pathway'] = kegg_get_results[1]
                a['Classes'] = kegg_get_results[2]
                drug['KEGG'] = a
                drug_storage[dname] = copy.deepcopy(drug)
                continue
            # fix for Ursodiol
            if drug['drug_name'] == 'ursodeoxycholate':
                kegg_find_results = KEGG_find_query('Ursodiol')
                kegg_get_results = KEGG_get_query(kegg_find_results[1])
                a['get_URL'] = kegg_find_results[1]
                a['D_number'] = kegg_find_results[2]
                a['Target'] = kegg_get_results[0]
                a['Pathway'] = kegg_get_results[1]
                a['Classes'] = kegg_get_results[2]
                drug['KEGG'] = a
                drug_storage[dname] = copy.deepcopy(drug)
                continue
            # try with original RxNorm drug name
            try:
                kegg_find_results = KEGG_find_query(drug['drug_name'])
                kegg_get_results = KEGG_get_query(kegg_find_results[1])
                a['get_URL'] = kegg_find_results[1]
                a['D_number'] = kegg_find_results[2]
                a['Target'] = kegg_get_results[0]
                a['Pathway'] = kegg_get_results[1]
                a['Classes'] = kegg_get_results[2]
                drug['KEGG'] = a
                drug_storage[dname] = copy.deepcopy(drug)
                continue
            except Exception as e1:
                print(e1)  
                #print("\ncatch 0!", drug['drug_name'])
                pass
                #print("case id:", reportID)
                #print(KEGG_find_base + drug['drug_name'])
                #print("concept id:", drug['drug_concept_id'])
            # try removing unnecessary trailing s
            if drug['drug_name'][-1] == 's':
                try:
                    fix1 = drug['drug_name']
                    fix1 = fix1[:-1]
                    #print(fix1)
                    kegg_find_results = KEGG_find_query(fix1)
                    kegg_get_results = KEGG_get_query(kegg_find_results[1])
                    a['get_URL'] = kegg_find_results[1]
                    a['D_number'] = kegg_find_results[2]
                    a['Target'] = kegg_get_results[0]
                    a['Pathway'] = kegg_get_results[1]
                    a['Classes'] = kegg_get_results[2]
                    drug['KEGG'] = a
                    drug_storage[dname] = copy.deepcopy(drug)
                    #print("fixed by removing s:", fix1)
                    continue
                except:
                    pass
            # try fix for drugs that end with product
            if drug['drug_name'].strip(" ").endswith("product"):
                try:
                    fixy = drug['drug_name'].strip(" ")
                    fixy = fixy[:-7]
                    kegg_find_results = KEGG_find_query(fixy[0])
                    kegg_get_results = KEGG_get_query(kegg_find_results[1])
                    a['get_URL'] = kegg_find_results[1]
                    a['D_number'] = kegg_find_results[2]
                    a['Target'] = kegg_get_results[0]
                    a['Pathway'] = kegg_get_results[1]
                    a['Classes'] = kegg_get_results[2]
                    drug['KEGG'] = a
                    drug_storage[dname] = copy.deepcopy(drug)
                    #print("fixed by removing ', product'")
                    continue
                except:
                    pass
            # try fix for drugs with hyphens
            try:
                fix2 = drug['drug_name'].replace("-", " ")
                kegg_find_results = KEGG_find_query(fix2)
                kegg_get_results = KEGG_get_query(kegg_find_results[1])
                a['get_URL'] = kegg_find_results[1]
                a['D_number'] = kegg_find_results[2]
                a['Target'] = kegg_get_results[0]
                a['Pathway'] = kegg_get_results[1]
                a['Classes'] = kegg_get_results[2]
                drug['KEGG'] = a
                drug_storage[dname] = copy.deepcopy(drug)
                #print("fixed by removing hypen:", fix2)
                continue
            except:
                pass
             # try fix for drugs that end with ", human"
            if drug['drug_name'].endswith(", human"):
                try:
                    fix3 = drug['drug_name'].split(",")
                    kegg_find_results = KEGG_find_query(fix3[0])
                    kegg_get_results = KEGG_get_query(kegg_find_results[1])
                    a['get_URL'] = kegg_find_results[1]
                    a['D_number'] = kegg_find_results[2]
                    a['Target'] = kegg_get_results[0]
                    a['Pathway'] = kegg_get_results[1]
                    a['Classes'] = kegg_get_results[2]
                    drug['KEGG'] = a
                    drug_storage[dname] = copy.deepcopy(drug)
                    #print("fixed by removing ', human'")
                    continue
                except:
                    pass
                # fix for vaccines with "innactivated"
                if drug['drug_name'].endswith(", inactivated"):
                    try:
                        fix3 = drug['drug_name'].split(",")
                        kegg_find_results = KEGG_find_query(fix3[0])
                        kegg_get_results = KEGG_get_query(kegg_find_results[1])
                        a['get_URL'] = kegg_find_results[1]
                        a['D_number'] = kegg_find_results[2]
                        a['Target'] = kegg_get_results[0]
                        a['Pathway'] = kegg_get_results[1]
                        a['Classes'] = kegg_get_results[2]
                        drug['KEGG'] = a
                        drug_storage[dname] = copy.deepcopy(drug)
                        #print("fixed by removing ', inactivated'")
                        continue
                    except:
                        pass
            # try fix for drugs that end with "4000"
            if drug['drug_name'].strip(" ").endswith("4000") :
                try:
                    fix3 = drug['drug_name'].strip(" ")
                    fix3 = fix3[:-4]
                    kegg_find_results = KEGG_find_query(fix3[0])
                    kegg_get_results = KEGG_get_query(kegg_find_results[1])
                    a['get_URL'] = kegg_find_results[1]
                    a['D_number'] = kegg_find_results[2]
                    a['Target'] = kegg_get_results[0]
                    a['Pathway'] = kegg_get_results[1]
                    a['Classes'] = kegg_get_results[2]
                    drug['KEGG'] = a
                    drug_storage[dname] = copy.deepcopy(drug)
                    #print("fixed by removing '4000'")
                    continue
                except:
                    pass 
            # try fix for drugs that end with ", USP"
            if drug['drug_name'].strip(" ").endswith(", USP") :
                try:
                    fix3 = drug['drug_name'].strip(" ")
                    fix3 = fix3[:-5]
                    kegg_find_results = KEGG_find_query(fix3[0])
                    kegg_get_results = KEGG_get_query(kegg_find_results[1])
                    a['get_URL'] = kegg_find_results[1]
                    a['D_number'] = kegg_find_results[2]
                    a['Target'] = kegg_get_results[0]
                    a['Pathway'] = kegg_get_results[1]
                    a['Classes'] = kegg_get_results[2]
                    drug['KEGG'] = a
                    drug_storage[dname] = copy.deepcopy(drug)
                    #print("fixed by removing ', USP'")
                    continue
                except:
                    pass
            print("No KEGG:", drug['drug_name'], "\n")
            a = None
            drug['KEGG'] = a
            drug_storage[dname] = None
    print(dcount)
    results_dict = F_KEGG_copy
    return(F_KEGG_copy)



# update dictionary with info from KEGG API requests
def AEOLUS_get_KEGG_info():
    mycase = 1
    results_dict = ID_search_hw.add_FAERS_standard_data_to_dictionary(mycase)

    results_dict_A_KEGG = copy.deepcopy(results_dict)
    for reportID in results_dict_A_KEGG:
        for drug in results_dict_A_KEGG[reportID]['drugs']:
            if type(drug['KEGG']) == dict:
                a = drug['KEGG'].copy()
            else:
                a = drug['KEGG']
            # try fixes for common problems with find request
            try:
                kegg_find_results = KEGG_find_query(drug['drug_name'])
            except:
                print("\ncatch 1!")
                print("case id:", reportID)
                print(KEGG_find_base + drug['drug_name'])
                print("concept id:", drug['drug_concept_id'])
                # catching exception with drugs with hyphens
                try:
                    # try fix for mixture drugs
                    fix1 = drug['drug_name'].split(" ")
                    print("try2:", KEGG_find_base + fix1[0] + " " + fix1[2])
                    kegg_find_results = KEGG_find_query(fix1[0] + " " + fix1[2])
                    print(kegg_find_results)
                    print("fix1: ", KEGG_find_base + fix1[0] + " " + fix1[2])
                except Exception as e0:
                    print(traceback.format_exc())
                    # try fix for drugs with hyphens
                    try:
                        print("catch 2!")
                        print("error message:", e0)
                        fix2 = drug['drug_name'].replace("-", " ")
                        kegg_find_results = KEGG_find_query(fix2)
                        print("fixed 2:", fix2)
                    except Exception as e1:
                        print(traceback.format_exc())
                        print("catch 3!")
                        print("error message:", e1)
                        print("No KEGG:", drug['drug_name'])
                        a = "No entry"
                        drug['KEGG'] = a
                        continue    
            kegg_get_results = KEGG_get_query(kegg_find_results[1])
            if type(a) == dict:
                a['get_URL'] = kegg_find_results[1]
                a['D_number'] = kegg_find_results[2]
                a['Target'] = kegg_get_results[0]
                a['Pathway'] = kegg_get_results[1]
                a['Classes'] = kegg_get_results[2]
                drug['KEGG'] = a
    results_dict = results_dict_A_KEGG
    return results_dict_A_KEGG


