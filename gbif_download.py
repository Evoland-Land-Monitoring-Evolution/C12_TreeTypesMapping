from pygbif import occurrences as occ
from pygbif import species
import pandas as pd
from dotenv import load_dotenv
import time
# you need a .env file with GBIF_USER=, GBIF_PWD=, and GBIF_EMAIL= in your local folder
load_dotenv()


hierarchical_legend_path = r'HierachicalLegend.xlsx'
download_output_path = r'D:\Temp'
hlegend = pd.read_excel(hierarchical_legend_path, sheet_name='Hierarchical Legend')

# bounding box format left,bottom,right,top = min Longitude , min Latitude , max Longitude , max Latitude
# EEA 39 https://sdi.eea.europa.eu/catalogue/srv/api/records/8526ff78-b000-42e1-8360-a2fb3a51e4ac
xmin = -32.04
ymin = 22.73
xmax = 53.04
ymax = 75.54

# get taxon keys
splist = hlegend['for GBIF query'].dropna().tolist()
uklist = []
tklist = []
for sp in splist:

    query_result = species.name_backbone(sp)

    if query_result['diagnostics']['matchType']=='NONE':
        print(f'No match found for {sp}')
        continue
    else:
        if 'acceptedUsage' in query_result.keys():
            ukey = query_result['acceptedUsage']['key']
        else:
            ukey = query_result['usage']['key']
        print(f'Usage key for {sp} is {ukey}')
        uklist.append(ukey)

        tkey = query_result['classification'][-1]['key']
        print(f'Taxon key for {sp} is {tkey}')
        tklist.append(tkey)

if uklist == tklist:
    print('Usage keys and taxon keys are all equal!')
else:
    raise Exception('Difference between usage keys and taxon keys detected!')

# setup template for query
query = {"type": "and",
         "predicates": [
             {"type": "in",
              "key": "TAXON_KEY",
              "values": ["2387246","2399391","2364604"]
              },
             {"type": "isNotNull",
              "parameter": "YEAR"},
             {"type": "not",
              "predicate": {"type": "in",
                            "key": "ISSUE",
                            "values": ["RECORDED_DATE_INVALID",
                                       "TAXON_MATCH_FUZZY",
                                       "TAXON_MATCH_HIGHERRANK"]
                            }
              },
             {"type": "equals",
              "key": "HAS_COORDINATE",
              "value": "true"
             },
             {"type": "equals",
              "key": "HAS_GEOSPATIAL_ISSUE",
              "value": "false"
             },
             {"type": "greaterThanOrEquals",
              "key": "DECIMAL_LONGITUDE",
              "value": "-26"
              },
             {"type": "greaterThanOrEquals",
              "key": "DECIMAL_LATITUDE",
              "value": "25"
              },
             {"type": "lessThanOrEquals",
              "key": "DECIMAL_LONGITUDE",
              "value": "40"
              },
             {"type": "lessThanOrEquals",
              "key": "DECIMAL_LATITUDE",
              "value": "72"
              }
         ]
         }

# populate query
query['predicates'][5]['value'] = str(xmin)
query['predicates'][6]['value'] = str(ymin)
query['predicates'][7]['value'] = str(xmax)
query['predicates'][8]['value'] = str(ymax)
query['predicates'][0]['values'] = [str(key) for key in tklist]

res = occ.download(query)
# alternative way to get IDs for your downloads
# occ.download_list(user="your_user_name")
time.sleep(10)

while not occ.download_meta(key=res[0])['status'] == 'SUCCEEDED':
    print(f'Download preparation still {occ.download_meta(key=res[0])['status']}')
    time.sleep(60)

print(f'Download with ID {res[0]} is ready')
occ.download_get(res[0], path=download_output_path)
