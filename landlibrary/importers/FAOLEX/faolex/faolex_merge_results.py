def mangle(s):
    return s.strip()[1:-1]
def cat_json(outfile, infiles):
    file(outfile, "w")\
        .write("[%s]" % (",".join([mangle(file(f).read()) for f in infiles])))

infiles = ['results/all-results+P+1800+2018.json',
           'results/all-results+L+1800+1985.json', 
           'results/all-results+L+1986+2018.json',
           'results/all-results+R+1800+1985.json', 
           'results/all-results+R+1986+2018.json',
           'results/all-results+A+1800+2018.json',
           'results/all-results+M+1800+2018.json']
cat_json("ALL-1800+2018.json", infiles)
    