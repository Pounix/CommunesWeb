# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 10:18:44 2021

@author: jmoug
v3 . juste pour Github test
"""
import csv
import random
import unicodedata
import re
from operator import itemgetter        # pour le tri , voir page 239
from math import *

class commune:
    def __init__(self,code_commune=0,nom_commune="",ligne_5="",nom_commune_sans_accents="",latitude=0.0,longitude=0.0,code_postal=0,nom_departement="",code_departement=0,nom_region="",code_region=0):
        self.code_commune=code_commune
        self.nom_commune=nom_commune
        self.ligne_5=ligne_5
        self.nom_commune_sans_accents=nom_commune_sans_accents
        self.latitude=latitude
        self.longitude=longitude
        self.code_postal=code_postal
        self.nom_departement=nom_departement
        self.code_departement=code_departement
        self.nom_region=nom_region
        self.code_region=code_region
        
        
    def __str__(self):
        c="{0:-<40}".format(self.nom_commune+' '+ self.ligne_5)
        return f"{c} - ({self.code_departement}) {self.nom_departement}"
    
    def __sub__(self, valeur):
        phi_A=radians(self.latitude)
        phi_B=radians(valeur.latitude)
        lam_A=radians(self.longitude)
        lam_B=radians(valeur.longitude)
        trigo=max(min(sin(phi_A)*sin(phi_B)+cos(phi_A)*cos(phi_B)*cos(lam_B-lam_A),1),-1) # arrondis de calculs peuvent donner + que 1...
        
        resultat=6371*acos(trigo)
        return resultat

    def __lt__(self, autre):
        t= len(self.nom_commune) < len(autre.nom_commune)
        return t

class prox:
    
    def __init__(self,distance=float(),commune=commune()):
        self.distance=distance
        self.commune=commune
        
    def __lt__(self, autre):
        t= self.distance < autre.distance
        return t
    
    def __str__(self):
        d="{0:>6}".format(self.distance)
        c="{0:-<40}".format(self.commune.nom_commune+' '+ self.commune.ligne_5)
        return f"{d} km - {c} - ({self.commune.code_departement}) {self.commune.nom_departement}"
    
    
# ---------------------------------------------------------------------
    
communes=list()

print ('-------- Lancé !! ----------')

with open("communes-departement-region.csv",'r',encoding="utf8", newline='') as cvsFile:
    reader = csv.DictReader(cvsFile)
    for row in reader:
     
        try:
            lat=float(row['latitude'])
        except :
            lat=0
        
        try:
            lon=float(row['longitude'])
        except:
            lon=0
        if row['article']=="L'''" or row['article']=="":
            sep=""
        else:
            sep=" "
        c=commune(code_commune=row['code_commune_INSEE'],nom_commune=row['article']+sep+row['nom_commune'],ligne_5=row['ligne_5'],nom_commune_sans_accents=row['libelle_acheminement'],latitude=lat,longitude=lon,code_postal=row['code_postal'],nom_departement=row['nom_departement'],code_departement=row['code_departement'],nom_region=row['nom_region'],code_region=row['code_region'])
        communes.append(c)
        
    max_len_name=max(communes)
    max_len_name=len(max_len_name.nom_commune)
    
    print('==================> ',max_len_name)
    
print (len(communes), 'communes')
"""
r1=random.randint(0,len(communes))
c1=communes[r1].nom_commune
cp1=communes[r1].code_postal

r2=random.randint(0,len(communes))
c2=communes[r2].nom_commune
cp2=communes[r2].code_postal

dist=int(communes[r1]-communes[r2])


print (f"La distance à vol d'oiseau entre\n{c1}({cp1}) et {c2}({cp2})\nest de {dist} km.")
"""

fin=False
while fin==False:
    
    c=input('Nom de ville ==> ').upper()
    c= unicodedata.normalize("NFD", c)
    c=re.sub("[\u0300-\u036f]", "", c)
    " tout ça pour enlever les accents..."
    
    
    if c=="END" or c=="FIN" or c=="EXIT" or c=="":
        fin=True
        break
    else:
        # Ville connue ?
        ct=0
        while ct==0:
            homonymes=[]
            for cm in communes:
                if cm.nom_commune_sans_accents==c:
                    homonymes.append(cm)
                    ct=cm
                    
            if len(homonymes)>1:
                # il y a des homonymes
                print (f'de quel {ct.nom_commune_sans_accents} parle-t''on ?\n')
                i=1
                for cm in homonymes:
                    print(i,') ',cm)
                    i+=1
                j=-1
                while j<1 or j>i-1:
                    j=int(input('Numéro de votre choix ==> '))
                ct=homonymes[j-1]
                print('\nVous avez choisi :\n')
                
                
            if isinstance(ct,commune):
                print (f'{ct.nom_commune_sans_accents} ({ct.code_departement}-{ct.nom_departement})')
                
                lat="{:.{prec}f}".format(ct.latitude,prec=3)
                lon="{:.{prec}f}".format(ct.longitude,prec=3)
                if ct.latitude==0 and ct.longitude==0:
                    print ('Coordonnées GPS non disponibles ==> faites un autre choix.')
                    ct=1
                else:
                    print (f"Latitude : {lat} °N - Longitude : {lon} °E")
            else:
                print ('Ville inconnue !')
                ct=2


    # Demander la distance maxi
    if isinstance(ct,commune):
        d=float(input('Rayon de recherche (en km)==> '))
        print()
        proxima=[]
        for cm in communes:
            if cm!=ct and (cm-ct)<d:
                p=prox(round(cm-ct,1),cm)
                proxima.append(p)    
                # print(round(cm-ct,1),' km - ',cm)
        
        proxima.sort()
        for p in proxima:
            print(p)


        print ('\n===> soit',len(proxima),'communes trouvées à moins de',d,'km de',ct.nom_commune)      
print ('-------- Terminé ----------')

    