import requests
import pandas as pd

SCHOOLS = ["LEHI", "UNTD", "USFL", "CHAT"]
HOSTS = ["Gordonia", "Streptomyces"]
BASE_URL = 'https://phagesdb.org/api/'
COLUMNS = ['Phage', 'Species', 'Institution']
FILENAME = 'phages_by_institution'
PAGE_SIZE = 3000

def get_request(request_ending):
  url = BASE_URL + request_ending
  headers = {'Accept': 'application/json', 'X-CSRFToken': 'ShHZqkZD3ry8Rn7vpL04wG1GbBGoOKJ0klRI5I0nO8sP198YXktFVKIfEZDBhkKb'}
  r = requests.get(url, headers=headers)
  return r.json()

def refine(results, species):
  count = int(results['count'])
  print(f"Refining results for {species}")
  if PAGE_SIZE < count:
    print(f"WARNING: results for {species} may be truncated")
    print(f"Result size {count} greater than {PAGE_SIZE}")
  out = []
  for r in results['results']:
    if r['p_institution'] and r['p_institution']['institution_code'] in SCHOOLS:
      phage_info = (r['phage_name'], species, r['p_institution']['institution_name'])
      out.append(phage_info)
  return out

def instantiate_dict():
  results = get_request('host_species')
  species_dict = dict()
  for r in results:
    if r['genus'] in HOSTS:
      species = f"{r['genus']} {r['species_name']}"
      species_dict[species] = r['id']
  return species_dict

def populate_dataframe(species_dict):
  phage_info = pd.DataFrame(columns=COLUMNS)
  for s in species_dict:
    subdir = f'host_species/{species_dict[s]}/phagelist/?page=1&page_size={PAGE_SIZE}'
    results = get_request(subdir)
    data = refine(results, s)
    phage_info_species = pd.DataFrame(data,columns=COLUMNS)
    phage_info = pd.concat([phage_info, phage_info_species])
  return phage_info

if __name__=='__main__':
  species_dict = instantiate_dict()
  phage_info = populate_dataframe(species_dict)
  phage_info.sort_values('Phage', inplace=True, ignore_index=True)

  #---- For Debug Info ---#
  print(phage_info.head(10))
  print(f"\nNumber of entries: {phage_info.size}")

  phage_info.to_csv(f'{FILENAME}.csv', index=False, header=True)
