import re
import sys

pdf_path, keywords_input, Formation_Demandee, Experience_Demandee = sys.argv[1:5]

# Ouvrir le fichier PDF et extraire le texte
with open(pdf_path, "rb") as pdf_file:
    cv_text = pdf_file.read().decode("utf-8", "ignore")

# Convertir les mots-clés en une liste de mots en minuscules
keywords = [keyword.strip().lower() for keyword in keywords_input.split(",")]

# Compter le nombre de mots-clés présents dans le texte du CV
keyword_count = sum(keyword in cv_text.lower() for keyword in keywords)

# Calculer le pourcentage d'existence des mots-clés
percentage_existence = (keyword_count / len(keywords)) * 100

# Utiliser des expressions régulières pour extraire les informations pertinentes
matches_formation = re.search(r'\bformations?\b.*?(\d{4})', cv_text, re.IGNORECASE)
years_formation = [int(year) for year in re.findall(r'\b\d{4}\b', matches_formation.group())] if matches_formation else []
Formation = years_formation[-1] - years_formation[-2] if len(years_formation) >= 2 else 0

matches_experience = re.findall(r'\((\d+)\s*(?:mois|ans|jours)', cv_text)
total_days = sum(int(match) * (30 if 'mois' in match else 365 if 'ans' in match else 1) for match in matches_experience)

matches_telephone = re.findall(r'(?:\+|0[67])\d{0,3}[\s\d\(\)\-\+]{7,}\d\b', cv_text)
correspondances_telephone = ' '.join(matches_telephone) if matches_telephone else ''

Final_percentage = percentage_existence + round(min((total_days * 300) / float(Experience_Demandee), 300), 2)
Final_percentage += 400 if f"Bac+{Formation}" == Formation_Demandee.lower() else 0

# Afficher le pourcentage final
print(round(Final_percentage / 8, 2))
