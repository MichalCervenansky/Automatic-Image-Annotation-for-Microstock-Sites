from iptcinfo3 import IPTCInfo
from nltk.corpus import stopwords


def PF_from_IPTC(file_path):
    IPTC = IPTCInfo(file_path, force=True, inp_charset='utf_8')
    keywords = IPTC['keywords']
    caption = IPTC['caption/abstract']
    stopWords = stopwords.words("english")
    if caption is not None:
        caption = [''.join(e for e in word if e.isalnum()) for word in caption.split() if word not in stopWords]
    else:
        caption = []
    return list(keywords + caption)
