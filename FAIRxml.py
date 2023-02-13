# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 08:56:11 2022

This program carries out the FAIRification of the machine-readable files of key comparison data of radionuclide metrology  

@author: romain.coulon
"""


fileName = "Ce-139/2022/Ce-139_database.xml"
FAIRfileName = "Ce-139/2022/Ce-139_database_FAIR.xml"

file = open(fileName, 'r')
Lines = file.readlines()

FAIRfile = open(FAIRfileName, 'w')

for i, line in enumerate(Lines):

    # rewrite the 1st line
    if i == 0:
        FAIRfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")


    # rewrite the root 
    elif "<all>" in line:
        """
        FAIRfile.write("<comparison xmlns:h=\"http://www.w3.org/TR/html4/\"\n")
        FAIRfile.write("xmlns:qudt=\"http://qudt.org/2.1/schema/qudt\"\n")
        FAIRfile.write("xmlns:qudtUnit=\"http://qudt.org/schema/qudt/Unit\n")
        FAIRfile.write("  xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n")
        """
        FAIRfile.write("<comparison>")
    elif "</all>" in line:
        FAIRfile.write("</comparison>")


"""
xmlns:bibtex "http://purl.oclc.org/NET/nknouf/ns/bibtex#"
"""


    elif "<key name=\"Key Comparison Reference Value (KCRV)\" type=\"str\">" in line:
        line_1 = "\t\t\t<QuantityKind:KCRV xmlns:QuantityKind=\"http://qudt.org/vocab/quantitykind/Activity\">\n"
        value = line.replace("<key name=\"Key Comparison Reference Value (KCRV)\" type=\"str\">","")
        for j, v in enumerate(value):
            if v=="(": f1=j
            if v==")": f2=j
            if v=="<": f3=j
        quantityValue = float(value[:f1])
        uncertaintyValue = int(value[f1+1:f2])
        unit = value[f2+2:f3]
        if unit == "MBq":
            line_2 = "\t\t\t\t<unit:MBq xmlns:unit=\"http://qudt.org/vocab/unit/MegaBQ\"> </unit:MBq xmlns:unit=\"http://qudt.org/vocab/unit/MegaBQ\">\n"
        else:
            print("unit undefined at line ", i)
        line_3 = "\t\t\t\t<measurmentValue type=\"float\">"+str(quantityValue)+"</YmeasurmentValue>\n"
        line_4 = "\t\t\t\t<stdUncertaintyUvalue type=\"float\">"+str(uncertaintyValue)+"</stdUncertaintyUvalue>\n"
        line_5 = "\t\t\t</QuantityKind:KCRV xmlns:QuantityKind=\"http://qudt.org/vocab/quantitykind/Activity\">\n"
        FAIRfile.write(line_1+line_2+line_3+line_4+line_5)
        

    elif "<Unit type=\"str\">MBq</Unit>" in line:
        FAIRfile.write(line.replace("<Unit type=\"str\">MBq</Unit>",   
                                    "<unit:MBq xmlns:unit=\"http://qudt.org/vocab/unit/MegaBQ\"> </unit:MBq xmlns:unit=\"http://qudt.org/vocab/unit/MegaBQ\">"))
    else:
        FAIRfile.write(line)
        
    # FAIRfile.write(line)

print("END.")

# import xml.etree.ElementTree as ET


# file = "Ce-139/2022/Ce-139_database.xml"
# FAIRfile = "Ce-139/2022/Ce-139_database_FAIR.xml"


# tree = ET.parse(file)
# root = tree.getroot()

# for i in root[0]:
#     print(i.tag)
#     print(i.attrib)



# for i in root[1]:
#     print(i.tag)
#     print(i.attrib)




