import re
import sys

from pdfplumber import open
import spacy

pdf_path, keywords_input, Formation_Demandee, Experience_Demandee = sys.argv[1:5]

with open(pdf_path) as pdf:
    cv_text = ""
    for page in pdf.pages:
        cv_text += page.extract_text()

keywords = [keyword.strip().lower() for keyword in keywords_input.split(",")]

nlp = spacy.load("fr_core_news_sm")
doc = nlp(cv_text)

# Compter le nombre de mots-clés présents dans le texte du CV
keyword_count = sum(1 for keyword in keywords if re.search(r'\b{}\b'.format(re.escape(keyword)), cv_text.lower()))

# Calculer le pourcentage d'existence des mots-clés
percentage_existence = (keyword_count / len(keywords)) * 100

# Utiliser des expressions régulières pour extraire les informations pertinentes
pattern_formation = r'(formations?)[\s\S]*?(\b\d{4}\b)[\s\S]*?(expériences?|experiences?)'
matches_formation = re.search(pattern_formation, cv_text, re.IGNORECASE)

if matches_formation:
    years_formation = re.findall(r'\b\d{4}\b', matches_formation.group())
    Formation = int(years_formation[-1]) - int(years_formation[-2]) if len(years_formation) >= 2 else 0
else:
    Formation = 0

pattern_experience = r'\((\d+)\s*(mois|ans|jours)(?:\s*et\s*(\d+)\s*jours)?'
matches_experience = re.findall(pattern_experience, cv_text)

total_days = sum(
    int(duree) * (30 if unite == 'mois' else 365 if unite == 'ans' else 1) for duree, unite, _ in matches_experience
)

modele_telephone = r'(?:\+|0[67])\d{0,3}[\s\d\(\)\-\+]*\d[\s\d\(\)\-\+]*\d[\s\d\(\)\-\+]*\d[\s\d\(\)\-\+]*\d[\s\d\(\)\-\+]*\d[\s\d\(\)\-\+]*\d[\s\d\(\)\-\+]*\d\b'
correspondances_telephone = re.findall(modele_telephone, cv_text)

# Calcul du pourcentage final
Final_percentage = percentage_existence
Formation_search = f"Bac+{Formation}"

if Formation_search.lower() == Formation_Demandee.lower():
    Final_percentage += 400

Final_percentage += round(min((total_days * 300) / float(Experience_Demandee), 300), 2)

# Afficher le pourcentage final
print(round(Final_percentage / 8, 2))
