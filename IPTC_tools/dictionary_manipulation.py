def build_dic(file):
    with open(file) as f:
        dictionary = dict()
        first_file = [line.rstrip() for line in f]
        for line in first_file:
            name_keywords = line.split(":")
            keyword_set = set(name_keywords[1].split(";"))
            keyword_set.remove('')
            dictionary[name_keywords[0]] = keyword_set
    return dictionary


def write_dic(dic, output_filename):
    with open(output_filename, "w") as f:
        for key in dic.keys():
            stringBuilder = key + ":"
            if isinstance(dic[key], set):
                for keyword in dic[key]:
                    stringBuilder += keyword + ";"
            elif isinstance(dic[key], int):
                stringBuilder += str(dic[key])
            else:
                raise ValueError("Unknown value of dic")
            stringBuilder += "\n"
            f.write(stringBuilder)
