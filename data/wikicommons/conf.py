FILEPATH_DUMP = 'data/commonswiki-20220801-pages-articles-multistream-index.txt'
FILEPATH_DUMP_CACHE_PDF = 'data/commonswiki-20220801-pages-articles-multistream-index-pdfs.txt'
FILEPATH_DB_PDFS = 'data/commonswiki_db.csv'
FILEPATH_CATEGORIES_PDFS = 'data/commonswiki_db_categories.csv'
FILEPATH_DOWNLOADING_ERRORS = 'data/downloading_errors.csv'
FILEPATH_PDFS = 'pdfs/'


NUMBER_OF_PROCESSORS = 16

URL_INFO_TEMPLATE = "https://commons.wikimedia.org/w/api.php?action=query&titles=[[]]&format=json&prop=categoryinfo|categories|description|fileusage|info|pageterms|imageinfo&iiprop=timestamp|metadata"
DATA_LIST_SEP = '|'
MAX_DOC_PAGES = 20.0
MAX_DOC_SIZE = 15000000.0  # 15 MB

DEFAULT_SLEEP_TIME = 0.01

CATEGORIES_KEYWORDS = {
    # based on https://adamharley.com/rvl-cdip/
    'form': {'form', 'forms'},
    'letter': {'letter'},
    'resume': {'resume', 'cv', 'curriculum'},
    'news article': {'news', 'newspaper', 'magazine'},
    'invoice': {'invoice', 'receipt', 'invoices', 'receipts'},
    'questionnaire': {'questionnaire', 'questionnaire', 'poll', 'polls'},
    'memo': {'memo', 'memorandum'},
    'handwritten': {'handwritten', 'handwriting'},
    'email': {'email', 'emails'},
    'specification': {'specification', 'product description'},
    'presentation': {'presentation'},

    # new one
    'report': {'report', 'reports'},
    'leaflet': {'leaflet', 'flyer', 'brochure', 'leaflets', 'flyers', 'brochures'},
    'infographic': {'infographic', 'infographics'},
    'poster': {'poster', 'posters'},
    'health': {'health', 'medical'},
    'certificate': {'certificate'},
    # Ł
    'order': {'executive order', 'judge order', 'staff order', 'court order'},
    'meeting detail': {'meeting agenda', 'executive meeting', 'committee meeting', 'board meeting'},
    'legal agreement': {'lease agreement', 'signed agreement', 'signed settlement', 'settlement agreement', 'lawsuit settlement', 'collaboration agreement', 'grant agreement', 'merger agreement'},
    'sheet': {'summary sheet', 'data sheet', 'court sheet', 'information sheet'},
    'manual': {'instruction manual', 'repair manual', 'user manual'},
    'diploma': {'diploma'},
    'payment': {'payment required', 'payment request'},
    'request': {'request'},
    'application': {'application redacted', 'application for', 'application form'},
}
