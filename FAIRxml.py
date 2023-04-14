# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 08:56:11 2022

This program carries out the FAIRification of the machine-readable files of key comparison data of radionuclide metrology  

@author: romain.coulon
"""
import csv
import numpy as np

Radionuclide = "Ce-139" # select the radionuclide


def readRMO(NMI):
    with open('FAIRversions/NMId.csv', mode ='r')as file:
        csvFile = csv.reader(file, delimiter=';')
        for lines in csvFile:
            if lines[0] == NMI: return lines[4]

def readROR(NMI):
    with open('FAIRversions/NMId.csv', mode ='r')as file:
        csvFile = csv.reader(file, delimiter=';')
        for lines in csvFile:
            if lines[0] == NMI: return lines[7]

fileName = Radionuclide+"_database.xml"
FAIRfileName = "FAIRversions/"+Radionuclide+"_database_FAIR.xml"

file = open(fileName, 'r')
Lines = file.readlines()

FAIRfile = open(FAIRfileName, 'w')

indexDate=[]
BIPMdate=[]
HalfLife = False
for i, line in enumerate(Lines):

    # rewrite the 1st line
    if i == 0:
        FAIRfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        lineP = line


    # rewrite the root 
    if "<all>" in line:
        """
        FAIRfile.write("<comparison xmlns:h=\"http://www.w3.org/TR/html4/\"\n")
        FAIRfile.write("xmlns:qudt=\"http://qudt.org/2.1/schema/qudt\"\n")
        FAIRfile.write("xmlns:qudtUnit=\"http://qudt.org/schema/qudt/Unit\n")
        FAIRfile.write("  xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n")
        
        FAIRfile.write("<Comparison xmlns=\"https://www.w3schools.com\"\n \
        xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n \
        xsi:schemaLocation=\"https://github.com/RomainCoulon/BIPM.RI-II--K1_database/blob/main/FAIRversions/model.xsd\">\n")
        """
        FAIRfile.write("<Comparison>\n")

    if "</all>" in line:
        FAIRfile.write("</Comparison>")

    if "<General_information type=\"dict\">" in line:
        FAIRfile.write("\t<General_information>\n")
        FAIRfile.write("\t\t<Comparison_code>BIPM.RI(II)-K1."+Radionuclide+"</Comparison_code>\n")
        FAIRfile.write("\t\t<Pilot>\n")
        FAIRfile.write("\t\t\t<Acronym>BIPM</Acronym>\n")
        FAIRfile.write("\t\t\t<ROR_indentifier>https://ror.org/055vkyj43</ROR_indentifier>\n")
        FAIRfile.write("\t\t</Pilot>\n")
    if "</General_information>" in line:
        FAIRfile.write("\t</General_information>\n")

    if "<"+Radionuclide+" type=\"dict\">" in line:
        FAIRfile.write("\t<Comparison_data>\n")

    if "Year_of_publication" in line:
        FAIRfile.write("\t\t<Release>\n")
        line_change1 = line.replace("<Year_of_publication type=\"str\"","<Year")
        line_change2 = line_change1.replace("Year_of_publication","Year")
        FAIRfile.write(line_change2)

    if "Reference_of_the_published_comparison_report" in line:
        if "href" in line:
            i1=line.find("https")
            i2=line.find("}{")
            FAIRfile.write("\t\t\t<doi>"+line[i1:i2]+"</doi>\n")
            
    if ("</key>" in lineP and "<Data_from" in line) or ("</key>" in lineP and "<key name=\"Key comparison" in line) :
        FAIRfile.write("\t\t</Release>\n")

    if "<key name=\"Key Comparison Reference Value (KCRV)\"" in line:
        i1=line.find("\">")
        i2=line.find("</")
        line_change1=line[i1+2:i2]
        i3=line_change1.find("(")
        i4=line_change1.find(")")
        value=line_change1[:i3]
        u=line_change1[i3+1:i4]
        unit=line_change1[i4+2:]
        FAIRfile.write("\t\t\t<KCRV>\n")
        FAIRfile.write("\t\t\t\t<value>"+value+"</value>\n")
        FAIRfile.write("\t\t\t\t<unit>"+unit+"</unit>\n")
        FAIRfile.write("\t\t\t\t<standard_deviation>"+u+"</standard_deviation>\n")
        FAIRfile.write("\t\t\t</KCRV>\n")

    if "<Unit type=\"str\">" in line:
        i1=line.find(">")
        i2=line.find("</U")
        unitDoE=line[i1+1:i2]

    if "<Degrees_of_Equivalence type=\"dict\">" in line and "<Reference_of_the_linked" not in lineP2:
        FAIRfile.write("\t\t\t<Degrees_of_equivalence>\n")

    if "</Degrees_of_Equivalence>" in line:
        FAIRfile.write("\t\t\t</Degrees_of_equivalence>\n")

    if "type=\"dict\">" in lineP and "<D_i type=\"float\">" in line:
        i1=lineP.find("<")
        i2=lineP.find("type")
        Lab_acronym=lineP[i1+1:i2].replace(" ","")
        i1=line.find("\">")
        i2=line.find("</D")
        DoE=line[i1+2:i2]
        FAIRfile.write("\t\t\t\t<Degree_of_equivalence>\n")
        FAIRfile.write("\t\t\t\t\t<laboratory>\n")
        FAIRfile.write("\t\t\t\t\t\t<Acronym>"+Lab_acronym+"</Acronym>\n")
        if readROR(Lab_acronym)!="":
            FAIRfile.write("\t\t\t\t\t\t<ROR>"+readROR(Lab_acronym)+"</ROR>\n")
        FAIRfile.write("\t\t\t\t\t</laboratory>\n")
        FAIRfile.write("\t\t\t\t\t<value>"+DoE+"</value>\n")
        

    if "</D_i>" in lineP and "<U_i" in line:
        i1=line.find("\">")
        i2=line.find("</U_i")
        U=line[i1+2:i2]
        
        FAIRfile.write("\t\t\t\t\t<Expanded_uncertainty>"+U+"</Expanded_uncertainty>\n")
        FAIRfile.write("\t\t\t\t\t<unit>"+unitDoE+"</unit>\n")
        FAIRfile.write("\t\t\t\t</Degree_of_equivalence>\n")

    if "<Name_of_the_linked_" in line:
        i1=line.find("str\">")
        i2=line.find("</Name")
        code = line[i1+5:i2]
        i3=line.find(".RI(II)")
        rmoOrCC=line[i1+5:i3]
        FAIRfile.write("\t\t\t<Degrees_of_equivalence>\n")
        FAIRfile.write("\t\t\t\t<linked_comparison>\n")
        FAIRfile.write("\t\t\t\t\t<Comparison_code>"+code+"</Comparison_code>\n")
        if rmoOrCC == "CCRI":
            FAIRfile.write("\t\t\t\t\t<Consultative_Committee>CCRI</Consultative_Committee>\n")
        else:
            FAIRfile.write("\t\t\t\t\t<RMO>"+rmoOrCC+"</RMO>\n")

    if "<Year_of_the_link" in line:
        i1=line.find("str\">")
        i2=line.find("</Year")
        year = line[i1+5:i2]
        FAIRfile.write("\t\t\t\t\t<Year>"+year+"</Year>\n")

    if "<Reference_of_the_linked" in line:
        if "href" in line:
            i1=line.find("https")
            i2=line.find("}{")
            FAIRfile.write("\t\t\t\t\t<doi>"+line[i1:i2]+"</doi>\n")


    if "<Unit type=" in line and "<Reference_of_the_linked" in lineP:
        FAIRfile.write("\t\t\t\t</linked_comparison>\n")


    if "<Data_from" in line and "</key>" in lineP:
        FAIRfile.write("\t</Comparison_data>\n")
        FAIRfile.write("\t<Comparison_metadata>\n")


    if "<Data_from" in line:
        i1=line.find("from_")
        i2=line.find("type")
        Lab_acronym=line[i1+5:i2-6]
        year=line[i2-5:i2-1].replace(" ","")
        FAIRfile.write("\t\t<Submission>\n")
        FAIRfile.write("\t\t\t<laboratory>\n")
        FAIRfile.write("\t\t\t\t<Acronym>"+Lab_acronym+"</Acronym>\n")
        if readROR(Lab_acronym)!="":
            FAIRfile.write("\t\t\t\t<ROR>"+readROR(Lab_acronym)+"</ROR>\n")
        FAIRfile.write("\t\t\t</laboratory>\n")
        FAIRfile.write("\t\t\t<year>"+year+"</year>\n")

    if "Date of the measurement by the BIPM international" in line:
        i1=line.find("str\">")
        i2=line.find("</key")
        date1=line[i1+5:i2]
        year=date1[-4:]
        mounth=date1[3:5]
        day=date1[:2]
        BIPMdate.append(year+"-"+mounth+"-"+day+"Z")        
        #2002-09-24Z

    if "Date_of_reference_specified_by_the_laboratory" in line:
        i1=line.find("str\">")
        i2=line.find("</Date")
        dateRef=line[i1+5:i2-3].replace(" ","T")+":00Z"
        #FAIRfile.write("\t\t\t<Laboratory_measurements>\n")
        #FAIRfile.write("\t\t\t\t<Reference_date>"+dateRef+"</Reference_date>\n")
        

    if "Half-life used by the laboratory" in line:
        i1 = line.find("laboratory /")
        i2 = line.find("type")
        unit = line[i1+12:i2-2].replace(" ","")
        if "null" not in line:
            HalfLife = True
            #FAIRfile.write("\t\t\t\t<Half-life>\n")
            if "(" in line:
                i3=line.find("(")
                i5=line.find(")")
                halfLifeValue = line[i2+11:i3]
                halfLifeUnit = unit
                halfLifeStd = line[i3+1:i5]
                #FAIRfile.write("\t\t\t\t\t<value>"+halfLifeValue+"</value>\n")
                #FAIRfile.write("\t\t\t\t\t<unit>"+halfLifeUnit+"</unit>\n")
                #FAIRfile.write("\t\t\t\t\t<standard_deviation>"+halfLifeStd+"</standard_deviation>\n")
            else:
                i4=line.find(">/key")
                halfLifeStd = False
                halfLifeValue = line[i2+11:i4-6]
                halfLifeUnit = unit
                #FAIRfile.write("\t\t\t\t\t<value>"+line[i2+11:i4-6]+"</value>\n")
                #FAIRfile.write("\t\t\t\t\t<unit>"+unit+"</unit>\n")
        else:
            HalfLife = False

    if  "Reference_for_the_decay_data_used_by_the_laboratory type=\"null\"/" in line:
        ReferenceDecayData = False
        #if HalfLife: FAIRfile.write("\t\t\t\t</Half-life>\n")
        #FAIRfile.write("\t\t\t</Laboratory_measurements>\n")
    elif "Reference_for_the_decay_data_used_by_the_laboratory" in line:
        ReferenceDecayData = True
        if "\href" in line:
            i1=line.find("http")
            i2=line.find("}{")
            DOIdecayData = line[i1:i2]
            #FAIRfile.write("\t\t\t\t\t<reference>\n")
            #FAIRfile.write("\t\t\t\t\t\t<doi>"+DOIdecayData+"</doi>\n")
            #FAIRfile.write("\t\t\t\t\t</reference>\n")
        else:
            DOIdecayData = False
            i1=line.find("type=\"str\"")
            i2=line.find("</")
            DetaildecayData = line[i1+11:i2]
            #FAIRfile.write("\t\t\t\t\t<reference>\n")
            #FAIRfile.write("\t\t\t\t\t\t<detail>"+DetaildecayData+"</detail>\n")
            #FAIRfile.write("\t\t\t\t\t</reference>\n")
        #FAIRfile.write("\t\t\t\t</Half-life>\n")
            

    if "</Data_from" in line:
        FAIRfile.write("\t\t</Submission>\n")

    if "Eligible for the Key Comparison Reference Value (KCRV)" in line:
        if "False" in line:
            FAIRfile.write("\t\t\t<inKCRV>false</inKCRV>\n")
        elif "True" in line:
            FAIRfile.write("\t\t\t<inKCRV>true</inKCRV>\n")

    if "Eligible for Degree of Equivalence (DoE)" in line:
        if "False" in line:
            FAIRfile.write("\t\t\t<DoE_valid>false</DoE_valid>\n")
        elif "True" in line:
            FAIRfile.write("\t\t\t<DoE_valid>true</DoE_valid>\n")

    if "</"+Radionuclide+">" in line:
        FAIRfile.write("\t</Comparison_metadata>\n")
    
    if "Acronym(s) of the measurement method(s" in line:
        i1=line.find("\"str\"")
        i2=line.find("</key")
        methods = line[i1+6:i2].split(", ")
    
    if "Description of the measurement method" in line:
        i1=line.find("\"str\"")
        i2=line.find("</key")
        DescriptMethod = line[i1+6:i2].split(", ")

    if "Comment(s) on the measurement method" in line:
        if "null" not in line:
            i1=line.find("\"str\"")
            i2=line.find("</key")
            CommentMethod = line[i1+6:i2].split(", ")
        else:
            CommentMethod = False

    if "Activity measured by the laboratory" in line and ("null" not in line):
        i1=line.find("y /")
        i2=line.find("type")
        unit_Ai = line[i1+3:i2-2].replace(" ","")
        i3=line.find("</key")
        Ai=line[i2+11:i3].split(", ")
        AiFlag = True
    elif "Activity measured by the laboratory" in line and ("null" in line):
        AiFlag = False

    if "<Type_A_evaluation_of_the_relative" in line and AiFlag:
        i1=line.find("type=\"str\"")
        i2=line.find("</Type_A")
        uA_Ai=line[i1+11:i2].split(", ")

    if "<Type_B_evaluation_of_the_relative" in line and AiFlag:
        i1=line.find("type=\"str\"")
        i2=line.find("</Type_B")
        uB_Ai=line[i1+11:i2].split(", ")

    if "<Combined_relative_standard_uncertainty_of_the_activity_measured_by_the_laboratory type=\"null" in line and AiFlag:
        uC_Ai = []
        for ind in range(len(uA_Ai)):
            uC_Ai.append(round(np.sqrt(float(uA_Ai[ind])**2+float(uB_Ai[ind])**2),3))
    elif "<Combined_relative_standard_uncertainty_of_the_activity_measured_by_the_laboratory type=\"str" in line and AiFlag:
        i1=line.find("type=\"str\"")
        i2=line.find("</Combined")
        uC_Ai=line[i1+6:i2].split(", ")

    if "Mass of the solution" in line:
        if "null" in line: MassFlag = False
        else:
            u_mass = []
            solutionID = []
            MassFlag = True
            i1=line.find("type=\"str\"")
            i2=line.find("</key")
            mass = line[i1+11:i2].split(", ")
            i3=line.find("tion /")
            i4=line.find("type")
            unit_mass = line[i3+6:i4-2]
            for ii_mass, i_mass in enumerate(mass):
                solutionID.append(Radionuclide+Lab_acronym+year+"-"+str(ii_mass+1))
                if "(" in i_mass:
                    i5 = i_mass.find("(")
                    i6 = i_mass.find(")")
                    u_mass.append(i_mass[i5+1:i6])
                    mass[ii_mass] = i_mass[:i5]
                else:
                    u_mass = False

    if "Density of the solution " in line:
        if "null" in line: DensityFlag = False
        else:
            u_density = []
            DensityFlag = True
            i1=line.find("type=\"str\"")
            i2=line.find("</key")
            density = line[i1+11:i2].split(", ")
            i3=line.find("tion /")
            i4=line.find("type")
            unit_density = line[i3+8:i4-3]
            for ii_density, i_density in enumerate(density):
                if "(" in i_density:
                    i5 = i_density.find("(")
                    i6 = i_density.find(")")
                    u_density.append(i_density[i5+1:i6])
                    density[ii_density] = i_density[:i5]
                else:
                    u_density = False


    def ChemID(x):
        y_smiles = False
        y_InChIKey =  False
        # Ce-135
        if x == "CeCl3":
            y_smiles = "[Cl-].[Cl-].[Cl-].[Ce+3]"
            y_InChIKey = "VYLVYHXQOHJDJL-UHFFFAOYSA-K"
        if x == "CeCl2":
            y_smiles = "[Cl-].[Cl-].[Ce]"
            y_InChIKey = "ANFLYVRDLFXAOY-UHFFFAOYSA-L"
        if x == "Ce3+":
            y_smiles = "[Ce+3]"
            y_InChIKey = "XQTIWNLDFPPCIU-UHFFFAOYSA-N"        
        if x == "Ce":
            y_smiles = "[Ce]"
            y_InChIKey = "GWXLDORMOJMVQZ-UHFFFAOYSA-N"
        if x == "HCl":
            y_smiles = "[Cl]"
            y_InChIKey = "VEXZGXHMUGYJMC-UHFFFAOYSA-N"          

        return y_smiles, y_InChIKey


    if "Chemical_composition_of_the_solution" in line:
        Carrier = False
        Solvant = False
        i1=line.find("type=\"str\"")
        i2=line.find("</Chem")
        ChemComp = line[i1+11:i2]
        if "in" in ChemComp:
            Carrier = ChemComp.split(" in ")[0]
            Solvant = ChemComp.split(" in ")[1]
        else:
            Carrier = False
            Solvant = ChemComp           
        
        CarrierSMILES, CarrierInChiKey =  ChemID(Carrier)
        SolvantSMILES, SolvantInChiKey =  ChemID(Solvant)

    if "Solvent concentration of the solution / (mol.dm-3)" in line:
        if "null" in line:
            Solvant_conc = False
        else:
            i1=line.find("\"str\"")
            i2=line.find("</key")
            Solvant_conc = line[i1+6:i2]
            i3=line.find("/ (")
            i4=line.find(")")
            Solvant_conc_unit =line[i3+3:i4]

    if "Carrier concentration of the solution" in line:
        if "null" in line:
            Carrier_conc = False
        else:
            i1=line.find("\"str\"")
            i2=line.find("</key")
            Carrier_conc = line[i1+6:i2]
            i5=Carrier_conc.find(":")
            Carrier_conc = Carrier_conc[i5+1:]
            i3=line.find("/ (")
            i4=line.find(")")
            Carrier_conc_unit =line[i3+3:i4]

    if "Relative_activity_of_impurities_contained_into_the_solution" in line:
        if "null" in line:
            impurityFlag = False
            reportedImpurity = "Not reported"
        else:
            i1 = line.find("\"str\"")
            i2 = line.find("</Rel")
            reportedImpurity = line[i1+6:i2]
            #if ":" in reportedImpurity:
            #    reportedImpurity = reportedImpurity.split(";")
            #    for iImpurity in reportedImpurity:
            #        i3=iImpurity.find(":")

    if "Number_of_the_radium_source_u" in line:
        if "null" in line:
            RaRef = False
        else:
            i1 = line.find("\"str\"")
            i2 = line.find("</Num")
            RaRef = line[i1+6:i2].split(", ")

    if "Equivalent activity measured by the SIR" in  line:
        i1 = line.find("\"str\"")
        i2 = line.find("</key")
        Ae = line[i1+6:i2].split(", ")
        i3 = line.find("SIR /")
        AeUnit = line[i3+6:i1-7]

    if "Relative standard uncertainty (SIR contribution)" in line:
        if "null" in line:
            u_SIR_Ae = False
        else:
            i1 = line.find("\"str\"")
            i2 = line.find("</key")
            u_SIR_Ae = line[i1+6:i2].split(", ")

    if  "Combined standard uncertainty of the equivalent activity" in line:
        if "null" in line:
            u_Ae = False
        else:
            i1 = line.find("\"str\"")
            i2 = line.find("</key")
            u_Ae = line[i1+6:i2].split(", ")        

    if "Status_of_the_data" in line:

        FAIRfile.write("\t\t\t<Radioactive_solutions>\n")
        for indexMass, mass_i in enumerate(mass):
            if MassFlag: 
                FAIRfile.write("\t\t\t\t<Radioactive_solution>\n")
                FAIRfile.write("\t\t\t\t\t<Solution_ID>"+solutionID[indexMass]+"</Solution_ID>\n")
                FAIRfile.write("\t\t\t\t\t<mass>\n")
                FAIRfile.write("\t\t\t\t\t\t<value>"+mass_i+"</value>\n")
                FAIRfile.write("\t\t\t\t\t\t<unit>"+unit_mass+"</unit>\n")
                if u_mass: FAIRfile.write("\t\t\t\t\t\t<standard_uncertainty>"+u_mass[indexMass]+"</standard_uncertainty>\n")
                FAIRfile.write("\t\t\t\t\t</mass>\n")

                FAIRfile.write("\t\t\t\t\t<density>\n")
                FAIRfile.write("\t\t\t\t\t\t<value>"+density[0]+"</value>\n")
                FAIRfile.write("\t\t\t\t\t\t<unit>"+unit_density+"</unit>\n")
                if u_density: FAIRfile.write("\t\t\t\t\t\t<standard_uncertainty>"+u_density[0]+"</standard_uncertainty>\n")
                FAIRfile.write("\t\t\t\t\t</density>\n")

                FAIRfile.write("\t\t\t\t\t<Chemical_composition>\n")
                FAIRfile.write("\t\t\t\t\t\t<Solvant>\n")
                if SolvantSMILES: FAIRfile.write("\t\t\t\t\t\t\t<SMILES>"+SolvantSMILES+"</SMILES>\n")
                if SolvantInChiKey: FAIRfile.write("\t\t\t\t\t\t\t<InChIKey>"+SolvantInChiKey+"</InChIKey>\n")
                if Solvant_conc:
                    FAIRfile.write("\t\t\t\t\t\t\t<Concentration>\n")
                    FAIRfile.write("\t\t\t\t\t\t\t\t<value>"+Solvant_conc+"</value>\n")
                    FAIRfile.write("\t\t\t\t\t\t\t\t<unit>"+Solvant_conc_unit+"</unit>\n")
                    FAIRfile.write("\t\t\t\t\t\t\t</Concentration>\n")
                FAIRfile.write("\t\t\t\t\t\t</Solvant>\n")
                FAIRfile.write("\t\t\t\t\t\t<Carrier>\n")
                if CarrierSMILES: FAIRfile.write("\t\t\t\t\t\t\t<SMILES>"+CarrierSMILES+"</SMILES>\n")
                if CarrierInChiKey: FAIRfile.write("\t\t\t\t\t\t\t<InChIKey>"+CarrierInChiKey+"</InChIKey>\n")
                if Carrier_conc:
                    FAIRfile.write("\t\t\t\t\t\t\t<Concentration>\n")
                    FAIRfile.write("\t\t\t\t\t\t\t\t<value>"+Carrier_conc+"</value>\n")
                    FAIRfile.write("\t\t\t\t\t\t\t\t<unit>"+Carrier_conc_unit+"</unit>\n")
                    FAIRfile.write("\t\t\t\t\t\t\t</Concentration>\n")
                FAIRfile.write("\t\t\t\t\t\t</Carrier>\n")
                FAIRfile.write("\t\t\t\t\t</Chemical_composition>\n")
                FAIRfile.write("\t\t\t\t\t<impurities>"+reportedImpurity+"</impurities>\n")
                FAIRfile.write("\t\t\t\t</Radioactive_solution>\n")
        FAIRfile.write("\t\t\t</Radioactive_solutions>\n")
        FAIRfile.write("\t\t\t<Laboratory_measurements>\n")
        for indexMeth, meth_i in enumerate(methods):
            for indexMass, mass_i in enumerate(mass):
                FAIRfile.write("\t\t\t\t<Mesurement>\n")
                FAIRfile.write("\t\t\t\t\t<Reference_date>"+dateRef+"</Reference_date>\n")
                FAIRfile.write("\t\t\t\t\t<Solution_ID>"+solutionID[indexMass]+"</Solution_ID>\n")
                if HalfLife == True:
                    FAIRfile.write("\t\t\t\t\t<Half-life>\n")
                    FAIRfile.write("\t\t\t\t\t\t<value>"+halfLifeValue+"</value>\n")
                    FAIRfile.write("\t\t\t\t\t\t<unit>"+halfLifeUnit+"</unit>\n")
                    if halfLifeStd: FAIRfile.write("\t\t\t\t\t\t<standard_deviation>"+halfLifeStd+"</standard_deviation>\n")
                    if ReferenceDecayData:
                        if DOIdecayData:
                            FAIRfile.write("\t\t\t\t\t\t<reference>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t<doi>"+DOIdecayData+"</doi>\n")
                            FAIRfile.write("\t\t\t\t\t\t</reference>\n")
                        else:
                            FAIRfile.write("\t\t\t\t\t\t<reference>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t<detail>"+DetaildecayData+"</detail>\n")
                            FAIRfile.write("\t\t\t\t\t\t</reference>\n")
                    FAIRfile.write("\t\t\t\t\t</Half-life>\n")
                FAIRfile.write("\t\t\t\t\t<Method_ID>"+meth_i+"</Method_ID>\n")
                FAIRfile.write("\t\t\t\t\t<Description>"+DescriptMethod[indexMeth]+"</Description>\n")
                if CommentMethod:
                    FAIRfile.write("\t\t\t\t\t<Comments>"+CommentMethod[0]+"</Comments>\n")
                if AiFlag:
                    FAIRfile.write("\t\t\t\t\t<Activity>\n")
                    if len(Ai) == len(methods):
                        FAIRfile.write("\t\t\t\t\t\t<value>"+str(Ai[indexMeth])+"</value>\n")
                        FAIRfile.write("\t\t\t\t\t\t<unit>"+str(unit_Ai)+"</unit>\n")
                        FAIRfile.write("\t\t\t\t\t\t<relative_standard_uncertainty_type_A>"+str(uA_Ai[indexMeth])+"</relative_standard_uncertainty_type_A>\n")
                        FAIRfile.write("\t\t\t\t\t\t<relative_standard_uncertainty_type_B>"+str(uB_Ai[indexMeth])+"</relative_standard_uncertainty_type_B>\n")
                        FAIRfile.write("\t\t\t\t\t\t<relative_standard_uncertainty_combined>"+str(uC_Ai[indexMeth])+"</relative_standard_uncertainty_combined>\n")
                    elif len(Ai) > len(methods):
                        FAIRfile.write("\t\t\t\t\t\t<value>"+str(Ai[indexMass])+"</value>\n")
                        FAIRfile.write("\t\t\t\t\t\t<unit>"+str(unit_Ai)+"</unit>\n")
                        FAIRfile.write("\t\t\t\t\t\t<relative_standard_uncertainty_type_A>"+str(uA_Ai[0])+"</relative_standard_uncertainty_type_A>\n")
                        FAIRfile.write("\t\t\t\t\t\t<relative_standard_uncertainty_type_B>"+str(uB_Ai[0])+"</relative_standard_uncertainty_type_B>\n")
                        FAIRfile.write("\t\t\t\t\t\t<relative_standard_uncertainty_combined>"+str(uC_Ai[0])+"</relative_standard_uncertainty_combined>\n")
                    else:
                        FAIRfile.write("\t\t\t\t\t\t<value>"+str(Ai[0])+"</value>\n")
                        FAIRfile.write("\t\t\t\t\t\t<unit>"+str(unit_Ai)+"</unit>\n")
                        FAIRfile.write("\t\t\t\t\t\t<relative_standard_uncertainty_type_A>"+str(uA_Ai[0])+"</relative_standard_uncertainty_type_A>\n")
                        FAIRfile.write("\t\t\t\t\t\t<relative_standard_uncertainty_type_B>"+str(uB_Ai[0])+"</relative_standard_uncertainty_type_B>\n")
                        FAIRfile.write("\t\t\t\t\t\t<relative_standard_uncertainty_combined>"+str(uC_Ai[0])+"</relative_standard_uncertainty_combined>\n")
                    FAIRfile.write("\t\t\t\t\t</Activity>\n")
                FAIRfile.write("\t\t\t\t</Mesurement>\n")
        FAIRfile.write("\t\t\t</Laboratory_measurements>\n")
        massEqAe = len(mass)==len(Ae)
        methEqAe = len(methods)==len(Ae)
        #print(RaRef, Ai, Ae, massEqAe, methEqAe)
        FAIRfile.write("\t\t\t<BIPM_measurements>\n")

        if len(Ae)==1:
            FAIRfile.write("\t\t\t\t<BIPM_measurement>\n")
            FAIRfile.write("\t\t\t\t\t<Solutions>\n")
            for sol in solutionID:
                FAIRfile.write("\t\t\t\t\t\t<Solution_ID>")
                FAIRfile.write(sol)
                FAIRfile.write("</Solution_ID>\n")
            FAIRfile.write("\t\t\t\t\t</Solutions>\n")

            FAIRfile.write("\t\t\t\t\t<Methods>\n")
            for meth in methods:
                FAIRfile.write("\t\t\t\t\t\t<Method>")
                FAIRfile.write(meth)
                FAIRfile.write("</Method>\n")
            FAIRfile.write("\t\t\t\t\t</Methods>\n")

            if RaRef:
                FAIRfile.write("\t\t\t\t\t<Reference_source>")
                FAIRfile.write(RaRef[0])
                FAIRfile.write("</Reference_source>\n")
            FAIRfile.write("\t\t\t\t\t<Equivalent_activity>\n")
            FAIRfile.write("\t\t\t\t\t\t<value>")
            FAIRfile.write(Ae[0])
            FAIRfile.write("</value>\n")
            FAIRfile.write("\t\t\t\t\t\t<unit>")
            FAIRfile.write(AeUnit)
            FAIRfile.write("</unit>\n")
            FAIRfile.write("\t\t\t\t\t\t<standard_uncertainty_combined>")
            FAIRfile.write(u_Ae[0])
            FAIRfile.write("</standard_uncertainty_combined>\n")
            if u_SIR_Ae:
                FAIRfile.write("\t\t\t\t\t\t<relative_standard_uncertainty_from_SIR>")
                FAIRfile.write(str(round(float(u_SIR_Ae[0])*1e-4,4)))
                FAIRfile.write("</relative_standard_uncertainty_from_SIR>\n")
            FAIRfile.write("\t\t\t\t\t</Equivalent_activity>\n")
            FAIRfile.write("\t\t\t\t</BIPM_measurement>\n")
        
        elif len(solutionID)>1:
            for i_sol, sol in enumerate(solutionID):
                FAIRfile.write("\t\t\t\t<BIPM_measurement>\n")
                FAIRfile.write("\t\t\t\t\t<Solutions>\n")
                FAIRfile.write("\t\t\t\t\t\t<Solution_ID>")
                FAIRfile.write(sol)
                FAIRfile.write("</Solution_ID>\n")
                FAIRfile.write("\t\t\t\t\t</Solutions>\n")
                FAIRfile.write("\t\t\t\t\t<Methods>\n")
                FAIRfile.write("\t\t\t\t\t\t<Method>")
                FAIRfile.write(methods[0])
                FAIRfile.write("</Method>\n")
                FAIRfile.write("\t\t\t\t\t</Methods>\n")
                if RaRef:
                    FAIRfile.write("\t\t\t\t\t<Reference_source>")
                    FAIRfile.write(RaRef[i_sol])
                    FAIRfile.write("</Reference_source>\n")
                FAIRfile.write("\t\t\t\t\t<Equivalent_activity>\n")
                FAIRfile.write("\t\t\t\t\t\t<value>")
                FAIRfile.write(Ae[i_sol])
                FAIRfile.write("</value>\n")
                FAIRfile.write("\t\t\t\t\t\t<unit>")
                FAIRfile.write(AeUnit)
                FAIRfile.write("</unit>\n")
                FAIRfile.write("\t\t\t\t\t\t<standard_uncertainty_combined>")
                FAIRfile.write(u_Ae[i_sol])
                FAIRfile.write("</standard_uncertainty_combined>\n")
                if u_SIR_Ae:
                   FAIRfile.write("\t\t\t\t\t\t<relative_standard_uncertainty_from_SIR>")
                   FAIRfile.write(str(round(float(u_SIR_Ae[i_sol])*1e-4,4)))
                   FAIRfile.write("</relative_standard_uncertainty_from_SIR>\n")
                FAIRfile.write("\t\t\t\t\t</Equivalent_activity>\n")
                FAIRfile.write("\t\t\t\t</BIPM_measurement>\n")

        elif len(methods)>1:
           for i_meth, meth in enumerate(methods):
                FAIRfile.write("\t\t\t\t<BIPM_measurement>\n")
                FAIRfile.write("\t\t\t\t\t<Solutions>\n")
                FAIRfile.write("\t\t\t\t\t\t<Solution_ID>")
                FAIRfile.write(solutionID[0])
                FAIRfile.write("</Solution_ID>\n")
                FAIRfile.write("\t\t\t\t\t</Solutions>\n")
                FAIRfile.write("\t\t\t\t\t<Methods>\n")
                FAIRfile.write("\t\t\t\t\t\t<Method>")
                FAIRfile.write(meth)
                FAIRfile.write("</Method>\n")
                FAIRfile.write("\t\t\t\t\t</Methods>\n")
                if RaRef:
                    FAIRfile.write("\t\t\t\t\t<Reference_source>")
                    FAIRfile.write(RaRef[0])
                    FAIRfile.write("</Reference_source>\n")
                FAIRfile.write("\t\t\t\t\t<Equivalent_activity>\n")
                FAIRfile.write("\t\t\t\t\t\t<value>")
                FAIRfile.write(Ae[i_meth])
                FAIRfile.write("</value>\n")
                FAIRfile.write("\t\t\t\t\t\t<unit>")
                FAIRfile.write(AeUnit)
                FAIRfile.write("</unit>\n")
                FAIRfile.write("\t\t\t\t\t\t<standard_uncertainty_combined>")
                FAIRfile.write(u_Ae[i_meth])
                FAIRfile.write("</standard_uncertainty_combined>\n")
                if u_SIR_Ae:
                   FAIRfile.write("\t\t\t\t\t\t<relative_standard_uncertainty_from_SIR>")
                   FAIRfile.write(str(round(float(u_SIR_Ae[0])*1e-4,4)))
                   FAIRfile.write("</relative_standard_uncertainty_from_SIR>\n")
                FAIRfile.write("\t\t\t\t\t</Equivalent_activity>\n")
                FAIRfile.write("\t\t\t\t</BIPM_measurement>\n")
        else:
            print("warning: not managed!")


        FAIRfile.write("\t\t\t</BIPM_measurements>\n")
    lineP2=lineP
    lineP=line
    

#    xmlns:bibtex "http://purl.oclc.org/NET/nknouf/ns/bibtex#"



 #   if "<key name=\"Key Comparison Reference Value (KCRV)\" type=\"str\">" in line:
 #       line_1 = "\t\t\t<QuantityKind:KCRV xmlns:QuantityKind=\"http://qudt.org/vocab/quantitykind/Activity\">\n"
 #       value = line.replace("<key name=\"Key Comparison Reference Value (KCRV)\" type=\"str\">","")
 #       for j, v in enumerate(value):
 #           if v=="(": f1=j
 #           if v==")": f2=j
 #           if v=="<": f3=j
 #       quantityValue = float(value[:f1])
 #       uncertaintyValue = int(value[f1+1:f2])
 #       unit = value[f2+2:f3]
 #       if unit == "MBq":
 #           line_2 = "\t\t\t\t<unit:MBq xmlns:unit=\"http://qudt.org/vocab/unit/MegaBQ\"> </unit:MBq xmlns:unit=\"http://qudt.org/vocab/unit/MegaBQ\">\n"
 #       else:
 #           print("unit undefined at line ", i)
 #       line_3 = "\t\t\t\t<measurmentValue type=\"float\">"+str(quantityValue)+"</YmeasurmentValue>\n"
 #       line_4 = "\t\t\t\t<stdUncertaintyUvalue type=\"float\">"+str(uncertaintyValue)+"</stdUncertaintyUvalue>\n"
 #       line_5 = "\t\t\t</QuantityKind:KCRV xmlns:QuantityKind=\"http://qudt.org/vocab/quantitykind/Activity\">\n"
 #       FAIRfile.write(line_1+line_2+line_3+line_4+line_5)
        

#    elif "<Unit type=\"str\">MBq</Unit>" in line:
#        FAIRfile.write(line.replace("<Unit type=\"str\">MBq</Unit>",   
#                                    "<unit:MBq xmlns:unit=\"http://qudt.org/vocab/unit/MegaBQ\"> </unit:MBq xmlns:unit=\"http://qudt.org/vocab/unit/MegaBQ\">"))
#    else:
#        FAIRfile.write(line)
        
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




