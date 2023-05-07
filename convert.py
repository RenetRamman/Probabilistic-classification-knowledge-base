import argparse

parser = argparse.ArgumentParser(description="Program used to extract object|property|value triples from knowledge bases", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("src", help="file name of the input knowledge base")
parser.add_argument("-b", "--blacklist", help="blacklisted phrases, rules containing these phrases will be ignored", action="append")
parser.add_argument("-w", "--whitelist", help="whitelisted phrases, rules containing at least one whitelisted phrase and no blacklisted phrases will be printed", action="append")
args = parser.parse_args()
# print(args)

def convertFrom(fileName, whitelist = [], blacklist=[]):

    f = open(fileName)

    for i in f:
        accepted = False
        for j in whitelist:
            if (i.__contains__(j)):

                blacklisted = False
                for k in blacklist:
                    if (i.__contains__(k)): blacklisted = True
                    
                if not blacklisted:
                    print(i.strip("// ").strip("\n")[:-5])
                    accepted = True

                if accepted:
                    accepted = False
                    break

    f.close()

# convertFrom("cnet_50k.js", keyes=["|wing", "|wheel"], whitelist=["// "], blacklist=["// class element"])
# convertFrom("cnet_50k.js", keyes=[], whitelist=["// "], blacklist=["// class element"])
# convertFrom("cnet_50k.js", keyes=["vehicle", "hasProperty"], whitelist=["// ", "/"], blacklist=["// class element"])
# convertFrom("cnet_50k.js", keyes=[], whitelist=["// "], blacklist=["// class element"])
convertFrom(args.src, whitelist=args.whitelist, blacklist=args.blacklist)