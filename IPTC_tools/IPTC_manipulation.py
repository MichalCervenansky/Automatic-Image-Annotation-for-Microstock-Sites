from IPTC_tools.iptcinfo3 import IPTCInfo


def save_iterable_to_IPTC(iterable, filename):
    info = IPTCInfo(filename, force=True, inp_charset='utf8')
    info['keywords'] = list(iterable)
    info.save()

def read_from_IPTC(filename):
    info = IPTCInfo(filename, force=True, inp_charset='utf8')
    return list(info['keywords'])


def wipe_keywords(filename):
    save_iterable_to_IPTC([], filename)
