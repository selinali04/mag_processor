# tag_pruners
from open alex assigned concept tags, the pruner creates a dictionary of tags, keyed on ids with values corresponding to a set of related tags(as assigned by open alex) and all concept tags one hierarchal level above the tag(current level - 1 parents of the tag). From which, concept tags are removed if neither it nor its related/hierarchal tags are referenced at least once by any of the other tags and their sets. 

clinical_trials_fetcher --> clinicalTrials.json
clinicalTrials.json --> tag_pruner_clinicalTrials.ipnyb --> clinical_trials_results.json
patentViewJSON.json --> tag_pruner_patents.ipnyb --> patent_results_notype.json

both tag pruners work fundamentally the same -- the input jsons just vary in format

next steps:
- standardize formats across APIs 

