import lxml 

from lxml import etree

from tabulate import tabulate

import textwrap

Radionuclide = "Ce-139" # select the radionuclide
FAIRfileName = "FAIRversions/"+Radionuclide+"_database_FAIR.xml"

xml_file = lxml.etree.parse(FAIRfileName)
xml_validator = lxml.etree.XMLSchema(file="FAIRversions/model.xsd")



is_valid = xml_validator.validate(xml_file)

if is_valid == 'True' :
    output = "The xml has been validated"
else:
    output = "The xml was not validated"
    
print(output + "\n")

def validate_with_lxml(xsd_tree, xml_tree):
    table=[['Line','Error(s)']] #Output table structure
    raw=[]                        #row used to remove any duplicates
    xmlschema = xsd_tree
    try:
        xmlschema.assertValid(xml_tree)
    except lxml.etree.DocumentInvalid:
        print("Validation error(s):\n")
        for error in xmlschema.error_log:
            if error.line not in raw:
                table.append([error.line,textwrap.fill(error.message, width=60)])
                raw.append(error.line)
            
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))


validate_with_lxml(xml_validator,xml_file)