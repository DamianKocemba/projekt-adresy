# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 19:00:22 2022

@author: damia
"""

import pandas as pd
import re

path = "C:\\Users\\damia\\OneDrive\\Pulpit\\Python\\KontrolaAdresow_Brzesko\\120204_2_0001_wlasciciele.txt"

data = pd.read_csv(path, sep="|", encoding='ansi').astype(str)

columns = [col for col in data.columns]

adresy = data.groupby(columns[4:], as_index=False).agg({'DZIALKA': '#'.join})

#sprawdzenie ilosci srednikow
adresy["SREDNIKI"] = adresy["ADRES"].str.count(";")

adresy_cz1 = adresy[adresy.SREDNIKI == 1]
adresy_cz2 = adresy[adresy.SREDNIKI != 1].reset_index()

adresy_cz1[["UL_MSC_NRADR","KOD_POCZT"]] = adresy_cz1["ADRES"].str.split(";", expand=True)

adresy_cz1[["RESZTA","NRADR"]] = adresy_cz1["UL_MSC_NRADR"].str.rsplit(" ", n=1, expand=True)

adresy_cz1["mask"] = adresy_cz1["UL_MSC_NRADR"].str.contains(r' \d+$')

test = adresy_cz2[["ADRES",]]
test["ADRES_TEST"] = adresy_cz2["ADRES"].str.replace(" ", "")

#%%

przedrostki = ['ul', 'al', 'pl', 'os', 'oś']



for i, row in adresy_cz2.iterrows():
    
    # obsluzenie przypadków z przedrostkiem ulicy/alei/placu/osiedla
    pat = "[.|\s].+[^,\s] [0-9]+[a-zA-Z0-9mlok/]*"
    pat_ = '{}|'.format(pat).join(p.upper() for p in przedrostki) + pat  
    #print(pat_)
    if re.search(pat_, row["ADRES"]): 
        print(i)
        print(row["ADRES"])
        ul_nr = re.findall(pat_, row["ADRES"])[0]
        ulica = ul_nr.rsplit(" ",1)[0]
        nr_adresowy = ul_nr.rsplit(" ",1)[1]
        kod_msc = row["ADRES"].replace(ul_nr,"").replace(",","").strip()
        print(ulica)
        print(nr_adresowy)
        print(kod_msc)
        print()
        
        adresy_cz2.loc[i,"UL_MSC"] = ulica
        adresy_cz2.loc[i,"NRADR"] = nr_adresowy
        adresy_cz2.loc[i,"KOD_POCZT"] = kod_msc
        
#%%
for i, row in adresy_cz2.iterrows():
    
    #obsluzenie przypadkow, wg wzoru: nr_adresowy miejscowosc
    pat = "^[0-9]+[A-Z]? [^0-9][A-ZĄĆĘŁŚÓŹŻ-]+"

    if re.search(pat, row["ADRES"]) and pd.isnull(adresy_cz2.at[i,"UL_MSC"]):
        print(i)
        print(row["ADRES"])
        nradr_msc = row["ADRES"].split(" ",1)
        miejscowosc = nradr_msc[1]
        nr_adresowy = nradr_msc[0]
        print(miejscowosc)
        print(nr_adresowy)
  
        adresy_cz2.loc[i,"UL_MSC"] = miejscowosc
        adresy_cz2.loc[i,"NRADR"] = nr_adresowy

#%%
#adresy_cz2.at[1, "ADRES"] = "CHŁOPSKA 27 TARNÓW-TARNÓW"    #do testow
        
for i, row in adresy_cz2.iterrows():
    #obsluzenie przypadkow wg wzoru: ulica nr_adr miejscowosc
    pat = ("[0-9A-ZĄĆĘŁŚÓŹŻ-]+ [0-9]+[m/]?[0-9]* [A-ZĄĆĘŁŚÓŹŻ-]+|"
             "[0-9A-ZĄĆĘŁŚÓŹŻ-]+ [0-9]+[a-z/]{2}[0-9]* [A-ZĄĆĘŁŚÓŹŻ-]+")
    
    if re.search(pat, row["ADRES"]) and pd.isnull(adresy_cz2.at[i,"UL_MSC"]):
        print(i)
        print(row["ADRES"])
        ul_nr = re.findall(".+[0-9]", row["ADRES"])[0] #wyciagniecie ulicy i nr adresowego
        ul_nr_lista = ul_nr.rsplit(" ", 1)
        ulica = ul_nr_lista[0]
        nr_adresowy = ul_nr_lista[1]
        miejscowosc = row["ADRES"].replace(ul_nr,"").strip()
        print(ul_nr)
        print(ulica)
        print(nr_adresowy)
        print(miejscowosc)

        adresy_cz2.loc[i,"UL_MSC"] = ulica
        adresy_cz2.loc[i,"NRADR"] = nr_adresowy
        adresy_cz2.loc[i,"KOD_POCZT"] = miejscowosc

#%%
for i, row in adresy_cz2.iterrows():
    #obsluzenie przypadkow wg wzoru: miejscowosc (kod poczt) nr adresowy
    pat = ".+ [0-9]+[m/]?[0-9]+"
    if re.search(pat, row["ADRES"]) and pd.isnull(adresy_cz2.at[i,"UL_MSC"]):
        print(i)
        print(row["ADRES"])
        msc_nr = row["ADRES"].rsplit(" ", 1)
        miejscowosc = msc_nr[0]
        nr_adresowy = msc_nr[1]
        print(msc_nr)
        print(miejscowosc)
        print(nr_adresowy)
        
        adresy_cz2.loc[i,"NRADR"] = nr_adresowy
        if re.search("[0-9]{2}-[0-9]{3}", miejscowosc):
            adresy_cz2.loc[i,"KOD_POCZT"] = miejscowosc
        else:
            adresy_cz2.loc[i,"UL_MSC"] = miejscowosc
        
        
    
            

















