from utils import *
from mosparser import *

# print("Reading...")
# regions = get_regions()
# print("Reading end. Saving...")
# save_obj(regions, 'moscow')
# print("Saving end. Loading...")
regions = load_obj('moscow')
print("Loading end.")
region_names = list(regions.keys())[:2]
regions = {region_name: regions[region_name] for region_name in region_names}
print_regions(regions)