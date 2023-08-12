# PatentsView data scraper
The following is the recommended order of Python files that you should run to get all the data from PatentsView repository.

1. fetch_patentsView_ids.ipynb needs asci_aap_dataJSON.json to create patentsView_failed_queries.json and patentsView_final_ids.json
2. fetch_patentsView_works.ipynb needs patentsView_final_ids.json to create patentsView_final_works.json and patentsView_failed_work_queries.json
