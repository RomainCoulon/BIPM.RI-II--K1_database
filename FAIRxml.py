# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 08:56:11 2022

This program carries out the FAIRification of the machine-readable files of key comparison data of radionuclide metrology  

@author: romain.coulon
"""
import csv
import numpy as np
import pandas as pd
import lxml 
from tabulate import tabulate
import textwrap
import time
import hashlib

# selection the radionuclide

Radionuclide = "Sm-153" # Valid 2024 - Draft A
# Radionuclide = "Lu-177" # Valid 2024 - Draft B
# Radionuclide = "Cs-137" #  Valid 2024 - Draft B 
# Radionuclide = "Co-57" # Valid 2024 - Draft B 
# Radionuclide = "Ga-67" # Valid 2024 - Draft A
# Radionuclide = "Ge-68" # Valid 2023 - Draft A
# Radionuclide = "Tb-161" # Valid 2023 - Draft A
# Radionuclide = "Zn-65"  # Valid 2023 - Draft B
# Radionuclide = "Na-22"  # Valid 2022 - Final
# Radionuclide = "Ce-139" # Valid 2022 - published
# Radionuclide = "Ac-225" # Valid 2022 - published
# Radionuclide = "Ag-110m" # Valid 2020 - published
# Radionuclide = "Ba-133" # Valid 2022 - published
# Radionuclide = "Cd-109"   # Valid 2020 - published
# Radionuclide = "Co-60" # Valide 2022 - published
# Radionuclide = "Cs-134" # Valid 2022 - published
# Radionuclide = "Gd-153" # Valid 2021 - published
# Radionuclide = "Ra-223" # Valid 2022 - published
# Radionuclide = "Sn-113"  # Valid 2022 - published
# Radionuclide = "Sr-85"  # Valid 2020 - published
# Radionuclide = "Tl-201"  # Valid 2020 - published
# Radionuclide = "Y-88"  # Valid 2022 - published

# select the year
yyear = "2024"

# Path = "FAIRversions/" # published version
Path = "G:/SIR_Data_Management/"+Radionuclide+"/"+yyear+"/" # draft versions



def readrmo(NMI):
    with open('FAIRversions/NMId.csv', mode ='r')as file:
        csvFile = csv.reader(file, delimiter=';')
        for lines in csvFile:
            if lines[0] == NMI: return lines[4]

def readror(NMI):
    with open('FAIRversions/NMId.csv', mode ='r')as file:
        csvFile = csv.reader(file, delimiter=';')
        for lines in csvFile:
            if lines[0] == NMI: return lines[7]
            
def readPastAcro(NMI):
    with open('FAIRversions/NMId.csv', mode ='r')as file:
        csvFile = csv.reader(file, delimiter=';')
        for lines in csvFile:
            if lines[0] == NMI: return lines[5]
            
def readSMILES(rad, x):
    with open('FAIRversions/ChemID/'+rad+'.csv', mode ='r')as file:
        csvFile = csv.reader(file, delimiter=';')
        for lines in csvFile:
            if lines[0] == x: return lines[1]
            
def readINCHIKEY(rad, x):
    with open('FAIRversions/ChemID/'+rad+'.csv', mode ='r')as file:
        csvFile = csv.reader(file, delimiter=';')
        for lines in csvFile:
            if lines[0] == x: return lines[2]
            
def readINCHI(rad, x):
    with open('FAIRversions/ChemID/'+rad+'.csv', mode ='r')as file:
        csvFile = csv.reader(file, delimiter=';')
        for lines in csvFile:
            if lines[0] == x: return lines[3]            

if Path == "FAIRversions/":
    fileName = Radionuclide+"_database.xml"
    FAIRfileName = Path+Radionuclide+"_database_FAIR.xml"
else:
    fileName = Path+Radionuclide+"_database.xml"
    FAIRfileName = Path+Radionuclide+"_database_FAIR.xml"    

file = open(fileName, 'r')
Lines = file.readlines()

FAIRfile = open(FAIRfileName, 'w')


codeLink = []
rmoOrCC = []
yearLink = []
hrefK2 = []
Lab_acronym_K2 = []
DoE_K2 = []
U_K2 = []
Lab_acronym_K2_i = []
DoE_K2_i = []
U_K2_i = []
K2refFlag = []
ref_link = []
lineP = ""
K2Flag = False
flagK2end = True
doiRelease = []


release_year_list=[]
NoKCRV_re = False
for i, line in enumerate(Lines):
    if "Year_of_publication" in line:
        i1=line.find("cation")
        i2=line.find("</Year")
        yyy = line[i1+18:i2]
        release_year_list.append(yyy)
        
    if "Reference_of_the_published_comparison_report" in line:
        if "href" in line:
            i1=line.find("https")
            i2=line.find("}{")
            doiRelease.append(line[i1:i2])

for j in range(len(release_year_list)):
    # if j >0:
    #     Lab_acronym_K2.append(Lab_acronym_K2_i)
    #     DoE_K2.append(DoE_K2_i)
    #     U_K2.append(U_K2_i)
    x=pd.read_excel("../"+Radionuclide+"/"+release_year_list[j]+"/DegreesOfEquivalence_"+Radionuclide+"_"+release_year_list[j]+".xlsx", sheet_name="DoE")
    n=x.shape[0]-1
    unit_DoE = x.columns.values[2]
    Lab_acronym_K2_i=[]
    DoE_K2_i=[]
    U_K2_i=[]
    Lab_acronym_K2_i_i=[]
    DoE_K2_i_i=[]
    U_K2_i_i=[]
    countNAN=0
    codeLink_i = []
    rmoOrCC_i = []
    yearLink_i = []
    hrefK2_i = []
    for i in range(2,n+1):

        
        if str(x.iat[i,0])=="nan":
            countNAN+=1
        if countNAN==2 and str(x.iat[i,0])=="nan":
            codeLink_i.append(str(x.iat[i,1]))  
            # print(x.iat[i,0],countNAN,release_year_list[j])
            hrefK2_i.append(str(x.iat[i,5]))
            i3=codeLink_i[-1].find("(II)")
            rmoOrCC_i.append(codeLink_i[-1][:i3])
            yearLink_i.append(codeLink_i[-1][-5:-1])
            
        if countNAN>=3 and str(x.iat[i,0])!="nan":
            Lab_acronym_K2_i_i.append(str(x.iat[i,0]))
            DoE_K2_i_i.append(str(x.iat[i,1]))
            U_K2_i_i.append(str(x.iat[i,2]))
            
        if (countNAN>3 and str(x.iat[i,0])=="nan") or i==n:
            countNAN=1
            Lab_acronym_K2_i.append(Lab_acronym_K2_i_i)
            # print(release_year_list[j], i==n, Lab_acronym_K2_i)
            DoE_K2_i.append(DoE_K2_i_i)
            U_K2_i.append(U_K2_i_i)
            if str(x.iat[i,0])=="nan":
                Lab_acronym_K2_i_i=[]
                DoE_K2_i_i=[]
                U_K2_i_i=[]
            
    codeLink.append(codeLink_i)
    rmoOrCC.append(rmoOrCC_i)
    yearLink.append(yearLink_i)
    hrefK2.append(hrefK2_i)
    Lab_acronym_K2.append(Lab_acronym_K2_i)
    DoE_K2.append(DoE_K2_i)
    U_K2.append(U_K2_i)




# for i, line in enumerate(Lines):
    
#     if "<Name_of_the_linked_" in line:
#         # Lab_acronym_K2.append(Lab_acronym_K2_i)
#         # DoE_K2.append(DoE_K2_i)
#         # U_K2.append(U_K2_i)
#         # Lab_acronym_K2_i = []
#         # DoE_K2_i = []
#         # U_K2_i = []
#         K2Flag = True
#         i1=line.find("str\">")
#         i2=line.find("</Name")
#         codeLink.append(line[i1+5:i2])
#         i3=line.find(".RI(II)")
#         rmoOrCC.append(line[i1+5:i3])
        
#     if "<year_of_the_link" in line:
#         i1=line.find("str\">")
#         i2=line.find("</year")
#         yearLink.append(line[i1+5:i2])
        
#     if "/Degrees_of_Equivalence" in line:
#         if K2Flag:
#             Lab_acronym_K2.append(Lab_acronym_K2_i)
#             DoE_K2.append(DoE_K2_i)
#             U_K2.append(U_K2_i)
#             # K2refFlag.append(K2refFlag_i)
#             # ref_link.append(ref_link_i)
#         K2Flag = False
        
#     if K2Flag:
#         if "type=\"dict\">" in lineP and "<D_i type=\"float\">" in line:
#             i1=lineP.find("<")
#             i2=lineP.find("type")
#             Lab_acronym_K2_i.append(lineP[i1+1:i2].replace(" ",""))
#             i1=line.find("\">")
#             i2=line.find("</D")
#             DoE_K2_i.append(line[i1+2:i2])
    
#         if "</D_i>" in lineP and "<U_i" in line:
#             i1=line.find("\">")
#             i2=line.find("</U_i")
#             U_K2_i.append(line[i1+2:i2])       
        
#         if "<Reference_of_the_linked" in line:
#             if "href" in line:
#                 i1=line.find("https")
#                 i2=line.find("}{")
#                 K2refFlag.append(True)
#                 ref_link.append(line[i1:i2])      


#     lineP = line





indexDate=[]
BIPMdate=[]

HalfLife = False
K2Flag = False
for i, line in enumerate(Lines):





    if "<Data_from" in line:
        i1=line.find("from_")
        i2=line.find("type")
        Lab_acronym=line[i1+5:i2-6]
        year_sub=line[i2-5:i2-1].replace(" ","")
        
        
        # FAIRfile.write("\t\t<submission>\n")
        # FAIRfile.write("\t\t\t<laboratory>\n")
        # FAIRfile.write("\t\t\t\t<Acronym>"+Lab_acronym+"</Acronym>\n")
        # if readror(Lab_acronym)!="":
        #     FAIRfile.write("\t\t\t\t<ror>"+readror(Lab_acronym)+"</ror>\n")
        # FAIRfile.write("\t\t\t</laboratory>\n")
        # FAIRfile.write("\t\t\t<year>"+year_sub+"</year>\n")

    if "Status_of_the_data" in line:
        if "Published with the linked" in line:
            linkSub = True
            i1 = line.find("comparison ")
            i2 = line.find("</Status")
            ref_link_2 = line[i1+11:i2]
        else:
            linkSub = False



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
        datejjj = line[i1+5:i2-3]
        if datejjj[-1] == " ":
            datejjj = datejjj[:-1]
        dateRef=datejjj.replace(" ","T")+":00Z"
        #FAIRfile.write("\t\t\t<laboratoryMeasurements>\n")
        #FAIRfile.write("\t\t\t\t<Reference_date>"+dateRef+"</Reference_date>\n")
        

    if "Half-life used by the laboratory" in line:
        i1 = line.find("laboratory /")
        i2 = line.find("type")
        unit = line[i1+12:i2-2].replace(" ","")
        if "null" not in line:
            HalfLife = True
            #FAIRfile.write("\t\t\t\t<Half-life>\n")
            halfLifeUnit = unit
            if halfLifeUnit == "d": halfLifeUnit="\\day"
            if halfLifeUnit == "h": halfLifeUnit="\\hour"
                           
            if "(" in line:
                i3=line.find("(")
                i5=line.find(")")
                if halfLifeUnit == "y": 
                    halfLifeValue = str(365.2425*float(line[i2+11:i3]))
                    halfLifeStd = str(365.2425*float(line[i3+1:i5]))
                    halfLifeUnit="\\day"
                else:
                    halfLifeValue = line[i2+11:i3]
                    halfLifeStd = line[i3+1:i5]
                    
                #FAIRfile.write("\t\t\t\t\t<value>"+halfLifeValue+"</value>\n")
                #FAIRfile.write("\t\t\t\t\t<unit>"+halfLifeUnit+"</unit>\n")
                #FAIRfile.write("\t\t\t\t\t<standard_deviation>"+halfLifeStd+"</standard_deviation>\n")
            else:
                i4=line.find(">/key")
                halfLifeStd = False
                if halfLifeUnit == "y": 
                    halfLifeValue = str(365.2425*float(line[i2+11:i4-6]))
                else:
                    halfLifeValue = line[i2+11:i4-6]
                #FAIRfile.write("\t\t\t\t\t<value>"+line[i2+11:i4-6]+"</value>\n")
                #FAIRfile.write("\t\t\t\t\t<unit>"+unit+"</unit>\n")
        else:
            HalfLife = False

    if  "Reference_for_the_decay_data_used_by_the_laboratory type=\"null\"/" in line:
        ReferenceDecayData = False
        #if HalfLife: FAIRfile.write("\t\t\t\t</Half-life>\n")
        #FAIRfile.write("\t\t\t</laboratoryMeasurements>\n")
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
            

    # if "</Data_from" in line:
    #     FAIRfile.write("\t\t</submission>\n")

    if "Eligible for the Key Comparison Reference Value (KCRV)" in line:
        if "false" in line:
            OK_KCRV = False
            # FAIRfile.write("\t\t\t<inKCRV>false</inKCRV>\n")
        elif "true" in line:
            OK_KCRV = True
            # FAIRfile.write("\t\t\t<inKCRV>true</inKCRV>\n")

    if "Eligible for Degree of Equivalence (DoE)" in line:
        if "false" in line:
            OK_DoE = False
            # FAIRfile.write("\t\t\t<doeValid>false</doeValid>\n")
        elif "true" in line:
            OK_DoE = True
            # FAIRfile.write("\t\t\t<doeValid>true</doeValid>\n")


    
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
        if unit_Ai == 'GBq': unit_Ai = "\\Giga\\becquerel"
        if unit_Ai == 'MBq': unit_Ai = "\\Mega\\becquerel"
        if unit_Ai == 'kBq': unit_Ai = "\\kilo\\becquerel"
        if unit_Ai == 'Bq': unit_Ai = "\\becquerel"
        
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
        LabCombUonly = False
    elif "<Combined_relative_standard_uncertainty_of_the_activity_measured_by_the_laboratory type=\"str" in line and AiFlag:
        i1=line.find("type=\"str\"")
        i2=line.find("</Combined")
        uC_Ai=line[i1+11:i2].split(", ")
        LabCombUonly = True

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
            if unit_mass == "g":
                unit_mass = "\\gram"
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
            for di in range(len(density)):
                density[di]=density[di].replace("approx. ","")            
            i3=line.find("tion /")
            i4=line.find("type")
            unit_density = line[i3+8:i4-3]
            if "g" in unit_density:
                #unit_density=unit_density.replace('g',"\gram")[0:]
                unit_density="\\gram\\centi\\metre\\tothe{-3}"
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
        
        y_smiles = readSMILES(Radionuclide, x)
        y_InChIKey = readINCHIKEY(Radionuclide, x)
        y_InChI = readINCHI(Radionuclide, x)
          
        return y_smiles, y_InChIKey, y_InChI


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
        if Carrier:
            if "and" in Carrier:
                Carrier=Carrier.replace(" ","")
                Carrier=Carrier.split("and")
            if "&" in Carrier:
                Carrier=Carrier.replace(" ","")
                Carrier=Carrier.split("&")

        
        CarrierSMILES, CarrierInChiKey, CarrierInChi =  ChemID(Carrier)
        SolvantSMILES, SolvantInChiKey, SolvantInChi =  ChemID(Solvant)

    if "Solvent concentration of the solution / (mol.dm-3)" in line:
        if "null" in line or "unknown" in line:
            Solvant_conc = False
        else:
            i1=line.find("\"str\"")
            i2=line.find("</key")
            Solvant_conc = line[i1+6:i2]
            if "," in line:
                Solvant_conc = Solvant_conc.split(",")
            if "and" in line:
                Solvant_conc = Solvant_conc.split("and")
            if "with" in line:
                Solvant_conc = Solvant_conc.split("with")
            if isinstance(Solvant_conc,list):
                Solvant=[]
                for isc in range(len(Solvant_conc)):
                    Solvant_conc[isc] = Solvant_conc[isc].replace("\si{\micro g.g^{-1}}","")
                    Solvant_conc[isc] = Solvant_conc[isc].replace("\si{\microg.g^{-1}}","")
                    i6=Solvant_conc[isc].find(":")
                    Solvant.append(Solvant_conc[isc][:i6].replace(" ",""))
                    Solvant_conc[isc]=Solvant_conc[isc][i6+1:]
                    Solvant_conc[isc]=Solvant_conc[isc].replace(" ","")
            i3=line.find("/ (")
            i4=line.find(")")
            Solvant_conc_unit =line[i3+3:i4]
            if  Solvant_conc_unit == 'mol.dm-3': Solvant_conc_unit="\\mole\\deci\\metre\\tothe{-3}"
            if "\si{\micro g.g^{-1}}" in line and (not isinstance(Solvant_conc,list)):
                Solvant_conc = Solvant_conc.replace("\si{\micro g.g^{-1}}","")
                Solvant_conc = Solvant_conc.replace(" ","")
                Solvant_conc_unit="\\micro\\gram\\gram\\tothe{-1}"

    if "Carrier concentration of the solution" in line:
        
        if isinstance(Carrier, list):
            i1=line.find("\"str\"")
            i2=line.find("</key")
            i3=line.find("/ (")
            i4=line.find(")")
            Carrier_conc_unit =line[i3+4:i4]
            if Carrier_conc_unit == 'µg.g-1': Carrier_conc_unit = "\\micro\\gram\\gram\\tothe{-1}"
            Carrier_conc = line[i1+6:i2].split(",")  
            UnknownCarConc = False
            for ci, c in enumerate(Carrier_conc):
                if "null" in line or "unknown" in line:
                    Carrier_conc = False
                else:
                    i5=c.find(":")
                    c = c[i5+1:]
                    Carrier_conc[ci]=c.replace(" ","")
        elif "null" in line or "unknown" in line:
            Carrier_conc = False
        else:
            i1=line.find("\"str\"")
            i2=line.find("</key")
            Carrier_conc = line[i1+6:i2]
            i5=Carrier_conc.find(":")
            Carrier_conc = Carrier_conc[i5+1:]
            if Carrier_conc == "?" or Carrier_conc == "-" or Carrier_conc == "none" or Carrier_conc == "N/A" or Carrier_conc == "NA":
                UnknownCarConc = True
            else:
                UnknownCarConc = False
            i3=line.find("/ (")
            i4=line.find(")")
            Carrier_conc_unit =line[i3+4:i4]
            if "(" in Carrier_conc:
                i5=Carrier_conc.find("(")
                i6=Carrier_conc.find(")")
                uCarrier_conc=Carrier_conc[i5+1:i6]
                Carrier_conc=Carrier_conc[:i5]
            else:
                uCarrier_conc=False
            if Carrier_conc_unit == 'µg.g-1': Carrier_conc_unit = "\\micro\\gram\\gram\\tothe{-1}"
        if Carrier_conc and ("or" in Carrier_conc):
            Carrier_conc = Carrier_conc.split("or")[0]
        if Carrier_conc and not isinstance(Carrier, list): Carrier_conc = Carrier_conc.replace(" ","")
        if Carrier_conc:
            if "&lt" in Carrier_conc:
                Carrier_conc = Carrier_conc.replace("&lt;","")
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
        if AeUnit == 'GBq': AeUnit = "\\giga\\becquerel"
        if AeUnit == 'MBq': AeUnit = "\\mega\\becquerel"
        if AeUnit == 'kBq': AeUnit = "\\kilo\\becquerel"
        if AeUnit == 'Bq': AeUnit = "\\becquerel"
        

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

    if ("Status_of_the_data" in line) and ("linked" in line):
        FlagK1=False
        # print(FlagK1)
    if "Status_of_the_data" in line and "BIPM.RI(II)-K1" in line:
        FlagK1=True
        # print(FlagK1)
        

    #############
    ## WRITING ##
    #############
    
    # rewrite the 1st line
    if i == 0:
        FAIRfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        lineP = line


    # rewrite the root 
    if "<all>" in line:
        # FAIRfile.write("<Comparison xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n \
        #         xsi:schemaLocation=\"https://github.com/RomainCoulon/BIPM.RI-II--K1_database/blob/main/FAIRversions/KC_model_RI_II.xsd\"\n \
        #         xmlns:dsi=\"https://ptb.de/si\">\n")
        # FAIRfile.write("<Comparison xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n \
        #         xsi:schemaLocation=\"KC_model_RI_II.xsd\"\n \
        #         xmlns:dsi=\"https://ptb.de/si\">\n")
        FAIRfile.write("<kc:comparison \n \
   xmlns:kc=\"KC_Schema\" \n \
   xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n \
   xmlns:dsi=\"https://ptb.de/si\">\n")
        
        #FAIRfile.write("<Comparison>\n")

    if "</all>" in line:
        FAIRfile.write("</kc:comparison>")
        
        
    # General info
                
    if "<General_information type=\"dict\">" in line:
        FAIRfile.write("\t<kc:generalInformation>\n")
        FAIRfile.write("\t\t<kc:comparisonCode>BIPM.RI(II)-K1."+Radionuclide+"</kc:comparisonCode>\n")
        # FAIRfile.write("\t\t<Radionuclide>\n")
        # FAIRfile.write("\t\t\t<SMILES>+"+readSMILES(Radionuclide, Radionuclide)+"</SMILES>\n")
        # FAIRfile.write("\t\t\t<InChIKey>"+readINCHIKEY(Radionuclide, Radionuclide)+"</InChIKey>\n")
        # FAIRfile.write("\t\t\t<InChI>"+readINCHI(Radionuclide, Radionuclide)+"</InChI>\n")
        # FAIRfile.write("\t\t</Radionuclide>\n")
        FAIRfile.write("\t\t<kc:serviceCategoryID>https://si-digital-framework.org/kcdb-sc/RI/RAD-1.3.1</kc:serviceCategoryID>\n")
        FAIRfile.write("\t\t<kc:siDigitalFrameworkRadionuclide>https://si-digital-framework.org/kcdb-sc/nucl/"+Radionuclide+"</kc:siDigitalFrameworkRadionuclide>\n")
        FAIRfile.write("\t\t<kc:pilot>\n")
        FAIRfile.write("\t\t\t<kc:acronym>BIPM</kc:acronym>\n")
        FAIRfile.write("\t\t\t<kc:ror>https://ror.org/055vkyj43</kc:ror>\n")
        FAIRfile.write("\t\t</kc:pilot>\n")
    if "</General_information>" in line:
        FAIRfile.write("\t</kc:generalInformation>\n")

    
    # Comparison data
    
    if "Year_of_publication" in line:
        i1=line.find("cation")
        i2=line.find("</Year")
        release_year = line[i1+18:i2]
    
    
    hrefFlag = False
    if "Reference_of_the_published_comparison_report" in line:
        if "href" in line:
            hrefFlag = True
            i1=line.find("https")
            i2=line.find("}{")
            URLrelease=line[i1:i2]
        else:
            hrefFlag = False

    if "<key name=\"Key Comparison Reference Value (KCRV)\"" in line:
        i1=line.find("\">")
        i2=line.find("</")
        line_change1=line[i1+2:i2]
        i3=line_change1.find("(")
        i4=line_change1.find(")")
        if line_change1[:3] == "not":
            valueKCRV = "not evaluated"
            uKCRV = "not evaluated"
            unitKCRV = "not applicable"
            NoKCRV_re = True
        else:
            valueKCRV=line_change1[:i3]
            uKCRV=line_change1[i3+1:i4]
            nDig_u=len(uKCRV)
            if "." in valueKCRV[-2]:
                uKCRV = uKCRV[0]+"."+uKCRV[1]
            if "." in valueKCRV[-3]:
                uKCRV = "0."+uKCRV
            # print(valueKCRV,uKCRV,valueKCRV[-nDig_u:])
            unitKCRV=line_change1[i4+2:]
            if unitKCRV == "GBq":  unit = "\\giga\\becquerel"
            if unitKCRV == "MBq":  unit = "\\mega\\becquerel"
            if unitKCRV == "kBq":  unit = "\\kilo\\becquerel"
            if unitKCRV == "Bq":  unit = "\\becquerel"
            NoKCRV_re = False
        Lab_acronym=[]
        DoE=[]
        U=[]

    if "<"+Radionuclide+" type=\"dict\">" in line:
        FAIRfile.write("\t<kc:comparisonData>\n")
        
        
    if "<Unit type=\"str\">" in line:
        i1=line.find(">")
        i2=line.find("</U")
        unitDoE=line[i1+1:i2]
        if unitDoE == "GBq":  unitDoE = "\\giga\\becquerel"
        if unitDoE == "MBq":  unitDoE = "\\mega\\becquerel"
        if unitDoE == "kBq":  unitDoE = "\\kilo\\becquerel"
        if unitDoE == "Bq":   unitDoE = "\\becquerel"
        
    if "type=\"dict\">" in lineP and ("<D_i type=\"float\">" in line or "<D_i type=\"int\">" in line):
        i1=lineP.find("<")
        i2=lineP.find("type")
        # print(lineP)
        if not(K2Flag): Lab_acronym.append(lineP[i1+1:i2].replace(" ",""))
        i1=line.find("\">")
        i2=line.find("</D")
        if not(K2Flag): DoE.append(line[i1+2:i2])

    if "</D_i>" in lineP and "<U_i" in line:
        i1=line.find("\">")
        i2=line.find("</U_i")
        if not(K2Flag): U.append(line[i1+2:i2])
        
    if "name=\"Linked comparison" in line:
        flagK2end = False
        

        # FAIRfile.write("\t\t\t\t\t<Expanded_uncertainty>"+U+"</Expanded_uncertainty>\n")
        # FAIRfile.write("\t\t\t\t\t<unit>"+unitDoE+"</unit>\n")
        # FAIRfile.write("\t\t\t\t</degreeOfEquivalence>\n")
        


    if "/Degrees_of_Equivalence" in line and flagK2end:
        FAIRfile.write("\t\t<kc:release>\n")
        indRel = release_year_list.index(release_year)
        print(doiRelease,indRel)
        FAIRfile.write("\t\t\t<kc:doi>"+doiRelease[indRel]+"</kc:doi>\n")
        if "_" in release_year:
            i3=yyy.find("_")
            release_year2=release_year[:i3-1]
        else:
            release_year2=release_year
        FAIRfile.write("\t\t\t<kc:year>"+str(release_year2)+"</kc:year>\n")
        if hrefFlag: FAIRfile.write("\t\t\t<kc:doi>"+URLrelease+"</kc:doi>\n")
        if not NoKCRV_re:
            FAIRfile.write("\t\t\t<kc:kcrv>\n")
            FAIRfile.write("\t\t\t\t<dsi:value>"+valueKCRV+"</dsi:value>\n")
            FAIRfile.write("\t\t\t\t<dsi:unit>"+unitKCRV+"</dsi:unit>\n")
            FAIRfile.write("\t\t\t\t<dsi:measurementUncertaintyUnivariate>\n")
            FAIRfile.write("\t\t\t\t\t<dsi:standardMU>\n")
            FAIRfile.write("\t\t\t\t\t\t<dsi:valueStandardMU>"+uKCRV+"</dsi:valueStandardMU>\n")
            FAIRfile.write("\t\t\t\t\t</dsi:standardMU>\n")
            FAIRfile.write("\t\t\t\t</dsi:measurementUncertaintyUnivariate>\n")
            # FAIRfile.write("\t\t\t\t<dsi:expandedUnc>\n")
            # FAIRfile.write("\t\t\t\t\t<dsi:uncertainty>"+uKCRV+"</dsi:uncertainty>\n")
            # FAIRfile.write("\t\t\t\t\t<dsi:coverageFactor>1</dsi:coverageFactor>\n")
            # FAIRfile.write("\t\t\t\t\t<dsi:coverageProbability>0.68</dsi:coverageProbability>\n")
            # FAIRfile.write("\t\t\t\t</dsi:expandedUnc>\n")
            FAIRfile.write("\t\t\t</kc:kcrv>\n")
            FAIRfile.write("\t\t\t<kc:degreesOfEquivalence>\n")
            for i, labi in enumerate(Lab_acronym):
                FAIRfile.write("\t\t\t\t<kc:degreeOfEquivalence>\n")
                FAIRfile.write("\t\t\t\t\t<kc:laboratory>\n")
                FAIRfile.write("\t\t\t\t\t\t<kc:acronym>"+labi+"</kc:acronym>\n")
                if readPastAcro(labi)!="-":
                    FAIRfile.write("\t\t\t\t\t\t<kc:pastAcronyms>"+readPastAcro(labi)+"</kc:pastAcronyms>\n")
                if readror(labi)!="":
                    FAIRfile.write("\t\t\t\t\t\t<kc:ror>"+readror(labi)+"</kc:ror>\n")
                FAIRfile.write("\t\t\t\t\t</kc:laboratory>\n")
                #FAIRfile.write("\t\t\t\t\t<value>"+DoE+"</value>\n")
                FAIRfile.write("\t\t\t\t\t<kc:result>\n")
                FAIRfile.write("\t\t\t\t\t\t<dsi:value>"+DoE[i]+"</dsi:value>\n")
                FAIRfile.write("\t\t\t\t\t\t<dsi:unit>"+unitDoE+"</dsi:unit>\n")
                FAIRfile.write("\t\t\t\t\t\t<dsi:measurementUncertaintyUnivariate>\n")
                FAIRfile.write("\t\t\t\t\t\t\t<dsi:expandedMU>\n")
                FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:valueExpandedMU>"+U[i]+"</dsi:valueExpandedMU>\n")
                FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:coverageFactor>2</dsi:coverageFactor>\n")
                FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:coverageProbability>0.95</dsi:coverageProbability>\n")
                FAIRfile.write("\t\t\t\t\t\t\t</dsi:expandedMU>\n")
                FAIRfile.write("\t\t\t\t\t\t</dsi:measurementUncertaintyUnivariate>\n")
                # FAIRfile.write("\t\t\t\t\t\t<dsi:expandedUnc>\n")
                # FAIRfile.write("\t\t\t\t\t\t\t<dsi:uncertainty>"+U[i]+"</dsi:uncertainty>\n")
                # FAIRfile.write("\t\t\t\t\t\t\t<dsi:coverageFactor>2</dsi:coverageFactor>\n")
                # FAIRfile.write("\t\t\t\t\t\t\t<dsi:coverageProbability>0.95</dsi:coverageProbability>\n")
                # FAIRfile.write("\t\t\t\t\t\t</dsi:expandedUnc>\n")
                FAIRfile.write("\t\t\t\t\t</kc:result>\n")              
                FAIRfile.write("\t\t\t\t</kc:degreeOfEquivalence>\n")
            FAIRfile.write("\t\t\t</kc:degreesOfEquivalence>\n")
        Index = release_year_list.index(release_year)
        if yearLink[Index]!=[]:
            for j in range(len(yearLink[Index])):
                 # if int(release_year)>=int(yearLink[Index][j]):# and int(release_year)-int(yearLink[Index][j])<=20:
                    FAIRfile.write("\t\t\t<kc:degreesOfEquivalence>\n")
                    FAIRfile.write("\t\t\t\t<kc:linkedComparison>\n")
                    FAIRfile.write("\t\t\t\t\t<kc:comparisonCode>"+str(codeLink[Index][j])+"</kc:comparisonCode>\n")
                    if "CCRI" in rmoOrCC[Index][j]:  FAIRfile.write("\t\t\t\t\t<kc:consultativeCommittee>CCRI(II)</kc:consultativeCommittee>\n")
                    else: FAIRfile.write("\t\t\t\t\t<kc:rmo>"+str(rmoOrCC[Index][j])+"</kc:rmo>\n")
                    FAIRfile.write("\t\t\t\t\t<kc:year>"+str(yearLink[Index][j])+"</kc:year>\n")
                    FAIRfile.write("\t\t\t\t\t<kc:doi>"+str(hrefK2[Index][j])+"</kc:doi>\n")
                    FAIRfile.write("\t\t\t\t</kc:linkedComparison>\n")
                    # if K2refFlag[j]: FAIRfile.write("\t\t\t\t\t<doi>"+str(ref_link[j])+"</doi>\n")
                    for i, labi in enumerate(Lab_acronym_K2[Index][j]):
                        FAIRfile.write("\t\t\t\t<kc:degreeOfEquivalence>\n")
                        FAIRfile.write("\t\t\t\t\t<kc:laboratory>\n")
                        FAIRfile.write("\t\t\t\t\t\t<kc:acronym>"+labi+"</kc:acronym>\n")
                        if readPastAcro(labi)!="-":
                            FAIRfile.write("\t\t\t\t\t\t<kc:pastAcronyms>"+readPastAcro(labi)+"</kc:pastAcronyms>\n")
                        if readror(labi)!="":
                            FAIRfile.write("\t\t\t\t\t\t<kc:ror>"+readror(labi)+"</kc:ror>\n")
                        FAIRfile.write("\t\t\t\t\t</kc:laboratory>\n")
                        #FAIRfile.write("\t\t\t\t\t<value>"+DoE+"</value>\n")
                        FAIRfile.write("\t\t\t\t\t<kc:result>\n")
                        FAIRfile.write("\t\t\t\t\t\t<dsi:value>"+DoE_K2[Index][j][i]+"</dsi:value>\n")
                        FAIRfile.write("\t\t\t\t\t\t<dsi:unit>"+unitDoE+"</dsi:unit>\n")
                        
                        FAIRfile.write("\t\t\t\t\t\t<dsi:measurementUncertaintyUnivariate>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t<dsi:expandedMU>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:valueExpandedMU>"+U_K2[Index][j][i]+"</dsi:valueExpandedMU>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:coverageFactor>2</dsi:coverageFactor>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:coverageProbability>0.95</dsi:coverageProbability>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t</dsi:expandedMU>\n")
                        FAIRfile.write("\t\t\t\t\t\t</dsi:measurementUncertaintyUnivariate>\n")
                        
                        # FAIRfile.write("\t\t\t\t\t\t<dsi:expandedUnc>\n")
                        # FAIRfile.write("\t\t\t\t\t\t\t<dsi:uncertainty>"+U_K2[Index][j][i]+"</dsi:uncertainty>\n")
                        # FAIRfile.write("\t\t\t\t\t\t\t<dsi:coverageFactor>2</dsi:coverageFactor>\n")
                        # FAIRfile.write("\t\t\t\t\t\t\t<dsi:coverageProbability>0.95</dsi:coverageProbability>\n")
                        # FAIRfile.write("\t\t\t\t\t\t</dsi:expandedUnc>\n")
                        
                        FAIRfile.write("\t\t\t\t\t</kc:result>\n")              
                        FAIRfile.write("\t\t\t\t</kc:degreeOfEquivalence>\n")
                    FAIRfile.write("\t\t\t</kc:degreesOfEquivalence>\n")
        FAIRfile.write("\t\t</kc:release>\n")
    # if ("</key>" in lineP and "<Data_from" in line) or ("</key>" in lineP and "<key name=\"Key comparison" in line) :
    #     FAIRfile.write("\t\t</Release>\n")




        
        
        

    # if "<Degrees_of_Equivalence type=\"dict\">" in line and "<Reference_of_the_linked" not in lineP2:
    #     FAIRfile.write("\t\t\t<Degrees_of_equivalence>\n")

    # if "</Degrees_of_Equivalence>" in line:
    #     FAIRfile.write("\t\t\t</Degrees_of_equivalence>\n")

    # if "<Name_of_the_linked_" in line:
    #     i1=line.find("str\">")
    #     i2=line.find("</Name")
    #     code = line[i1+5:i2]
    #     i3=line.find(".RI(II)")
    #     rmoOrCC=line[i1+5:i3]
    #     FAIRfile.write("\t\t\t<Degrees_of_equivalence>\n")
    #     FAIRfile.write("\t\t\t\t<linkedComparison>\n")
    #     FAIRfile.write("\t\t\t\t\t<comparisonCode>"+code+"</comparisonCode>\n")
    #     if rmoOrCC == "CCRI":
    #         FAIRfile.write("\t\t\t\t\t<consultativeCommittee>CCRI</consultativeCommittee>\n")
    #     else:
    #         FAIRfile.write("\t\t\t\t\t<rmo>"+rmoOrCC+"</rmo>\n")

    # if "<year_of_the_link" in line:
    #     i1=line.find("str\">")
    #     i2=line.find("</year")
    #     year = line[i1+5:i2]
    #     FAIRfile.write("\t\t\t\t\t<year>"+year+"</year>\n")

    # if "<Reference_of_the_linked" in line:
    #     if "href" in line:
    #         i1=line.find("https")
    #         i2=line.find("}{")
    #         FAIRfile.write("\t\t\t\t\t<doi>"+line[i1:i2]+"</doi>\n")


    # if "<Unit type=" in line and "<Reference_of_the_linked" in lineP:
    #     FAIRfile.write("\t\t\t\t</linkedComparison>\n")
    
    
    
    
  
    
    
    if "<Data_from" in line and "</key>" in lineP and "Degrees_of_Equivalence" in lineP2:
        FAIRfile.write("\t</kc:comparisonData>\n")
        FAIRfile.write("\t<kc:comparisonMetadata>\n")

    # Comparison metadata

    if "</"+Radionuclide+">" in line:
        FAIRfile.write("\t</kc:comparisonMetadata>\n")
        
    if "</Data_from" in line:
        if Lab_acronym == "NUCLEAR_MALAYSIA": Lab_acronym = Lab_acronym.replace("NUCLEAR_MALAYSIA","NUCLEAR MALAYSIA")
        FAIRfile.write("\t\t<kc:submission>\n")
        FAIRfile.write("\t\t\t<kc:laboratory>\n")
        FAIRfile.write("\t\t\t\t<kc:acronym>"+Lab_acronym+"</kc:acronym>\n")
        if readPastAcro(Lab_acronym)!="-":
            FAIRfile.write("\t\t\t\t<kc:pastAcronyms>"+readPastAcro(Lab_acronym)+"</kc:pastAcronyms>\n")
        if readror(Lab_acronym)!="":
            FAIRfile.write("\t\t\t\t<kc:ror>"+readror(Lab_acronym)+"</kc:ror>\n")
        FAIRfile.write("\t\t\t</kc:laboratory>\n")
        FAIRfile.write("\t\t\t<kc:year>"+year_sub+"</kc:year>\n")
        if OK_KCRV: FAIRfile.write("\t\t\t<kc:inKCRV>true</kc:inKCRV>\n")
        else : FAIRfile.write("\t\t\t<kc:inKCRV>false</kc:inKCRV>\n")

        if OK_DoE: FAIRfile.write("\t\t\t<kc:doeValid>true</kc:doeValid>\n")
        else: FAIRfile.write("\t\t\t<kc:doeValid>false</kc:doeValid>\n")

    # if "Status_of_the_data" in line:
        if MassFlag:
            FAIRfile.write("\t\t\t<kc:radioactiveSolutions>\n")
            for indexMass, mass_i in enumerate(mass): 
                FAIRfile.write("\t\t\t\t<kc:radioactiveSolution>\n")
                FAIRfile.write("\t\t\t\t\t<kc:solutionID>"+solutionID[indexMass]+"</kc:solutionID>\n")
                FAIRfile.write("\t\t\t\t\t<kc:mass>\n")
                # FAIRfile.write("\t\t\t\t\t\t<dsi:real>\n")
                FAIRfile.write("\t\t\t\t\t\t<dsi:value>"+mass_i+"</dsi:value>\n")
                FAIRfile.write("\t\t\t\t\t\t<dsi:unit>"+unit_mass+"</dsi:unit>\n")
                # FAIRfile.write("\t\t\t\t\t\t<value>"+mass_i+"</value>\n")
                # FAIRfile.write("\t\t\t\t\t\t<unit>"+unit_mass+"</unit>\n")
                if u_mass:
                    
                    FAIRfile.write("\t\t\t\t\t\t<dsi:measurementUncertaintyUnivariate>\n")
                    FAIRfile.write("\t\t\t\t\t\t\t<dsi:standardMU>\n")
                    FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:valueStandardMU>"+u_mass[indexMass]+"</dsi:valueStandardMU>\n")
                    FAIRfile.write("\t\t\t\t\t\t\t</dsi:standardMU>\n")
                    FAIRfile.write("\t\t\t\t\t\t</dsi:measurementUncertaintyUnivariate>\n")
                    
                    
                    # FAIRfile.write("\t\t\t\t\t\t<dsi:expandedUnc>\n")
                    # FAIRfile.write("\t\t\t\t\t\t\t<dsi:uncertainty>"+u_mass[indexMass]+"</dsi:uncertainty>\n")
                    # FAIRfile.write("\t\t\t\t\t\t\t<dsi:coverageFactor>1</dsi:coverageFactor>\n")
                    # FAIRfile.write("\t\t\t\t\t\t\t<dsi:coverageProbability>0.68</dsi:coverageProbability>\n")
                    # FAIRfile.write("\t\t\t\t\t\t</dsi:expandedUnc>\n")

                FAIRfile.write("\t\t\t\t\t</kc:mass>\n")
                if DensityFlag:
                    FAIRfile.write("\t\t\t\t\t<kc:density>\n")
                    # FAIRfile.write("\t\t\t\t\t\t<dsi:real>\n")
                    FAIRfile.write("\t\t\t\t\t\t<dsi:value>"+density[0]+"</dsi:value>\n")
                    FAIRfile.write("\t\t\t\t\t\t<dsi:unit>"+unit_density+"</dsi:unit>\n")                
                    # FAIRfile.write("\t\t\t\t\t\t<value>"+density[0]+"</value>\n")
                    # FAIRfile.write("\t\t\t\t\t\t<unit>"+unit_density+"</unit>\n")
                    if u_density:
                        FAIRfile.write("\t\t\t\t\t\t<dsi:measurementUncertaintyUnivariate>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t<dsi:standardMU>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:valueStandardMU>"+u_density[0]+"</dsi:valueStandardMU>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t</dsi:standardMU>\n")
                        FAIRfile.write("\t\t\t\t\t\t</dsi:measurementUncertaintyUnivariate>\n")
                    FAIRfile.write("\t\t\t\t\t</kc:density>\n")
    
                FAIRfile.write("\t\t\t\t\t<kc:chemicalComposition>\n")
                FAIRfile.write("\t\t\t\t\t\t<kc:solvant>\n")
                if Solvant_conc:
                    if isinstance(Solvant_conc, list):
                        # for si in range(len(Solvant_conc)):
                        #     if ChemID(Solvant[si])[0]: FAIRfile.write("\t\t\t\t\t\t\t<kc:smiles>"+ChemID(Solvant[si])[0]+"</kc:smiles>\n")
                        #     if ChemID(Solvant[si])[1]: FAIRfile.write("\t\t\t\t\t\t\t<kc:InChIKey>"+ChemID(Solvant[si])[1]+"</kc:InChIKey>\n")
                        #     if ChemID(Solvant[si])[2]: FAIRfile.write("\t\t\t\t\t\t\t<kc:InChI>"+ChemID(Solvant[si])[2]+"</kc:InChI>\n")
                        #     FAIRfile.write("\t\t\t\t\t\t\t<kc:solvantConcentration>\n")
                        #     # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:real>\n")
                        #     FAIRfile.write("\t\t\t\t\t\t\t\t\t<dsi:value>"+Solvant_conc[si]+"</dsi:value>\n")
                        #     FAIRfile.write("\t\t\t\t\t\t\t\t\t<dsi:unit>"+Solvant_conc_unit+"</dsi:unit>\n") 
                        #     # FAIRfile.write("\t\t\t\t\t\t\t\t</dsi:real>\n")
                        #     FAIRfile.write("\t\t\t\t\t\t\t</kc:solvantConcentration>\n")
                        if ChemID(Solvant[indexMass])[0]: FAIRfile.write("\t\t\t\t\t\t\t<kc:smiles>"+ChemID(Solvant[indexMass])[0]+"</kc:smiles>\n")
                        if ChemID(Solvant[indexMass])[1]: FAIRfile.write("\t\t\t\t\t\t\t<kc:InChIKey>"+ChemID(Solvant[indexMass])[1]+"</kc:InChIKey>\n")
                        if ChemID(Solvant[indexMass])[2]: FAIRfile.write("\t\t\t\t\t\t\t<kc:InChI>"+ChemID(Solvant[indexMass])[2]+"</kc:InChI>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t<kc:solvantConcentration>\n")
                        # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:real>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t\t\t<dsi:value>"+Solvant_conc[indexMass]+"</dsi:value>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t\t\t<dsi:unit>"+Solvant_conc_unit+"</dsi:unit>\n") 
                        # FAIRfile.write("\t\t\t\t\t\t\t\t</dsi:real>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t</kc:solvantConcentration>\n")
                    else:
                        if SolvantSMILES: FAIRfile.write("\t\t\t\t\t\t\t<kc:smiles>"+SolvantSMILES+"</kc:smiles>\n")
                        if SolvantInChiKey: FAIRfile.write("\t\t\t\t\t\t\t<kc:InChIKey>"+SolvantInChiKey+"</kc:InChIKey>\n")
                        if SolvantInChi: FAIRfile.write("\t\t\t\t\t\t\t<kc:InChI>"+SolvantInChi+"</kc:InChI>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t<kc:solvantConcentration>\n")
                        # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:real>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:value>"+Solvant_conc+"</dsi:value>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:unit>"+Solvant_conc_unit+"</dsi:unit>\n") 
                        # FAIRfile.write("\t\t\t\t\t\t\t\t</dsi:real>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t</kc:solvantConcentration>\n")
                FAIRfile.write("\t\t\t\t\t\t</kc:solvant>\n")

                if isinstance(Carrier, list):
                    for ci in range(len(Carrier)):
                        FAIRfile.write("\t\t\t\t\t\t<kc:carrier>\n")
                        if CarrierSMILES: FAIRfile.write("\t\t\t\t\t\t\t<kc:smiles>"+ChemID(Carrier[ci])[0]+"</kc:smiles>\n")
                        if CarrierInChiKey: FAIRfile.write("\t\t\t\t\t\t\t<kc:InChIKey>"+ChemID(Carrier[ci])[1]+"</kc:InChIKey>\n")
                        if CarrierInChi: FAIRfile.write("\t\t\t\t\t\t\t<kc:InChI>"+ChemID(Carrier[ci])[2]+"</kc:InChI>\n")
                        # print(Carrier_conc, ci)
                        if Carrier_conc and (not UnknownCarConc) and (Carrier_conc[ci]!="?"):
                            FAIRfile.write("\t\t\t\t\t\t\t<kc:carrierConcentration>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:real>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:value>"+Carrier_conc[ci]+"</dsi:value>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:unit>"+Carrier_conc_unit+"</dsi:unit>\n") 
                            # FAIRfile.write("\t\t\t\t\t\t\t\t</dsi:real>\n")                    
                            # FAIRfile.write("\t\t\t\t\t\t\t\t<value>"+Carrier_conc+"</value>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t\t<unit>"+Carrier_conc_unit+"</unit>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t</kc:carrierConcentration>\n")
                        FAIRfile.write("\t\t\t\t\t\t</kc:carrier>\n")
                else:
                    FAIRfile.write("\t\t\t\t\t\t<kc:carrier>\n")
                    if CarrierSMILES: FAIRfile.write("\t\t\t\t\t\t\t<kc:smiles>"+CarrierSMILES+"</kc:smiles>\n")
                    if CarrierInChiKey: FAIRfile.write("\t\t\t\t\t\t\t<kc:InChIKey>"+CarrierInChiKey+"</kc:InChIKey>\n")
                    if CarrierInChi: FAIRfile.write("\t\t\t\t\t\t\t<kc:InChI>"+CarrierInChi+"</kc:InChI>\n")
                    if Carrier_conc and (not UnknownCarConc):
                        FAIRfile.write("\t\t\t\t\t\t\t<kc:carrierConcentration>\n")
                        # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:real>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:value>"+Carrier_conc+"</dsi:value>\n")
                        FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:unit>"+Carrier_conc_unit+"</dsi:unit>\n")
                        if uCarrier_conc:
                            
                            FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:measurementUncertaintyUnivariate>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t\t\t<dsi:standardMU>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t\t\t\t<dsi:valueStandardMU>"+uCarrier_conc+"</dsi:valueStandardMU>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t\t\t</dsi:standardMU>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t\t</dsi:measurementUncertaintyUnivariate>\n")
                            
                            # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:expandedUnc>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t\t\t<dsi:uncertainty>"+uCarrier_conc+"</dsi:uncertainty>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t\t\t<dsi:coverageFactor>1</dsi:coverageFactor>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t\t\t<dsi:coverageProbability>0.68</dsi:coverageProbability>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t\t</dsi:expandedUnc>\n")   
                        FAIRfile.write("\t\t\t\t\t\t\t</kc:carrierConcentration>\n")
                    # print(Carrier_conc, UnknownCarConc)
                    FAIRfile.write("\t\t\t\t\t\t</kc:carrier>\n")
                FAIRfile.write("\t\t\t\t\t</kc:chemicalComposition>\n")
                FAIRfile.write("\t\t\t\t\t<kc:impurities>"+reportedImpurity+"</kc:impurities>\n")
                FAIRfile.write("\t\t\t\t</kc:radioactiveSolution>\n")
            FAIRfile.write("\t\t\t</kc:radioactiveSolutions>\n")
        if AiFlag and FlagK1:
            FAIRfile.write("\t\t\t<kc:laboratoryMeasurements>\n")
            for indexMeth, meth_i in enumerate(methods):
                for indexMass, mass_i in enumerate(mass):
                    FAIRfile.write("\t\t\t\t<kc:measurement>\n")
                    if MassFlag:
                        FAIRfile.write("\t\t\t\t\t<kc:referenceDate>"+dateRef+"</kc:referenceDate>\n")
                        FAIRfile.write("\t\t\t\t\t<kc:solutionID>"+solutionID[indexMass]+"</kc:solutionID>\n")
                        if HalfLife == True:
                            FAIRfile.write("\t\t\t\t\t<kc:halfLife>\n")
                            FAIRfile.write("\t\t\t\t\t\t<kc:evaluation>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t<dsi:value>"+halfLifeValue+"</dsi:value>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t<dsi:unit>"+halfLifeUnit+"</dsi:unit>\n") 
                                                   
                            # FAIRfile.write("\t\t\t\t\t\t<value>"+halfLifeValue+"</value>\n")
                            # FAIRfile.write("\t\t\t\t\t\t<unit>"+halfLifeUnit+"</unit>\n")
                            if halfLifeStd:
                               
                                FAIRfile.write("\t\t\t\t\t\t\t<dsi:measurementUncertaintyUnivariate>\n")
                                FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:standardMU>\n")
                                FAIRfile.write("\t\t\t\t\t\t\t\t\t<dsi:valueStandardMU>"+halfLifeStd+"</dsi:valueStandardMU>\n")
                                FAIRfile.write("\t\t\t\t\t\t\t\t</dsi:standardMU>\n")
                                FAIRfile.write("\t\t\t\t\t\t\t</dsi:measurementUncertaintyUnivariate>\n")
                               
                                # FAIRfile.write("\t\t\t\t\t\t\t<dsi:expandedUnc>\n")
                                # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:uncertainty>"+halfLifeStd+"</dsi:uncertainty>\n")
                                # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:coverageFactor>1</dsi:coverageFactor>\n")
                                # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:coverageProbability>0.68</dsi:coverageProbability>\n")
                                # FAIRfile.write("\t\t\t\t\t\t\t</dsi:expandedUnc>\n")
                            FAIRfile.write("\t\t\t\t\t\t</kc:evaluation>\n")
                            if ReferenceDecayData:
                                if DOIdecayData:
                                    FAIRfile.write("\t\t\t\t\t\t<kc:reference>\n")
                                    FAIRfile.write("\t\t\t\t\t\t\t<kc:doi>"+DOIdecayData+"</kc:doi>\n")
                                    FAIRfile.write("\t\t\t\t\t\t</kc:reference>\n")
                                else:
                                    FAIRfile.write("\t\t\t\t\t\t<kc:reference>\n")
                                    FAIRfile.write("\t\t\t\t\t\t\t<kc:detail>"+DetaildecayData+"</kc:detail>\n")
                                    FAIRfile.write("\t\t\t\t\t\t</kc:reference>\n")
                                    
                            FAIRfile.write("\t\t\t\t\t</kc:halfLife>\n")
    
                    if "null" in meth_i: FAIRfile.write("\t\t\t\t\t<kc:methodID></kc:methodID>\n")
                    else: FAIRfile.write("\t\t\t\t\t<kc:methodID>"+meth_i+"</kc:methodID>\n")
                    if "null" in DescriptMethod[indexMeth]: FAIRfile.write("\t\t\t\t\t<kc:description></kc:description>\n")
                    else: FAIRfile.write("\t\t\t\t\t<kc:description>"+DescriptMethod[indexMeth]+"</kc:description>\n")
                    
                    if CommentMethod:
                        FAIRfile.write("\t\t\t\t\t<kc:comments>"+CommentMethod[0]+"</kc:comments>\n")
                    if AiFlag:
                        FAIRfile.write("\t\t\t\t\t<kc:activity>\n")
                        if len(Ai) == len(methods):
                            FAIRfile.write("\t\t\t\t\t\t<kc:measurementResult>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t<dsi:value>"+str(Ai[indexMeth])+"</dsi:value>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t<dsi:unit>"+str(unit_Ai)+"</dsi:unit>\n")                         
                            # FAIRfile.write("\t\t\t\t\t\t\t<dsi:uncertaintyValueType>"+str(uC_Ai[indexMeth])+"</dsi:uncertaintyValueType>\n")
                            
                            FAIRfile.write("\t\t\t\t\t\t\t<dsi:measurementUncertaintyUnivariate>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:standardMU>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t\t\t<dsi:valueStandardMU>"+str(uC_Ai[indexMeth])+"</dsi:valueStandardMU>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t\t</dsi:standardMU>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t</dsi:measurementUncertaintyUnivariate>\n")
                           
                            # FAIRfile.write("\t\t\t\t\t\t\t<dsi:expandedUnc>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:uncertainty>"+str(uC_Ai[indexMeth])+"</dsi:uncertainty>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:coverageFactor>1</dsi:coverageFactor>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:coverageProbability>0.68</dsi:coverageProbability>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t</dsi:expandedUnc>\n")
                            
                            FAIRfile.write("\t\t\t\t\t\t</kc:measurementResult>\n")

                            if (not LabCombUonly):
                                FAIRfile.write("\t\t\t\t\t\t<kc:relStdUncertTypeA>"+str(uA_Ai[indexMeth])+"</kc:relStdUncertTypeA>\n")
                                FAIRfile.write("\t\t\t\t\t\t<kc:relStdUncertTypeB>"+str(uB_Ai[indexMeth])+"</kc:relStdUncertTypeB>\n")
                            # FAIRfile.write("\t\t\t\t\t\t<relative_standard_uncertainty_combined>"+str(uC_Ai[indexMeth])+"</relative_standard_uncertainty_combined>\n")
                        elif len(Ai) > len(methods):
                            FAIRfile.write("\t\t\t\t\t\t<kc:measurementResult>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t<dsi:value>"+str(Ai[indexMass])+"</dsi:value>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t<dsi:unit>"+str(unit_Ai)+"</dsi:unit>\n") 
                           
                            FAIRfile.write("\t\t\t\t\t\t\t<dsi:measurementUncertaintyUnivariate>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:standardMU>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t\t\t<dsi:valueStandardMU>"+str(uC_Ai[0])+"</dsi:valueStandardMU>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t\t</dsi:standardMU>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t</dsi:measurementUncertaintyUnivariate>\n")
                           
                            
                            # FAIRfile.write("\t\t\t\t\t\t\t<dsi:expandedUnc>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:uncertainty>"+str(uC_Ai[0])+"</dsi:uncertainty>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:coverageFactor>1</dsi:coverageFactor>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:coverageProbability>0.68</dsi:coverageProbability>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t</dsi:expandedUnc>\n")
                            
                            FAIRfile.write("\t\t\t\t\t\t</kc:measurementResult>\n")

                            if (not LabCombUonly):
                                FAIRfile.write("\t\t\t\t\t\t<kc:relStdUncertTypeA>"+str(uA_Ai[0])+"</kc:relStdUncertTypeA>\n")
                                FAIRfile.write("\t\t\t\t\t\t<kc:relStdUncertTypeB>"+str(uB_Ai[0])+"</kc:relStdUncertTypeB>\n")
                            # FAIRfile.write("\t\t\t\t\t\t<relative_standard_uncertainty_combined>"+str(uC_Ai[0])+"</relative_standard_uncertainty_combined>\n")
                        else:
                            FAIRfile.write("\t\t\t\t\t\t<kc:measurementResult>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t<dsi:value>"+str(Ai[0])+"</dsi:value>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t<dsi:unit>"+str(unit_Ai)+"</dsi:unit>\n")
                            
                            FAIRfile.write("\t\t\t\t\t\t\t<dsi:measurementUncertaintyUnivariate>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:standardMU>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t\t\t<dsi:valueStandardMU>"+str(uC_Ai[0])+"</dsi:valueStandardMU>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t\t</dsi:standardMU>\n")
                            FAIRfile.write("\t\t\t\t\t\t\t</dsi:measurementUncertaintyUnivariate>\n")
                            
                            # FAIRfile.write("\t\t\t\t\t\t\t<dsi:expandedUnc>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:uncertainty>"+str(uC_Ai[0])+"</dsi:uncertainty>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:coverageFactor>1</dsi:coverageFactor>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:coverageProbability>0.68</dsi:coverageProbability>\n")
                            # FAIRfile.write("\t\t\t\t\t\t\t</dsi:expandedUnc>\n")
                            
                            
                            FAIRfile.write("\t\t\t\t\t\t</kc:measurementResult>\n")

                            if (not LabCombUonly):
                                FAIRfile.write("\t\t\t\t\t\t<kc:relStdUncertTypeA>"+str(uA_Ai[0])+"</kc:relStdUncertTypeA>\n")
                                FAIRfile.write("\t\t\t\t\t\t<kc:relStdUncertTypeB>"+str(uB_Ai[0])+"</kc:relStdUncertTypeB>\n")
                            # FAIRfile.write("\t\t\t\t\t\t<relative_standard_uncertainty_combined>"+str(uC_Ai[0])+"</relative_standard_uncertainty_combined>\n")
                        FAIRfile.write("\t\t\t\t\t</kc:activity>\n")
                    if AiFlag: FAIRfile.write("\t\t\t\t</kc:measurement>\n")
            FAIRfile.write("\t\t\t</kc:laboratoryMeasurements>\n")

        if MassFlag: massEqAe = len(mass)==len(Ae)
        methEqAe = len(methods)==len(Ae)
        #print(RaRef, Ai, Ae, massEqAe, methEqAe)
        FAIRfile.write("\t\t\t<kc:bipmMeasurements>\n")
        
        if len(Ae)==1:
            FAIRfile.write("\t\t\t\t<kc:bipmMeasurement>\n")
            if MassFlag:
                FAIRfile.write("\t\t\t\t\t<kc:solutions>\n")
                for sol in solutionID:
                    FAIRfile.write("\t\t\t\t\t\t<kc:solutionID>")
                    FAIRfile.write(sol)
                    FAIRfile.write("</kc:solutionID>\n")
                FAIRfile.write("\t\t\t\t\t</kc:solutions>\n")
            if AiFlag:
                FAIRfile.write("\t\t\t\t\t<kc:methods>\n")
                for meth in methods:
                    FAIRfile.write("\t\t\t\t\t\t<kc:method>")
                    if "null" not in meth: FAIRfile.write(meth)
                    FAIRfile.write("</kc:method>\n")
                FAIRfile.write("\t\t\t\t\t</kc:methods>\n")
            if RaRef:
                FAIRfile.write("\t\t\t\t\t<kc:referenceSource>")
                FAIRfile.write(RaRef[0])
                FAIRfile.write("</kc:referenceSource>\n")
            FAIRfile.write("\t\t\t\t\t<kc:equivalentActivity>\n")
            FAIRfile.write("\t\t\t\t\t\t<kc:sirResult>\n")
            FAIRfile.write("\t\t\t\t\t\t\t<dsi:value>"+str(Ae[0])+"</dsi:value>\n")
            FAIRfile.write("\t\t\t\t\t\t\t<dsi:unit>"+str(AeUnit)+"</dsi:unit>\n")  
            
            FAIRfile.write("\t\t\t\t\t\t\t<dsi:measurementUncertaintyUnivariate>\n")
            FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:standardMU>\n")
            FAIRfile.write("\t\t\t\t\t\t\t\t\t<dsi:valueStandardMU>"+str(u_Ae[0])+"</dsi:valueStandardMU>\n")
            FAIRfile.write("\t\t\t\t\t\t\t\t</dsi:standardMU>\n")
            FAIRfile.write("\t\t\t\t\t\t\t</dsi:measurementUncertaintyUnivariate>\n")
            
            # FAIRfile.write("\t\t\t\t\t\t\t<dsi:expandedUnc>\n")
            # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:uncertainty>"+str(u_Ae[0])+"</dsi:uncertainty>\n")
            # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:coverageFactor>1</dsi:coverageFactor>\n")
            # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:coverageProbability>0.68</dsi:coverageProbability>\n")
            # FAIRfile.write("\t\t\t\t\t\t\t</dsi:expandedUnc>\n")
            
            FAIRfile.write("\t\t\t\t\t\t</kc:sirResult>\n")

            if u_SIR_Ae:
                FAIRfile.write("\t\t\t\t\t\t<kc:relStdUncertFromSIR>")
                FAIRfile.write(str(round(float(u_SIR_Ae[0])*1e-4,4)))
                FAIRfile.write("</kc:relStdUncertFromSIR>\n")
            FAIRfile.write("\t\t\t\t\t</kc:equivalentActivity>\n")
            if linkSub:
                FAIRfile.write("\t\t\t\t\t<kc:fromLinkedComparison>")
                FAIRfile.write(ref_link_2)
                FAIRfile.write("</kc:fromLinkedComparison>\n")
            FAIRfile.write("\t\t\t\t</kc:bipmMeasurement>\n")
        
        elif len(solutionID)>1:
            for i_sol, sol in enumerate(solutionID):
                FAIRfile.write("\t\t\t\t<kc:bipmMeasurement>\n")
                FAIRfile.write("\t\t\t\t\t<kc:solutions>\n")
                if MassFlag:
                    FAIRfile.write("\t\t\t\t\t\t<kc:solutionID>")
                    FAIRfile.write(sol)
                    FAIRfile.write("</kc:solutionID>\n")
                FAIRfile.write("\t\t\t\t\t</kc:solutions>\n")
                FAIRfile.write("\t\t\t\t\t<kc:methods>\n")
                FAIRfile.write("\t\t\t\t\t\t<kc:method>")
                if "null" not in methods[0]: FAIRfile.write(methods[0])
                FAIRfile.write("</kc:method>\n")
                FAIRfile.write("\t\t\t\t\t</kc:methods>\n")
                if RaRef:
                    FAIRfile.write("\t\t\t\t\t<kc:referenceSource>")
                    FAIRfile.write(RaRef[i_sol])
                    FAIRfile.write("</kc:referenceSource>\n")
                FAIRfile.write("\t\t\t\t\t<kc:equivalentActivity>\n")
                FAIRfile.write("\t\t\t\t\t\t<kc:sirResult>\n")
                FAIRfile.write("\t\t\t\t\t\t\t<dsi:value>"+str(Ae[i_sol])+"</dsi:value>\n")
                FAIRfile.write("\t\t\t\t\t\t\t<dsi:unit>"+str(AeUnit)+"</dsi:unit>\n")     
                
                FAIRfile.write("\t\t\t\t\t\t\t<dsi:measurementUncertaintyUnivariate>\n")
                FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:standardMU>\n")
                FAIRfile.write("\t\t\t\t\t\t\t\t\t<dsi:valueStandardMU>"+str(u_Ae[i_sol])+"</dsi:valueStandardMU>\n")
                FAIRfile.write("\t\t\t\t\t\t\t\t</dsi:standardMU>\n")
                FAIRfile.write("\t\t\t\t\t\t\t</dsi:measurementUncertaintyUnivariate>\n")
                
                # FAIRfile.write("\t\t\t\t\t\t\t<dsi:expandedUnc>\n")
                # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:uncertainty>"+str(u_Ae[i_sol])+"</dsi:uncertainty>\n")
                # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:coverageFactor>1</dsi:coverageFactor>\n")
                # FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:coverageProbability>0.68</dsi:coverageProbability>\n")
                # FAIRfile.write("\t\t\t\t\t\t\t</dsi:expandedUnc>\n")      
                
                FAIRfile.write("\t\t\t\t\t\t</kc:sirResult>\n")

                if u_SIR_Ae:
                   FAIRfile.write("\t\t\t\t\t\t<kc:relStdUncertFromSIR>")
                   FAIRfile.write(str(round(float(u_SIR_Ae[i_sol])*1e-4,4)))
                   FAIRfile.write("</kc:relStdUncertFromSIR>\n")
                FAIRfile.write("\t\t\t\t\t</kc:equivalentActivity>\n")
                FAIRfile.write("\t\t\t\t</kc:bipmMeasurement>\n")

        elif len(methods)>1:
           for i_meth, meth in enumerate(methods):
                FAIRfile.write("\t\t\t\t<kc:bipmMeasurement>\n")
                FAIRfile.write("\t\t\t\t\t<kc:solutions>\n")
                FAIRfile.write("\t\t\t\t\t\t<kc:solutionID>")
                FAIRfile.write(solutionID[0])
                FAIRfile.write("</kc:solutionID>\n")
                FAIRfile.write("\t\t\t\t\t</kc:solutions>\n")
                FAIRfile.write("\t\t\t\t\t<kc:methods>\n")
                FAIRfile.write("\t\t\t\t\t\t<kc:method>")
                if "null" not in meth: FAIRfile.write(meth)
                FAIRfile.write("</kc:method>\n")
                FAIRfile.write("\t\t\t\t\t</kc:methods>\n")
                if RaRef:
                    FAIRfile.write("\t\t\t\t\t<kc:referenceSource>")
                    FAIRfile.write(RaRef[0])
                    FAIRfile.write("</kc:referenceSource>\n")
                FAIRfile.write("\t\t\t\t\t<kc:equivalentActivity>\n")
                FAIRfile.write("\t\t\t\t\t\t<kc:sirResult>\n")
                FAIRfile.write("\t\t\t\t\t\t\t<dsi:value>"+str(Ae[i_meth])+"</dsi:value>\n")
                FAIRfile.write("\t\t\t\t\t\t\t<dsi:unit>"+str(AeUnit)+"</dsi:unit>\n")   
                
                FAIRfile.write("\t\t\t\t\t\t\t<dsi:measurementUncertaintyUnivariate>\n")
                FAIRfile.write("\t\t\t\t\t\t\t\t<dsi:standardMU>\n")
                FAIRfile.write("\t\t\t\t\t\t\t\t\t<dsi:valueStandardMU>"+str(u_Ae[i_meth])+"</dsi:valueStandardMU>\n")
                FAIRfile.write("\t\t\t\t\t\t\t\t</dsi:standardMU>\n")
                FAIRfile.write("\t\t\t\t\t\t\t</dsi:measurementUncertaintyUnivariate>\n")
                
                FAIRfile.write("\t\t\t\t\t\t</kc:sirResult>\n")
                
                if u_SIR_Ae:
                   FAIRfile.write("\t\t\t\t\t\t<kc:relStdUncertFromSIR>")
                   FAIRfile.write(str(round(float(u_SIR_Ae[0])*1e-4,4)))
                   FAIRfile.write("</kc:relStdUncertFromSIR>\n")
                FAIRfile.write("\t\t\t\t\t</kc:equivalentActivity>\n")
                FAIRfile.write("\t\t\t\t</kc:bipmMeasurement>\n")
                
        else:
            print("warning: not managed!")


        FAIRfile.write("\t\t\t</kc:bipmMeasurements>\n")
        FAIRfile.write("\t\t</kc:submission>\n")
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

file.close()
FAIRfile.close()
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







"""
VALIDATION
"""
def calculate_checksum(xml_document):
    with open(xml_document, 'rb') as file:
        xml_content = file.read()
    sha256_hash = hashlib.sha256(xml_content).hexdigest()
    return sha256_hash
checksum = calculate_checksum(FAIRfileName)
print(f"SHA-256 Checksum: {checksum}")


# import requests

# xsd_url = "https://www.ptb.de/si/v2.1.0/SI_Format.xsd"

# try:
#     response = requests.get(xsd_url)
#     if response.status_code == 200:
#         xsd_content = response.text
#         print("Access to D_SI")
#     else:
#         print(f"Failed to fetch XSD. Status code: {response.status_code}")
# except Exception as e:
#     print(f"Error: {e}")



# # time.sleep(2)
# xml_file = lxml.etree.parse(FAIRfileName)
# xml_validator = lxml.etree.XMLSchema(file="FAIRversions/KC_model_RI_II.xsd")

# is_valid = xml_validator.validate(xml_file)

# if is_valid == 'True' :
#     output = "The xml has been validated"
# else:
#     output = "The xml was not validated"
    
# print(output + "\n")

# def validate_with_lxml(xsd_tree, xml_tree):
#     table=[['Line','ErComparison_(s)']] #Output table structure
#     raw=[]                        #row used to remove any duplicates
#     xmlschema = xsd_tree
#     try:
#         xmlschema.assertValid(xml_tree)
#     except lxml.etree.DocumentInvalid:
#         print("Validation erComparison_(s):\n")
#         for error in xmlschema.error_log:
#             if error.line not in raw:
#                 table.append([error.line,textwrap.fill(error.message, width=60)])
#                 raw.append(error.line)
            
#         print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))


# validate_with_lxml(xml_validator,xml_file)