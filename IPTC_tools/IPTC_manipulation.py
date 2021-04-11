from iptcinfo3 import IPTCInfo

def save_iterable_to_IPTC(iterable, filename):
    info = IPTCInfo(filename, force=True, inp_charset='utf8')
    info['keywords'] = list(iterable)
    info.save_as(filename)