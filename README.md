# PhagesDBSearch
This repository was created to facilitate the phage search process from the [phagesDB](https://phagesdb.org/) [API](https://phagesdb.org/api/schema/).
## Config Info
Change these as needed. Currently there is no integration with the config file but this functionality will be added soon!
- `SCHOOLS` contains all the institution code as specified in [this API response](https://phagesdb.org/api/institutions/).
- `HOSTS` contains the names of the target host genuses.
- `BASE_URL` is the API url. This is combined with a request ending to get the request URL.
- `COLUMNS` details the columns stored in the dataframe (and eventually the CSV). If you change this **you must** change the `phage_info` tuple accordingly.
- `PAGE_SIZE` is the max amount of entries you retrieve. A warning is printed if the page size is insufficient for one of the species.
- `FILENAME` is the name that the final CSV will have (`.csv` will be appended)
