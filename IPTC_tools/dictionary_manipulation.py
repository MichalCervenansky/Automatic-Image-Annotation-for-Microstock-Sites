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