import csv
import os

def format_nombre(number):
    return '{:,}'.format(number).replace(',', ' ')

def inverse_format(format_nombre):
    return int(format_nombre.replace(' ', '').replace(',', ''))

# Créer des dossiers s'ils n'existent pas
output_folders = ["html", "css", "js"]
for folder in output_folders:
    os.makedirs(folder, exist_ok=True)

# Lecture des données des dépenses
depenses_dep = open("dataset/depenses-ministere-culture_dep.csv", 'r', encoding='utf-8')
dico_depenses_dep = csv.DictReader(depenses_dep)

# Création d'un dictionnaire pour stocker les informations
departements_data = {}

for ligne in dico_depenses_dep:
    code_departement = ligne["code_insee"]
    nom_departement = ligne["libelle_geographique"]
    
    # Vérifier si le département existe déjà dans le dictionnaire
    if code_departement not in departements_data:
        departements_data[code_departement] = {"nom_departement": nom_departement}

    # Ajouter les données des dépenses au dictionnaire
    departements_data[code_departement]["total_depenses"] = format_nombre(departements_data.get(code_departement, {}).get("total_depenses", 0) + int(ligne["total"]))
    departements_data[code_departement]["cout_fonctionnement"] = format_nombre(departements_data.get(code_departement, {}).get("cout_fonctionnement", 0) + int(ligne["fonctionnement"]))
    departements_data[code_departement]["investissement"] = format_nombre(departements_data.get(code_departement, {}).get("investissement", 0) + int(ligne["investissement"]))

# Lecture des données salariés
salaries_dep = open("dataset/salaries-secteurs-culturels_dep.csv", 'r', encoding='utf-8')
dico_salaries_dep = csv.DictReader(salaries_dep)

for ligne in dico_salaries_dep:
    code_departement = ligne["code_insee"]

    # Vérifier si le département existe déjà dans le dictionnaire
    if code_departement not in departements_data:
        departements_data[code_departement] = {"nom_departement": ligne["libelle_geographique"]}

    # Ajouter le nombre de salariés actifs au dictionnaire
    departements_data[code_departement]["nombre_salaries_actifs"] = format_nombre(departements_data.get(code_departement, {}).get("nombre_salaries_actifs", 0) + int(ligne["nombre_de_salaries_actifs_des_secteurs_culturels_marchands"]))

# Trier les départements par ordre croissant des codes postaux
departements_data_sorted = dict(sorted(departements_data.items(), key=lambda x: int(x[0]) if x[0].isdigit() else float('inf')))

# Génération de la page principale avec des liens vers les fichiers détaillés
index_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>SAE 15 - Traiter les données</title>
    <link rel="stylesheet" type="text/css" href="style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

</head>
<body>
    <h1>Statistiques sur la Culture en France - Page Principale</h1>
    
    <p>Ce site prends ses données de deux fichiers csv, l'un portant sur les dépenses du ministère de la culture par département
    et l'autre sur le nombre de salariés du secteur culturel par département. Vous trouverez donc sur cette page principale un tableau 
    qui regroupe ces données ainsi qu'un graphique en fin de page pour comparer ces deux données. Chaque département possède une page 
    un peu plus détaillée où figure quelques données supplémementaires non affichées dans la page principale.</p>

    <!-- Ajout du champ de recherche -->
    <label for="search">Rechercher : </label>
    <input type="text" id="search" oninput="searchTable()" placeholder="Nom du département">

    <table border="1">
        <tr>
            <th>Département</th>
            <th>Nom du Département</th>
            <th>Total des Dépenses</th>
            <th>Nombre de Salariés Actifs</th>
        </tr>
"""

# Ajout des lignes du tableau avec des liens vers les pages détaillées
for code_departement, data in departements_data_sorted.items():
    nom_departement = data["nom_departement"]
    total_depenses = data.get("total_depenses", 0)
    nombre_salaries = data.get("nombre_salaries_actifs", 0)

    index_html += f"""
        <tr class="filterable">
            <td><a href='departement_{code_departement}.html'>{code_departement}</a></td>
            <td>{nom_departement}</td>
            <td>{total_depenses} €</td>
            <td>{nombre_salaries}</td>
        </tr>
    """

index_html += """
    </table>
    
    <!-- Ajout du graphique combiné -->
    <div class="graph-container">
        <canvas id="graph" class="graph-canvas"></canvas>
    </div>

    <script src="graph.js"></script>

    <!-- Ajout du footer -->
    <footer>
        <p>Réalisé par CHADLI Jawed en BUT1 R&T dans le cadre de la SAE 15 encadrée par M.GIRARDOT</p>
    </footer>
</body>
</html>
"""

with open(os.path.join("html", "index.html"), "w", encoding="utf-8") as main_page:
    main_page.write(index_html)

# Génération des pages détaillées
for code_departement, data in departements_data_sorted.items():
    departement_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SAE 15 - Traiter les données</title>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body>
        <h1>Statistiques sur la Culture en France - {nom_departement} - {code_departement}</h1>
        <table border="1">
            <tr>
                <th>Information</th>
                <th>Valeur</th>
            </tr>
            <tr>
                <td>Nom du Département</td>
                <td>{data["nom_departement"]}</td>
            </tr>
            <tr>
                <td>Total des Dépenses</td>
                <td>{data.get("total_depenses", 0)} €</td>
            </tr>
            <tr>
                <td>Investissement</td>
                <td>{data.get("investissement", 0)} €</td>
            </tr>
            <tr>
                <td>Coût de Fonctionnement</td>
                <td>{data.get("cout_fonctionnement", 0)} €</td>
            </tr>
            <tr>
                <td>Nombre de Salariés Actifs</td>
                <td>{data.get("nombre_salaries_actifs", 0)}</td>
            </tr>
        </table>

        <br>
        <a href="index.html">Retour à la page principale</a>
    </body>
    </html>
    """

    with open(os.path.join("html", f"departement_{code_departement}.html"), "w", encoding="utf-8") as departement:
        departement.write(departement_html)

# Génération du fichier CSS
css_style = """
body {
    font-family: Arial, sans-serif;
    background-color: #f2f2f2;
}

h1 {
    color: #006600;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th, td {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

th {
    background-color: #4CAF50;
    color: white;
}

a {
    color: #0066cc;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

label {
    font-weight: bold;
    margin-top: 10px;
}

input[type=text] {
    width: 200px;
    padding: 5px;
    margin-top: 5px;
    margin-bottom: 10px;
}

.graph-container {
    background-color: #f0f0f0;
    padding: 20px;
}

.graph-canvas {
    width: 100%;
    height: auto;
}

footer {
    margin-top: 20px;
    text-align: center;
    color: #666;
}
"""

# Écriture du fichier CSS
with open(os.path.join("css", "style.css"), "w", encoding="utf-8") as css:
    css.write(css_style)

# Génération du fichier JavaScript pour la barre de recherche
search_js = """
function searchTable() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    table = document.querySelector("table");
    tr = table.getElementsByTagName("tr");

    for (i = 1; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1]; // Index 1 corresponds to the column with department names
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}
"""

# Écriture du fichier JavaScript
with open(os.path.join("js", "search.js"), "w", encoding="utf-8") as search:
    search.write(search_js)

labels_depenses = []
data_depenses = []
data_salaries = []

totalDepensesGlobal = sum(inverse_format(data.get('total_depenses', '0')) for data in departements_data_sorted.values())
totalSalariesGlobal = sum(inverse_format(data.get('nombre_salaries_actifs', '0')) for data in departements_data_sorted.values())

for code_departement, data in departements_data_sorted.items():
    nom_departement = data["nom_departement"]
    totalDepenses = inverse_format(data.get('total_depenses', '0'))
    pourcentageDepenses = (totalDepenses / totalDepensesGlobal) * 100
    nombreSalaries = inverse_format(data.get('nombre_salaries_actifs', '0'))
    pourcentageSalaries = (nombreSalaries / totalSalariesGlobal) * 100

    labels_depenses.append(f'"{nom_departement}"')
    data_depenses.append((totalDepenses / totalDepensesGlobal) * 100)  # Pourcentage des dépenses
    data_salaries.append((nombreSalaries / totalSalariesGlobal) * 100)  # Pourcentage des salariés
    
# Création du fichier JavaScript pour le graphique
graph_js = f"""
var ctxCombined = document.getElementById('combinedChart').getContext('2d');
var combinedChart = new Chart(ctxCombined, {{
    type: 'bar',
    data: {{
        labels: [{", ".join(labels_depenses)}],
        datasets: [
            {{
                label: 'Pourcentage de Dépenses',
                data: [{", ".join(map(str, data_depenses))}],
                backgroundColor: 'rgba(255, 99, 132, 0.7)',
            }},
            {{
                label: 'Pourcentage de Salariés',
                data: [{", ".join(map(str, data_salaries))}],
                backgroundColor: 'rgba(54, 162, 235, 0.7)',
            }},
        ],
    }},
    options: {{
        title: {{
            display: true,
            text: 'Répartition des Dépenses et des Salariés par Département en Pourcentage',
        }},
        scales: {{
            yAxes: [{{
                ticks: {{
                    beginAtZero: true,
                    max: 100,
                }},
                scaleLabel: {{
                    display: true,
                    labelString: 'Pourcentage (%)',
                }},
            }}],
        }},
    }},
}});
"""

# Écriture du fichier JavaScript pour le graphique combiné
with open(os.path.join("js", "graph.js"), "w", encoding="utf-8") as graph:
    graph.write(graph_js)

print("Fichiers HTML, CSS, et JS générés avec succès.")