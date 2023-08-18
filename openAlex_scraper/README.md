# OpenAlex data scraper
The following is the recommended order of Python files that you should run to get all the data from OpenAlex repository.

1. fetch_openAlex_ids.ipynb needs asci_aap_dataJSON.json to create openAlex_failed_queries.json and openAlex_final_ids.json
2. fetch_openAlex_works.ipynb needs openAlex_final_ids.json to create openAlex_final_works.json and openAlex_failed_work_queries.json
