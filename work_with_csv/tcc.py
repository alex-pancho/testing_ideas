#cloud export script by Alexander Panchenko
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import csv
from collections import OrderedDict

#skip = data[5], data[7], data[13]
#column to pars = data[9]
#parse data
def parse(data):
    result = OrderedDict()
    for row in data:
        id_, *data = map(str.strip, row)

        if len(data)<13:
            #result[id_] = data
            print ("Error in "+id_ + " string is: "+ str(data))
            data += [""] * (15-len(data))

        if data[-1] == "":
            del data[-1]

        if id_ not in result:
            result[id_] = data
            
            #parse mailing            

            rostr = str(str(str(data[9]).split('\n'))[2:-2].replace("', '",",")).split(',')
            rostr += [""] * (4-len(rostr))
            #print (len(rostr[2]),"\t",rostr[2] )
            if len(rostr[2]) > 6:
                mzip = (str(rostr[2])[-5:]).strip()
                sta = (str(rostr[2])[1:3])
                rostr.insert(2, sta)
                rostr.insert(3, mzip)

            # if zip n/a insert "10000"  you can change this    
            if rostr[3] == "[n/a]":
                rostr.insert(3, "")

            #for Name Famname PREFFERNAME formating
            data[0] = (data[0].title())
            data[1] = (data[1].title())
            data[2] = (data[2].upper())
            data[11] = (data[11].title())

            #skip some string
            rores = [data[0], data[1], data[2], data[3], data[4], data[6], data[8], 
            rostr[0], rostr[1].strip(), rostr[2].strip(), rostr[3], data[10], data[11], data[12]]
            #add to output
            if id_ != "ContactID":
                result[id_] = rores
                rowun = data[-3] + ', ' + data[-1] + ', ' + data[-2] 
            else:
                #add new column head name
                result[id_] = ["FirstName", "LastName", "PreferredName", "Birthday", "Email", "Occupation", "Tel", "Address", 
                "City", "County", "Postcode", "Mobile", "EnrolledBy", "EnrolledDate", "WorkshopHistory", "AccountName"]
                rowun = "DO NOT CONTACT"

            result[id_].extend([rowun])
        else:
            rowun = result[id_][-1] + ', ' + data[-3] + ', ' + data[-1] + ', ' + data[-2]
            result.update({id_:result[id_][:-1]+[rowun]})

    return result


def main():
    filename = sys.argv[1]
    print ("ToCloud export script, ver 2.31")
    # if this .csv file do:
    if (filename[-3:]) == "csv":
        
        out_fln = ("out_" + filename)
        with open(filename, 'r', encoding='utf-8', errors='ignore') as in_file:
            in_data = csv.reader(in_file)
            result = parse(in_data)
        #write to file
        with open(out_fln, 'w', newline='') as out_file:
            out_data = csv.writer(out_file, delimiter=',', quotechar='"')
            #, quoting=csv.QUOTE_NONNUMERIC
            for id_, data in result.items():
                if id_ != "ContactID":
                    out_data.writerow([id_]+list(data))
                else:
                    out_data.writerow(["DBContactID"]+list(data))

if __name__ == '__main__':
    main()
    print ("All done")