# BIPM key comparison database for radionuclide metrology

Romain Coulon, BIPM, 2022-10-03

This repository contains machine-readable versions (XML and JSON formats) of the BIPM/RI(II)-K1 key comparison reports [1].
These comparisons are made using the BIPM's measurement service, the International Reference System (SIR), which has been in use since 1976 [2].
The files contain exactly the same information as the reports publicly available in PDF format on the key comparison database platform (KCDB [3]).

## Structure of the data

### Root 

The root of the file consists of two sections. The first section gives general information on the data. The second section gives all available details on a given radionuclide.

* General information
  - Content
  - Date
  - References
* Name of the radionuclide (eg. Ga-67)
  - Bibliographical data

### Metadata

        "Eligible for the Key Comparison Reference Value (KCRV)": false,
        "Eligible for Degree of Equivalence (DoE)": false,
        "Laboratory": {
            "Acronym": "LNE-LNHB",
            "Full name": "Université Paris-Saclay, CEA, List, Laboratoire National Henri Becquerel",
            "Address": "F-91120 Palaiseau",
            "Country": "France",
            "Regional Metrology Organization (RMO)": "EURAMET",
            "Old acronyms": "LMRI, LPRI, BNM-LNHB"
            },
        "Contributor(s) from the BIPM": null,
        "Contributor(s) from the laboratory": null,
        "Date of reference specified by the laboratory": "1981-11-13 12:00 UT",
        "Acronym(s) of the measurement method(s)": "4P-PP-MX-NA-GR-AC",
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
