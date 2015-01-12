import re
match_nums= r'(?:[,]?[-+]?(\d+(\.\d+)?|(\.\d+))[,]?){3}$'

a= [ "1,2,3", "0.31,.1,1123","1,2,3,","1,2,3,4","a,b,c"]
for txt in a:
    try:
        print re.match(match_nums,txt ).group();
    except AttributeError:
        pass
