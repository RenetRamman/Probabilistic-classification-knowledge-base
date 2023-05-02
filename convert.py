
def convertFrom(fileName, keyes = [], whitelist = [], blacklist=[]):

    f = open(fileName)

    for i in f:
        accepted = False
        for j in whitelist:
            if (i.__contains__(j)):

                blacklisted = False
                for k in blacklist:
                    if (i.__contains__(k)): blacklisted = True
                    
                if not blacklisted:
                    if len(keyes) == 0:
                        print(i.strip("// ").strip("\n")[:-5])
                        accepted = True

                    for key in keyes:
                        if i.__contains__(key):
                            print(i.strip("// ").strip("\n")[:-5])
                            accepted = True
                            break
                if accepted:
                    accepted = False
                    break

    f.close()

# convertFrom("cnet_50k.js", keyes=["|wing", "|wheel"], whitelist=["// "], blacklist=["// class element"])
# convertFrom("cnet_50k.js", keyes=[], whitelist=["// "], blacklist=["// class element"])
# convertFrom("cnet_50k.js", keyes=["vehicle", "hasProperty"], whitelist=["// ", "/"], blacklist=["// class element"])
# convertFrom("cnet_50k.js", keyes=[], whitelist=["// "], blacklist=["// class element"])
convertFrom("quasi_50k.js", keyes=[], whitelist=["// "], blacklist=["// class element"])