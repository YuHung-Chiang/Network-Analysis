def getType1 (data):
    for d in list(data):
        if len((data[d])["rumours"])>0 and len((data[d])["non_rumours"])>0:
            continue
        else:
            data.pop(d)

    return data