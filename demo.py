from utils import *
from mosparser import *

# regions = get_regions()
# save_obj(regions, 'moscow')
regions = load_obj('moscow')


# Вывести данные по двум районам
region_names = list(regions.keys())[:2]
regions = {region_name: regions[region_name] for region_name in region_names}
print_regions(regions)
