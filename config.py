class Config:
    DEBUG = True
    # modifier le chemin ci-dessous pour avoir le chemin absolu de data.csv
    # dans le dossier opendata téléchargé depuis github
    # c'est nécessaire pour le déploiement des DAG
    mydata = '/Users/parduzizana/Documents/INFO_5A/Big_Data/opendata/data.csv'
    user = 'root'
    password='new_password'
    database='weatherApp'
