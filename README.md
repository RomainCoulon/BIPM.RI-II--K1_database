# BIPM key comparison database for radionuclide metrology

Romain Coulon, BIPM, 2022-10-03

This repository contains machine-readable versions (XML and JSON formats) of the BIPM/RI(II)-K1 key comparison reports [1].
These comparisons are made using the BIPM's measurement service, the International Reference System (SIR), which has been in use since 1976 [2].
The files contain exactly the same information as the reports publicly available in PDF format on the key comparison database platform (KCDB [3]). This database is continuously updated.

If you have any questions about this database, please contact romain.coulon@bipm.org.

## Structure of the data

### Root 

The root of the file consists of two sections. The first section gives general information on the data. The second section gives all available details on a given radionuclide.

* General information
  - Content
  - Date
  - References
* Name of the radionuclide (eg. Ga-67)
  - Key comparison data
  - Key comparison metadata

### Key comparison data

Each time a report is published, an entry is created such as "Key comparison BIPM.RI(II)-K1.Xx-ZZZ(YYYY)", where Xx-ZZZ is the radionuclide (eg. Am-241) and YYYY is the year of publication. The key comparison value (KCRV) is expressed as a string with the value followed by the standard uncertainty in brackets, then a space and finally the unit (e.g. "5980.8(64) kBq"). Values of the degrees of equivalence (DoE) are in number. The quantity $D_i$ is the value of the DoE and $U_i$ is the extended uncertainty ($k$=2). Please note that while the KCRV is reported for each reporting year, the degrees of equivalence are only available for publications after 2019. 

* Key comparison BIPM.RI(II)-K1.Ag-110m(YYYY)
  - Name of the comparison
  - Year of publication
  - Key Comparison Reference Value (KCRV)
  - Reference of the published comparison report
  - Editorial assistant(s)
  - Comments on the publication
  - Unit
  - Degrees of Equivalence
    - Laboratory name
      - $D_i$
      - $U_i$
    - ...
*  ... 

### Key comparison metadata

The key comparison metadata is data on the key comparison data presented above. All submissions by laboratories of standard solutions of the radionuclide of interest are detailed. Each entry is referenced by the acronym of the national metrology institutes (NMI) and designated institutes (DI), followed by the year of submission (e.g. NIST-2020).

The first two entries specify with a Boolean value whether the submission is eligible for the rules defined by the CIPM/CCRI(II) to produce a DoE and be used for the calculation of the reference value. In the 3<sup>rd</sup> entry, administrative deltails on the participant are given. In the 4<sup>th</sup> and 5<sup>th</sup> entries, the contributors involved in the BIPM measurement and the participating laboratory are listed. In the 6<sup>th</sup> entry, the reference date for which the laboratory calculated the activity is given in the format "YYYY-MM-DD HH:mm UT". In the 7<sup>th</sup> entry, the acronym(s) of the method(s) used by the laboratory are specified according to the nomenclature defined by the CIPM/CCRI(II). When several methods, they are separated by a ",". In the eighth entry, the full description of the method(s) is given and further relevant comments are written in the ninth entry. The particulars ("number of sample" and "number of method") of the submission are given in the 10<sup>th</sup> entry. They make it possible to know what the values that will be given later correspond to. The configurations can be as follows:

a) "1 sample and 1 measurement method"

b) "1 sample and several measurement methods"

c) "1 sample and average of several measurement methods"

d) "Several samples and several measurement methods"

e) "Several samples and  average of several measurement methods"

f) "Several samples and 1 measurement method"

In configurations a) and c), only one value is given in the following entries. In configurations b), e) d) and f), several values - seprated by "," - are given in the following entries. In entries 11, 12, 13, 14, are respectively given, the activity(ies), the relative type A standard uncertainty(ies), the relative type B standard uncertainty(ies), the relative combined standard uncertainty(ies). 

* Data from Lab-Acronym-YYYY
  - Eligible for the Key Comparison Reference Value (KCRV)
  - Eligible for Degree of Equivalence (DoE)
  - Laboratory
    - Acronym
    - Full name
    - Address
    - Country
    - Regional Metrology Organization (RMO)
    - Old acronyms
  - Contributor(s) from the BIPM
  - Contributor(s) from the laboratory
  - Date of reference specified by the laboratory
  - Acronym(s) of the measurement method(s)
  - Description of the measurement method(s)
  - Comment(s) on the measurement method(s)
  - Particularities of the submission to the SIR
  - Activity measured by the laboratory / kBq"
  - Type A evaluation of the relative standard uncertainty of the activity measured by the laboratory
  - Type B evaluation of the relative standard uncertainty of the activity measured by the laboratory
  - Combined relative standard uncertainty of the activity measured by the laboratory
  - Date of the measurement by the BIPM international reference system (SIR)
  - Half-life used by the laboratory / d
  - Reference for the decay data used by the laboratory
  - Chemical composition of the solution
  - Solvent concentration of the solution / (mol.dm-3)
  - Carrier concentration of the solution / (µg.g-1)
  - Density of the solution / (g.cm-3)
  - Relative activity of impurities contained into the solution
  - Comments on impurities contained into the solution
  - Mass of the solution /g
  - Number of the radium source used by the SIR
  - Equivalent activity measured by the SIR / kBq
  - Relative standard uncertainty (SIR contribution) of the equivalent activity / 1e-4
  - Comments on the SIR measurement
  - Combined standard uncertainty of the equivalent activity / kBq
  - Number of the equivalent activity measurement retained for the degree of equivalence
  - Specified equivalent activity for the degree of equivalence
  - Specified equivalent activity for the key comparison reference value
  - Comments on the equivalent activity
  - Initials of the person who entered the data plus the date
  - Initials of the person(s) who verified the data plus the date
  - Status of the data

## Reference

[1] https://doi.org/10.1088/1361-6501/ac3fc4

[2] https://doi.org/10.1016/S0160-4120(78)80071-3

[3] https://www.bipm.org/kcdb/
