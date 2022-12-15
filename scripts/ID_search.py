import requests
import pandas as pd
import datetime
import copy
import random
from subprocess import PIPE, Popen


# are we using AEOLUS or FAERS_standard?
aeolus = 0
FAERS_std = 1
safetyreportid_list = []

country_list = ["BE", "FR", "DE", "NL", "GB", "PL", "ES", "CH"]
            

'''
# rate limiting is important to avoid accidental service abuse of the OpenFDA API provider
from ratelimit import limits, sleep_and_retry


# cache API calls in a sqllite file to reduce the number of requests to openfda server
import requests_cache
requests_cache.install_cache('openfda_cache')

OPENFDA_API = "https://api.fda.gov/drug/event.json"

@sleep_and_retry
@limits(calls=40, period=60)
def call_api(params):
    """
    OpenFDA API call. Respects rate limit. Overrides default data limit
    Input: dictionary with API parameters {search: '...', count: '...'}
    Output: nested dictionary representation of the JSON results section
    
    OpenFDA API rate limits:
         With no API key: 40 requests per minute, per IP address. 1000 requests per day, per IP address.
         With an API key: 240 requests per minute, per key. 120000 requests per day, per key.
    """
    if not params:
        params = {}
    params['limit'] = params.get('limit', 1000)
    response = requests.get(OPENFDA_API, params=params)
    
    print(response.url)

    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return response.json()['results']

OPENFDA_METADATA_YAML = "https://open.fda.gov/fields/drugevent.yaml"
# munch is a yaml parser with javascript-style object access
from munch import Munch

def api_meta():
    """
    YAML file with field description and other metadata retrieved from the OpenFDA website
    Parses YAML file and provides syntactic sugar for accessing nested dictionaries
    Example: .patient.properties.patientagegroup.possible_values.value
    Note: reserved words, such as count and items still have to be accessed via ['count'], ['items']
    """
    response = requests.get(OPENFDA_METADATA_YAML)
    if response.status_code != 200:
        raise Exception('Could not retrieve YAML file with drug event API fields')
    y = Munch.fromYAML(response.text)
    return y['properties']

# API key that I got from FAERS site
columbia_api_key = 'Og4jAa0KIhPJkiwaxXVD6VHp3DGqoQf37JFPeRct'


#start_date = '20110701'
#end_date = '20110704'

#start_date = input("Enter the beginning of your desired date range (YYMMDDDD): " )
#end_date = input("Enter the end of your desired date range (YYMMDDDD): ")

#country_list = input("Enter the countries you would like to limit your search to: ")
#country_list = ["FR", "DE", "ES", "IT","CH"]


# cluster get_dates function
def get_dates_cluser():
    if FAERS_std == 1:
        #date_range = get_dates('20190623', '20190628')
        #date_range = get_dates('20110702', '20110703')
        start_date = datetime.date(2019, 6, 23)
        end_date = datetime.date(2022, 6, 28)
        d_range = []
        current_date = start_date
        while current_date <= end_date:
            d_range.append(current_date)
            current_date += datetime.timedelta(days=1)
        return d_range
'''

def get_dates(strt_dt, end_dt):
    # create a range of all dates between start and end date
    my_range = pd.date_range(start=strt_dt, end=end_dt)
    f_range = []
    for dt in my_range:
        y = str(dt)[0:4]
        m = str(dt)[5:7]
        d = str(dt)[8:10]
        new_dt = y + m + d
        f_range.append(new_dt)
    return f_range


# list of dates to limit search to
#date_range = get_dates(start_date, end_date)
#print(date_range)

'''
# strings that go in the URL of the API query


# test strings for API query search fields
#date_query = 'patient.summary.narrativeincludeclinical:('
#d_sub = '"CASE EVENT DATE:'

# add each date in range to date_query
#date_ind = 0
#num_dates = len(date_range)
#for ymd in date_range:
#    date_ind += 1
#   if date_ind < num_dates:
#        date_query += d_sub + ymd + '"' + " OR "
#    else:
#        date_query += d_sub + ymd + '"' + ")"


# potential search query terms to add to API query
#country_query = 'primarysource.reportercountry:"FR"'
#country_query = '(primarysource.reportercountry:"FR" OR occurcountry:"FR" OR primarysourcecountry:"FR")'
#country_query = 'primarysource.reportercountry:("FR" OR "DE" OR "ES" OR "IT" OR "CH")'
#country_query = 'occurcountry:("FR" OR "DE" OR "ES" OR "IT" OR "CH")'
#reaction_query = 'patient.reaction.reactionmeddrapt:("Heat exhaustion" OR "Heat stroke")'

# get an api response with the given search query terms


test_out = call_api({
    'limit': 5,
    'api_key': columbia_api_key,
    'search': 'transmissiondate:[20040101 TO 20150630]' + ' AND ' + reaction_query
    #'search': 'transmissiondate:[20040101 TO 20150630]' + ' AND ' + country_query + ' AND ' + date_query
    #'search': 'transmissiondate:[20150630 TO 20150730]' + ' AND ' + country_query
    #'search': country_query + ' AND ' + date_query
    #'search': 'safetyreportid:10332098'

})

# iterate through each entry, store safetyreportid
def get_safetyreportids(api_results):
    write_obj = open('text_files/results.txt', 'w')
    write_obj.close()
    results_obj = open('text_files/results.txt', 'a')
    for entry in api_results:
        # safetyreportid
        results_obj.write("report ID: ")
        results_obj.write(str(entry['safetyreportid']) + "\n")
        safetyreportid_list.append(str(entry['safetyreportid']))

        # reportercountry
        results_obj.write("\treportercountry: " + str(entry['primarysource']['reportercountry']) + "\n")

        # sex
        if 'patientsex' in entry['patient']:
            results_obj.write("\tsex: " + str(entry['patient']['patientsex']) + "\n")

        # date
        if 'summary' in entry['patient']:
            results_obj.write("\t" + str(entry['patient']['summary']['narrativeincludeclinical']) + "\n")
    results_obj.close()
    
get_safetyreportids(test_out)
'''
# dictionary templates

# template for KEGG value
KEGG_template = {"get_URL": None, "D_number": None, "Classes": None, "Target": None, "Pathway": None }  

if aeolus == 1:
    # template for a drug value
    drug_template = { "drug_concept_id": None, "drug_name": None, "role_cod": None, "KEGG": KEGG_template.copy()}
    # template for a primaryid value
    pid_template = {'reactions_SNOMED': None, 'reactions_MedDRA': None, 'drugs': []}

if FAERS_std == 1:
    # template for a drug value
    drug_template = { "drug_concept_id": None, "drug_name": None, "KEGG": KEGG_template.copy()}
    # template for a primaryid value
    pid_template = { 'reactions_MedDRA': None, 'drugs': []}



# get lines in given file that match certain strings
# used to search standard_case_drug, standard_case_outcome.tsv, or RxNorm CONCEPT.csv
def AEOLUS_generate_lines_that_equal(string, fp, case):
    # iterate through each line in the given file
    yielded = set() # for ensuring only non-duplicate drug concepts ids are yielded
    for line in fp:
        # if there is a match
        if line.startswith(string):
            # split line by tabs
            line_2 = line.strip("\n")
            tab_split = line_2.split('\t')
            # get the last column (concept id) and second to last column (role_cod)
            # non-duplicate drug concepts
            if case == 0:
                return_col0 = tab_split[(len(tab_split)-1)]
                # role_cod
                return_col1 = tab_split[3]
                # ensure no duplicates
                if tuple([return_col0, return_col1]) in yielded:
                    continue
                yield [return_col0, return_col1]
                yielded.add(tuple([return_col0, return_col1]))
            # RxNorm drug names
            elif case == 1:
                return_col0 = tab_split[1]
                yield return_col0
            # SNOMED and MedDRA pt outcome concepts from standard_case_outcome
            elif case == 2:
                # SNOMED code
                return_col0 = tab_split[(len(tab_split)-1)]
                # MedDRA pt
                return_col1 = tab_split[2]
                yield [return_col0, return_col1]


# adds a drug subdictionary for each drug for each corresponding safetyreportid key in AEOLUS
def add_AEOLUS_data_to_dictionary(reportids):
    # creates a dictionary entry for each id
    A_res_dict = dict( (pid, pid_template.copy()) for pid in reportids )
    print(A_res_dict)
    # search standard_case_drug.tsv for each safetyreportid key
    # adds drug subdictionary for each drug for each report
    with open("doi_10.5061_dryad.8q0s4__v1/aeolus_v1/standard_case_drug.tsv", "r") as fp:
        for pid in A_res_dict:
            # generate a list of drug_ids associated with each safetyreportID
            for i in AEOLUS_generate_lines_that_equal(str(pid), fp, 0):
                template_copy = copy.deepcopy(drug_template)
                # assign drug_concept_ids
                template_copy['drug_concept_id'] = i[0]
                # assign role_cod (primary suspect, secondary suspect, concomitant, etc)
                template_copy['role_cod'] = i[1]
                drugs_sub_dict_copy = copy.deepcopy(A_res_dict[pid]['drugs'])
                drugs_sub_dict_copy.append(template_copy)
                A_res_dict[pid]['drugs'] = drugs_sub_dict_copy
            # go back to first line
            fp.seek(0)
    # adds outcome for each safetyreportid key by searching standard_case_outcome file
    with open("doi_10.5061_dryad.8q0s4__v1/aeolus_v1/standard_case_outcome.tsv") as fp:
        for pid in A_res_dict:
            # generate a list of MedDRA reactions and SNOMED reactions associated with each safetyreportID
            for i in AEOLUS_generate_lines_that_equal(str(pid), fp, 2):
                SNOMED_react_copy = A_res_dict[pid]['reactions_SNOMED'].copy()
                MedDRA_react_copy = A_res_dict[pid]['reactions_MedDRA'].copy()
                SNOMED_react_copy.append(i[0])
                MedDRA_react_copy.append(i[1])
                A_res_dict[pid]['reactions_SNOMED'] = SNOMED_react_copy
                A_res_dict[pid]['reactions_MedDRA'] = MedDRA_react_copy
            # go back to first line
            fp.seek(0)
    # adds drug names from RxNorm by searching drug concept IDs
    with open("RxNorm_vocab/CONCEPT.csv", "r") as fp:
        # adds drug names from RxNorm by searching drug concept IDs
        for pid in A_res_dict:
            for drug in A_res_dict[pid]['drugs']:
                d_id = drug['drug_concept_id']
                drug_name_vals = []
                # search standard_case_drug for ids
                for i in AEOLUS_generate_lines_that_equal(d_id, fp, 1):
                    drug_name_vals.append(i)
                    drug['drug_name'] = i
                # go back to first line
                fp.seek(0)
    return(A_res_dict)

    
if aeolus == 1:
    results_dict = add_AEOLUS_data_to_dictionary(safetyreportid_list)


# get primaryids in FAERS_stand files in given date
# used to search DEMOGRAPHICS.txt
def FAERS_standard_generate_primaryids(fp, case):
    date_range = get_dates(start, end)
    # iterate through each line in the given file
    # case: search DEMOGRAPHICS.txt for matching dates AND countries
    if case == 1:
        for line in fp:
            split_line = line.split("$")
            if split_line[5] in date_range and split_line[8] in country_list:
                # store primaryid, country, age, gender, date
                primaryid = split_line[1]
                #country_abbr = split_line[8]
                #age = split_line[6]
                #gender = split_line[7]
                #event_dt = split_line[5]
                #yield [primaryid, country_abbr, age, gender, event_dt]
                yield primaryid
 

# generate drug info associated with each primaryid
def FAERS_standard_generate_drugs(string_list, fp):
    # primaryid, DRUG_ID, DRUG_SEQ, PERIOD, RXAUI, DRUG
    dct = 0
    for line in fp:
        split_line = line.split("$")
        if split_line[0] in string_list:
            # store drug's name, id, role
            dct += 1
            if dct % 50 == 0:
                print(dct)
            drug_name = split_line[6].replace("\n", "")
            drug_id = split_line[1]
            i = string_list.index(split_line[0])
            yield [drug_name, drug_id, string_list[i]]
    # case: search RxNorm for drug names/ingredient

# generate reactions associated with each primaryid
def FAERS_standard_generate_reactions(string_list, fp):
    rct = 0
    for line in fp:
        split_line = line.split("$")
        if split_line[0] in string_list:
            if rct % 50 == 0:
                print("rxn", rct)
            i = string_list.index(split_line[0])
            yield [split_line[2].replace("\n", ""), string_list[i]]

# European heat waves, June 2019
start = '20190623'
end = '20190628' 
# countries =  Belgium, France, Germany, Poland, the Netherlands, Spain, Switzerland, and the United Kingdom

# get a list of entries by picking lines with matching countries
def FAERS_standard_generate_primaryids_random(path):
    with open("/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/all_countries.txt", "w") as output:
        for line in path:
            spl = line.split("$")
            if spl[8] in country_list:
                output.write(line)
    filt = open("/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/text_files/all_countries.txt").read().splitlines()
    lset = set([])
    while len(lset) < 5:
        x = random.choice(filt).split("$")
        lset.add(x[1])
        yield x[1]

# adds a drug subdictionary for each drug for each corresponding safetyreportid key in FAERS_standardized
def add_FAERS_standard_data_to_dictionary(case):
    if case == 1:
        with open("/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/FAERS_standardized/DEMOGRAPHICS.txt", "r") as fp:
            primaryid_gen = FAERS_standard_generate_primaryids_random(fp)
            primaryid_list = []
            for l in primaryid_gen:
                primaryid_list.append(l)
        F_res_dict = dict( (pid, pid_template.copy()) for pid in primaryid_list )
        #print(F_res_dict)
    elif case == 0:
        # add primaryid keys that fulfill the search criteria
        with open("/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/FAERS_standardized/DEMOGRAPHICS.txt", "r") as fp:
            # generate a list of demographic info for each primaryid that fulfills the search requirements
            primaryid_list = FAERS_standard_generate_primaryids(fp, 1)
    # generate list of drugs associated with each primaryid
    print(len(primaryid_list))
    print("starting drugs")
    with open("/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/FAERS_standardized/DRUGS_STANDARDIZED.txt", "r") as fp:
        #print("lets find drugs")
        drug_info = FAERS_standard_generate_drugs(primaryid_list, fp)
        # add info for each pid
        count = 0
        for dr in drug_info:
            drugs_copy = copy.deepcopy(F_res_dict[dr[2]]['drugs'])
            drugs_sub_dict_copy = copy.deepcopy(drug_template)
            # add info for each drug in a given pid
            drugs_sub_dict_copy['drug_name'] = dr[0]
            drugs_sub_dict_copy['drug_concept_id'] = dr[1]
            # add it to the dict
            drugs_copy.append(drugs_sub_dict_copy)
            F_res_dict[dr[2]]['drugs'] = drugs_copy
            count += 1
        print("drug count", count)
    print("drugs done")
    print("starting reactions")
    # adds outcome for each primary key by searching ADVERSE_REACTIONS.txt
    with open("/Users/loaner/Documents/GitHub/Symbolic-Methods-FAERS-Project/FAERS_standardized/ADVERSE_REACTIONS.txt") as fp:
        reaction_info = FAERS_standard_generate_reactions(primaryid_list, fp)
        # generate a list reactions for each primaryid
        tok = 0
        for react in reaction_info:
            if F_res_dict[react[1]]['reactions_MedDRA'] == None:
                reactions_list = []
            else:
                reactions_list = F_res_dict[react[1]]['reactions_MedDRA'].copy()
            reactions_list.append(react[0])
            F_res_dict[react[1]]['reactions_MedDRA'] = reactions_list
            tok += 1
            print("tok", tok)
    print("done with reactions")
    #print(F_res_dict)
    return(F_res_dict)
