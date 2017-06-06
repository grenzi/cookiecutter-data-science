def dfColFinder(df, findme):
    return [k for k in df.columns if findme.lower() in k.lower()]

def dfSize(df):
    size_bytes = df.values.nbytes + df.index.nbytes + df.columns.nbytes
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def dfChecker(df):
    yield ("Dataframe occupies {} for {} rows".format(dfSize(df), len(df)))
    # find and warn on any all null columns
    nullcols = df.columns[df.isnull().any()].tolist()

    if (len(nullcols) > 0):
        for x in nullcols:
            yield ("Column with some NULLs: {}".format(x))

    onevals = [x for x in df.columns if len(df[x].value_counts()) == 1]
    if (len(onevals) > 0):
        yield("Columns with only one value: {}".format("\n".join(onevals)))

    nondates = [x for x in df.columns if (('date' in x) or ('Date' in x)) and str(df[x].dtype) != 'datetime64[ns]']
    if (len(nondates) > 0):
        yield("Possible missed date types: {}".format("\n".join(nondates)))


def dfColsToCat(df, cols):
    for col in cols:
        df[col]=df[col].astype('category')

def dfNanCounter(df):
    v = []
    for x in df.columns:
        v.append({'column' : x, 'null count':sum(pd.isnull(df[x])) })
    return(pd.DataFrame(v))
