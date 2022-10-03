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

Each time a report is published, an entry is created such as "Key comparison BIPM.RI(II)-K1.Ag-110m(YYYY)", where YYYY is the year of publication. The key comparison value (KCRV) is expressed as a string with the value followed by the standard uncertainty in brackets, then a space and finally the unit (e.g. "5980.8(64) kBq"). Values of the degrees of equivalence (DoE) are in number. The quantity $D_i$ is the value of the DoE and $U_i$ is the extended uncertainty ($k$=2). Please note that while the KCRV is reported for each reporting year, the degrees of equivalence are only available for publications after 2019. 

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





* Data from ACRONYME-YYYY
  - Eligible for the Key Comparison Reference Value (KCRV)
  - Eligible for Degree of Equivalence (DoE)
  - Laboratory
    - Acronym
    - Full name
    - Address
    - Country
    - Regional Metrology Organization (RMO)
    - Old acronyms
  - Contributor(s) from the BIPM": null,
  - Contributor(s) from the laboratory": null,
  - Date of reference specified by the laboratory": "1981-11-13 12:00 UT",
  - Acronym(s) of the measurement method(s)": "4P-PP-MX-NA-GR-AC",
        "Description of the measurement method(s)": "4pi(eA,x)-gamma anti-coincidence",
        "Comment(s) on the measurement method(s)": null,
        "Particularities of the submission to the SIR": "Several samples and 1 measurement method",
        "Activity measured by the laboratory / kBq": "4772, 4771",
        "Type A evaluation of the relative standard uncertainty of the activity measured by the laboratory": "0.02, 0.02",
        "Type B evaluation of the relative standard uncertainty of the activity measured by the laboratory": "0.38, 0.38",
        "Combined relative standard uncertainty of the activity measured by the laboratory": null,
        "Date of the measurement by the BIPM international reference system (SIR)": "10/11/1981",
        "Half-life used by the laboratory / d": null,
        "Reference for the decay data used by the laboratory": null,
        "Chemical composition of the solution": "Ga citrate and NaCl in HCl",
        "Solvent concentration of the solution / (mol.dm-3)": "0.1",
        "Carrier concentration of the solution / (µg.g-1)": "NaCl: 180",
        "Density of the solution / (g.cm-3)": "1.006",
        "Relative activity of impurities contained into the solution": "57Co: 5.1(10)x10-4 %, 60Co: 7.2(15)x10-4 %",
        "Comments on impurities contained into the solution": null,
        "Mass of the solution /g": "3.6125, 3.6119",
        "Number of the radium source used by the SIR": "3, 3",
        "Equivalent activity measured by the SIR / kBq": "114616, 114597",
        "Relative standard uncertainty (SIR contribution) of the equivalent activity / 1e-4": "10, 9",
        "Comments on the SIR measurement": null,
        "Combined standard uncertainty of the equivalent activity / kBq": "450, 450",
        "Number of the equivalent activity measurement retained for the degree of equivalence": null,
        "Specified equivalent activity for the degree of equivalence": null,
        "Specified equivalent activity for the key comparison reference value": null,
        "Comments on the equivalent activity": null,
        "Initials of the person who entered the data plus the date": "SJ (06/05/2020)",
        "Initials of the person(s) who verified the data plus the date": "SC (06/05/2020)",
        "Status of the data": "

## Reference

[1] https://doi.org/10.1088/1361-6501/ac3fc4

[2] https://doi.org/10.1016/S0160-4120(78)80071-3

[3] https://www.bipm.org/kcdb/
