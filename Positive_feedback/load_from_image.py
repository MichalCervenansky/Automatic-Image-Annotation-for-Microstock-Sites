import nltk
from iptcinfo3 import IPTCInfo
from nltk.corpus import stopwords

nltk.download('stopwords')


def PF_from_IPTC(file_path):
    IPTC = IPTCInfo(file_path, force=True, inp_charset='utf_8')
    keywords = IPTC['keywords']
    caption = IPTC['caption/abstract']
    stopWords = stopwords.words("english")
    caption = [word for word in caption.split() if word not in stopWords]
    return keywords + caption

