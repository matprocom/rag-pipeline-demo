import os
import json
import requests
import glob
from dotenv import load_dotenv

# Configuration
load_dotenv('API.env')
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"

DOSSIER_DATA = "data"
FICHIER_SORTIE = "rapport_final.md"

def extraire_et_resumer(texte, nom_fichier):
    """Envoie le texte à l'IA pour en extraire un JSON structuré."""
    print(f"  -> Analyse de {nom_fichier}...")
    prompt = (
        "Tu es un extracteur de données. Transforme ce texte en un objet JSON valide avec les clés :\n"
        "- 'faits' : liste des faits marquants.\n"
        "- 'donnees' : liste des données chiffrées (dates, prix, stats).\n"
        "- 'decisions' : liste des décisions prises.\n"
        "Ne renvoie QUE le JSON."
    )
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Texte :\n\n{texte}"}
        ],
        "temperature": 0.1
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        contenu = response.json()['choices'][0]['message']['content']
        contenu = contenu.replace("```json", "").replace("```", "").strip()
        return json.loads(contenu)
    except Exception as e:
        print(f"  ❌ Erreur sur {nom_fichier} : {e}")
        return {"faits": [texte[:500]], "donnees": [], "decisions": []}

def main():
    if not os.path.exists(DOSSIER_DATA):
        os.makedirs(DOSSIER_DATA)
        print(f"📁 Dossier '{DOSSIER_DATA}' créé. Placez vos fichiers .txt dedans.")
        return

    fichiers = glob.glob(f"{DOSSIER_DATA}/*.txt")
    if not fichiers:
        print("⚠️ Aucun fichier .txt trouvé dans le dossier 'data'.")
        return

    resultat_final = {"faits": [], "donnees": [], "decisions": []}

    for fichier in fichiers:
        with open(fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        # On traite le fichier
        json_resultat = extraire_et_resumer(contenu, os.path.basename(fichier))
        
        # On fusionne les résultats
        for cle in resultat_final.keys():
            if cle in json_resultat:
                resultat_final[cle].extend(json_resultat[cle])

    # Génération du rapport Markdown
    with open(FICHIER_SORTIE, 'w', encoding='utf-8') as f:
        f.write("# Rapport d'Analyse\n\n")
        
        f.write("## 📌 Faits Marquants\n")
        for fait in resultat_final['faits']:
            f.write(f"- {fait}\n")
            
        f.write("\n## 📊 Données Chiffrées\n")
        for donnee in resultat_final['donnees']:
            f.write(f"- {donnee}\n")
            
        f.write("\n## ✅ Décisions\n")
        for decision in resultat_final['decisions']:
            f.write(f"- {decision}\n")

    print(f"\n✅ Rapport généré : {FICHIER_SORTIE}")

if __name__ == "__main__":
    main()