# path related
RESULTS_FOLDER = "results"
RAW_DATA_FOLDER = "raw_data"
MAIN_DATA_CSV = "data.json"
DLPB_DATA_XML = "dblp.xml"
DLPB_DATA_URL = "https://dblp.uni-trier.de/xml/dblp.xml.gz"
DLPB_DATA_URL_DTD = "https://dblp.uni-trier.de/xml/dblp.dtd"
DLPB_DATA_ZIP = "dblp.xml.gz"
DLPB_DATA_DTD = "dblp.dtd"
FUNC_DATA_JSON = "profile_author_journal_dist_sr_1_c_5_r2_0.3.json"
JOURNALS_CSV = "my_journals3.csv"
CONFERENCES_CSV="conferences.csv"
JOURNALS_METRICS_CSV="home_journals_sjrq_jifq.csv"
H_INDEX_CSV="authors_hindex_all.csv"
H_INDEX_NUM_HV_CSV= "authors_hindex_num_hv.csv"
H_INDEX_NUM_PAPERS_VENUE_TYPE_RANK_CSV="authors_num_papers_hindex_type_hv_with_metrics_clean.csv"
RANKS_DIST_CSV="ranks_dist.csv"



# parse related
DLPB_TYPES = ["journal", "booktitle"]
DLPB_TYPES_LINE_END = ["</article>", "</inproceedings>"]
DLPB_TOO_LARGE_MEMORY = 250
CLUSTER_X_LENGTH = 20

# prints related
DLPB_PARSE_PRINT_EACH = 100000
