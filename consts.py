# path related
RESULTS_FOLDER = "results"
RAW_DATA_FOLDER = "raw_data"
MAIN_DATA_CSV = "data.json"
DLPB_DATA_XML = "dblp.xml"
DLPB_DATA_URL = "https://dblp.uni-trier.de/xml/dblp.xml.gz"
DLPB_DATA_URL_DTD = "https://dblp.uni-trier.de/xml/dblp.dtd"
DLPB_DATA_ZIP = "dblp.xml.gz"
DLPB_DATA_DTD = "dblp.dtd"

# parse related
DLPB_TYPES = ["journal", "booktitle"]
DLPB_TYPES_LINE_END = ["</article>", "</inproceedings>"]
DLPB_TOO_LARGE_MEMORY = 250

# prints related
DLPB_PARSE_PRINT_EACH = 100000
