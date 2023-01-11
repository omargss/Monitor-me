import json

with open("config.json", "r") as f:
        data = json.load(f)

    # Ajouter la nouvelle machine au tableau de machines
        data["machines"].append({
            "hostname": "cyril2@tse.net",
            "port": 22000,
            "username": "cyril",
            "password": "mdp"
    })

    # Enregistrer les données modifiées dans le fichier JSON

with open("config.json", "w") as f:
        json.dump(data, f, indent=4)