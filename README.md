\# RAG Pipeline Démo 📊



Ce projet est un pipeline de traitement de données automatisé conçu pour nettoyer, analyser et synthétiser de gros volumes de données textuelles.



\## 🚀 Fonctionnalités

\- \*\*Extraction\*\* : Lecture de fichiers JSON ou TXT.

\- \*\*Nettoyage\*\* : Suppression des balises inutiles (HTML, Markdown, etc.).

\- \*\*Analyse IA\*\* : Utilisation de l'API DeepSeek pour extraire les faits, décisions et données chiffrées.

\- \*\*Déduplication\*\* : Fusion intelligente sans doublons (SHA-256).

\- \*\*Génération\*\* : Création d'un rapport Markdown structuré.



\## 🛠️ Installation

1\. Clonez ce dépôt.

2\. Installez les dépendances : `pip install -r requirements.txt`

3\. Créez un fichier `API.env` avec votre clé : `DEEPSEEK\_API\_KEY=votre\_cle\_ici`

4\. Placez vos fichiers de données dans le dossier `data/`.

5\. Lancez le script : `python pipeline.py`



\## 💡 Cas d'usage

Idéal pour les entreprises souhaitant automatiser la synthèse de réunions, l'analyse de feedbacks clients ou l'extraction de connaissances à partir de documentation interne.

