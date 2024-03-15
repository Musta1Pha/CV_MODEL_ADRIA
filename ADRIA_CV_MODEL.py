import re
import sys

from pdfplumber import open
import spacy

pdf_path = sys.argv[1]
with open(pdf_path) as pdf:
    cv_text = ""
    for page in pdf.pages:
        cv_text += page.extract_text()

keywords_input = sys.argv[2]
Formation_Demandee = sys.argv[3]
Experience_Demandee = sys.argv[4]
keywords = [keyword.strip() for keyword in keywords_input.split(",")]

nlp = spacy.load("fr_core_news_sm")
doc = nlp(cv_text)

keyword_count = 0

for keyword in keywords:
    if keyword.lower() in [token.text.lower() for token in doc]:
        keyword_count += 1

percentage_existence = (keyword_count / len(keywords)) * 100

pattern_formation = r'(formations|formation)\s*[\s\S]*?(\b\d{4}\b)[\s\S]*?(expérience|expériences|experience|experiences)'
matches_formation = re.search(pattern_formation, cv_text, re.IGNORECASE | re.DOTALL)

if matches_formation:
    years_formation = re.findall(r'\b\d{4}\b', matches_formation.group())
    years_formation_update = years_formation[:-2]
    Formation = int(years_formation_update[1]) - int(years_formation_update[len(years_formation_update) - 2])

pattern_experience = r'\((\d+)\s*(mois|ans|jours)(?:\s*et\s*(\d+)\s*jours)?'
matches_experience = re.findall(pattern_experience, cv_text)

mois_list = []
annees_list = []
jours_list = []
year_to_days = 0
month_to_days = 0
days = 0

for match in matches_experience:
    duree, unite, jours = match
    if unite == 'mois':
        mois_list.append(int(duree))
    elif unite == 'ans':
        annees_list.append(int(duree))
    elif unite == 'jours':
        jours_list.append(int(duree))
    if jours:
        jours_list.append(int(jours))

for annee in annees_list:
    year_to_days += annee * 365

for mois in mois_list:
    month_to_days += mois * 30

for day in jours_list:
    days += day

total_days = month_to_days + year_to_days + days

modele_telephone = r'(?:\+|0[67])\d{0,3}[\s\d\(\)\-\+]*\d[\s\d\(\)\-\+]*\d[\s\d\(\)\-\+]*\d[\s\d\(\)\-\+]*\d[\s\d\(\)\-\+]*\d[\s\d\(\)\-\+]*\d[\s\d\(\)\-\+]*\d\b'
correspondances_telephone = re.findall(modele_telephone, cv_text)

if correspondances_telephone:
    chaine_resultat = ' '.join(correspondances_telephone)

Final_percentage = percentage_existence
Formation_search = f"Bac+{Formation}"

if Formation_search.lower() == Formation_Demandee.lower():
    Final_percentage += 400
Final_percentage += round(min((int(total_days) * 300) / float(Experience_Demandee), 300), 2)

# Output the final percentage value without any additional text
print(round(Final_percentage / 8, 2))


