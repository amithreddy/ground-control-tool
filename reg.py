import re
match_nums= r'(?:[,]?[-+]?(\d+(\.\d+)?|(\.\d+))[,]?){3}$'


#Test for regularexpressions
"""
a= [ "1,2,3","1.1,.11,1","11,.1.2,112", "0.31,.1,1123","1,2,3,","1,2,3,4","a,b,c"]
for txt in a:
    try:
        print re.match(match_nums,txt ).group();
    except AttributeError:
        pass
"""

