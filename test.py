#Scraping Welcome to the Jungle
from bs4 import BeautifulSoup as bs
import requests 
import pandas as pd

wttj_url = 'https://www.welcometothejungle.com/fr/companies/datascientest/jobs/data-engineer-h-f-cdi_puteaux_DATAS_ZMLPerq'
page = requests.get(wttj_url)
soup = bs(page.text, "html.parser")


#Collecte des données d'une offre
def get_info(link):
    page = requests.get(link)
    soup = bs(page.text, "html.parser")

    company = soup.find('span', attrs = {'class' : "sc-dxcDKg hwAIog wui-text"}).text
    title = soup.find('h1', attrs = {'color': "white"}).text
    lieu = soup.find('span', attrs = {'class': "k2ldby-3 kuSacT"}).span.text
    contrat = soup.find('div', attrs = { 'role':"listitem"}).text
    try : 
        if soup.find("time").has_attr('datetime'):
            debut= soup.find("time").text
    except : 
        debut = "Non trouvé"

    spans = soup.find_all('span', attrs = {'class': "sc-bXCLTC kJcLKT"})
    education = spans[1].find_next("span").find_next("span").string 
    try :
        experience = spans[2].find_next("span").find_next("span").string 
    except : 
        experience = "non spécifié"
    
    col = soup.find("div", class_="sc-bXCLTC hBkEnu")
    #for i,each_div in enumerate(col.find_all("div")):
        #print(i, ':' ,each_div.text)
    taille = col.find_all("div")[2].text
    domaine = col.find_all("div")[3].text
    try : 
        profil = soup.find("section", id='profile-section').text
    except : 
        profil = "non spécifié"
    
    line=[company,domaine,taille,lieu,title,debut,contrat,education,experience,profil,link]
    return line

requests.get('https://www.welcometothejungle.com/fr/companies/datascientest/jobs/data-engineer-h-f-cdi_puteaux_DATAS_ZMLPerq')


#On teste sur une autre offre d'emploi
url2 = 'https://www.welcometothejungle.com/fr/companies/datascientest/jobs/data-analyst-h-f-cdi_puteaux'
requests.get(url2)


#On généralise pour toutes les offres d'emploi de Datascientest
jobs_list = []
for i in range(1,3):
    all_jobs = "https://www.welcometothejungle.com/fr/companies/datascientest/jobs?page="+str(i)
    page = requests.get(all_jobs)
    soup = bs(page.text,'html.parser')
    divs = soup.find_all('div',class_="sc-1peil1v-7 fTGJpK")
    for div in divs : 
        a = div.find("a")
        if ("/fr/companies" in a["href"]) and (a["href"] not in jobs_list):
            jobs_list.append(a["href"])
            
print(len(jobs_list))
jobs_list


base = "https://www.welcometothejungle.com"
df = pd.DataFrame(columns=["Company","Domaine","Taille","Lieu","Titre","Debut","Contrat","Education","Experience","Profil", "Link"])

for i,job in enumerate(jobs_list) : 
    row = requests.get(base+job)
    a = pd.DataFrame([row],columns=["Company","Domaine","Taille","Lieu","Titre","Debut","Contrat","Education","Experience","Profil","Link"])
    #print(i,':',row)
    df = pd.concat([df,a],ignore_index=True)
    df



#On généralise à plusieurs entreprises
company_list = ["datascientest","thales"]
for company in company_list : 
    for i in range(1,10):
        all_jobs = "https://www.welcometothejungle.com/fr/companies/"+company+"/jobs?page="+str(i)
        page = requests.get(all_jobs)
        soup = bs(page.text,'html.parser')
        divs = soup.find_all('div',class_="sc-1peil1v-7 fTGJpK")
        for div in divs : 
            a = div.find("a")
            if ("/fr/companies" in a["href"]) and (a["href"] not in jobs_list):
                jobs_list.append(a["href"])
            
base = "https://www.welcometothejungle.com"
df = pd.DataFrame(columns=["Company","Domaine","Taille","Lieu","Titre","Debut","Contrat","Education","Experience","Profil","Link"])

for job in jobs_list : 
    row = requests.get(base+job)
    a = pd.DataFrame([row],columns=["Company","Domaine","Taille","Lieu","Titre","Debut","Contrat","Education","Experience","Profil","Link"])
    df = pd.concat([df,a],ignore_index=True)

df

df.to_csv(r'./welcome_to_the_jungle.csv', index=False, header=True)


#SELMA HADJ KHELIFA B3 CDA