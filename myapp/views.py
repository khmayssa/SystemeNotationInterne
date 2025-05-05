from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import pandas as pd
import os
from django.views.generic import TemplateView
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render




from .forms import (
    ColumnSelectionForm,
    BivariateColumnSelectionForm,
    MultipleColumnSelectionForm,
    DataTreatmentForm,
)
from .analysis_functions import *
from .models import *
import pickle
import base64
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from datetime import datetime


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(
                    "index"
                )  # Rediriger vers la page d'accueil ou toute autre page après la connexion
    else:
        form = AuthenticationForm()
        messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, "login.html", {"form": form, "messages": messages})


#@login_required
import pandas as pd
from django.shortcuts import render
from io import StringIO

import pandas as pd
from io import StringIO
from django.shortcuts import render

import pandas as pd
from django.shortcuts import render
from io import StringIO

def data_overview_view(request):
    if "uploaded_data" not in request.session:
        # Chemin vers le fichier Excel
        static_file_path = "BD_SNI.xlsx"
        # Lire le fichier Excel dans un DataFrame
        uploaded_data = pd.read_excel(static_file_path)
        # Convertir le DataFrame en JSON et le stocker dans la session
        request.session["uploaded_data"] = uploaded_data.to_json()
    else:
        # Récupérer les données JSON depuis la session et les convertir en DataFrame
        uploaded_data_json = request.session["uploaded_data"]
        uploaded_data = pd.read_json(StringIO(uploaded_data_json))

    # Calculer la forme des données pour l'affichage
    formatted_shape = f"Nombre de lignes : {uploaded_data.shape[0]}, Nombre de colonnes : {uploaded_data.shape[1]}"

    # Formater les en-têtes en gras pour l'affichage dans <pre>
    def format_header(col):
        return f"<b>{col}</b>"  # Encapsuler les noms des colonnes dans <b>

    # Créer une copie du DataFrame avec des en-têtes en gras pour data_full
    temp_df = uploaded_data.copy()
    temp_df.columns = [format_header(col) for col in temp_df.columns]

    # Convertir le DataFrame en texte pour l'affichage dans <pre>
    data_full = temp_df.to_string()

    # Passer les données, la forme des données et data_full au template
    return render(request, "overview.html", {
        "data": uploaded_data.to_dict(orient="records"),  # Utiliser le DataFrame original
        "formatted_shape": formatted_shape,
        "data_full": data_full,  # Pour <pre id="tab">
    })


# @login_required
def plot_selection_view(request):
#     if "uploaded_data" in request.session:
#
#         uploaded_data = pd.read_json(request.session["uploaded_data"])
#
#         plots = request.session.get("plot", [])
#         target_column = request.session.get("target_column")
#         categorical_cols, numeric_cols = decompose_variables(uploaded_data)
#
#         selected_numeric_column = None
#         selected_categorical_column = None
#
#         if request.method == "POST":
#             plot_dir = "media/plots/"
#             os.makedirs(plot_dir, exist_ok=True)
#
#             # Pour les colonnes numériques
#             if "plot_numeric_distribution" in request.POST:
#                 form = ColumnSelectionForm(request.POST, columns=numeric_cols)
#                 if form.is_valid():
#                     selected_numeric_column = form.cleaned_data["column"]
#                     filename = os.path.join(plot_dir, "numeric_distribution.png")
#                     plot_numeric_distribution(uploaded_data, selected_numeric_column, filename)
#                     plot_path = f"/media/plots/numeric_distribution.png"
#                     plots.append(plot_path)
#
#             # Pour les colonnes catégoriques
#             if "plot_categorical_distribution" in request.POST:
#                 form = ColumnSelectionForm(request.POST, columns=categorical_cols)
#                 if form.is_valid():
#                     selected_categorical_column = form.cleaned_data["column"]
#                     filename = os.path.join(plot_dir, "categorical_distribution.png")
#                     plot_categorical_distribution(uploaded_data, selected_categorical_column, filename)
#                     plot_path = f"/media/plots/categorical_distribution.png"
#                     plots.append(plot_path)
#
#             if "plot_pie_chart" in request.POST:
#                 if target_column and target_column in uploaded_data.columns:
#                     # Générer le Pie Chart pour la colonne cible
#                     filename = os.path.join(plot_dir, "pie_chart.png")
#                     print("Target column for pie chart:", target_column)  # Debug
#                     plot_pie_chart(uploaded_data, target_column, filename)
#                     plot_path = f"/media/plots/pie_chart.png"
#                     plots.append(plot_path)
#
#             request.session["plots"] = plots
#
#         # Passer la colonne sélectionnée aux formulaires
#         numeric_column_selection_form = ColumnSelectionForm(columns=numeric_cols, selected_column=selected_numeric_column)
#         categorical_column_selection_form = ColumnSelectionForm(columns=categorical_cols, selected_column=selected_categorical_column)
#
#         return render(
#             request,
#             "plot.html",
#             {
#                 "numeric_column_selection_form": numeric_column_selection_form,
#                 "categorical_column_selection_form": categorical_column_selection_form,
#                 "categorical_distribution_plots": [
#                     plot for plot in plots if "categorical_distribution" in plot
#                 ],
#                 "pie_chart_plots": [plot for plot in plots if "pie_chart" in plot],
#                 "numeric_distribution_plots": [
#                     plot for plot in plots if "numeric_distribution" in plot
#                 ],
#                 "target_column": target_column,
#                 "plots": plots
#             },
#         )
#
     return redirect("overview")

# @login_required
def feature_selection_view(request):
#     if "uploaded_data" in request.session:
#         uploaded_data = pd.read_json(request.session["uploaded_data"])

#         # Récupérer la colonne cible à partir de la session
#         target_column = request.session.get("target_column")
#         message = None  # Initialisation du message à None
#         anova_results = None
#         iv_results = None
#         correlation_plot = None

#         if request.method == "POST":
#             # Vérifier si une colonne doit être supprimée
#             if "column_to_remove" in request.POST:
#                 # Suppression de colonne
#                 column_to_remove = request.POST.get("column_to_remove")
#                 if column_to_remove in uploaded_data.columns:
#                     uploaded_data = uploaded_data.drop(columns=[column_to_remove])
#                     # Mettre à jour les données dans la session après suppression
#                     request.session["uploaded_data"] = uploaded_data.to_json()
#                     message = f"La colonne {column_to_remove} a été supprimée."
#                 else:
#                     message = f"La colonne {column_to_remove} n'existe pas."

#             # Effectuer les tests ANOVA, IV, et générer la matrice de corrélation si une colonne cible est présente
#             elif target_column:
#                 anova_results = chi2_test(uploaded_data, target_column)
#                 iv_results = calculate_iv_table_with_binning(uploaded_data, target_column)
#                 correlation_matrix(uploaded_data, plot=True)
#                 correlation_plot = "/media/plots/correlation_matrix.png"
        
#         return render(
#             request,
#             "feature_selection.html",
#             {
#                 "uploaded_data": uploaded_data,
#                 "anova_results": anova_results,
#                 "iv_results": iv_results,
#                 "correlation_plot": correlation_plot,
#                 "current_column": target_column,  # Passer la colonne cible à la vue
#                 "message": message,  # Passer le message à la vue
#             },
#         )
     return redirect("upload_file")


# @login_required
import pandas as pd
from django.shortcuts import render
from io import StringIO

def score_autonomie_financiere(ratio):
    if ratio < 0:
        return 0
    elif ratio < 0.10:
        return 5
    elif ratio < 0.2:
        return 10
    elif ratio < 0.4:
        return 15
    else:
        return 20

def score_rentabilite_nette(ratio):
    if ratio < 0:
        return 0
    elif ratio < 0.05:
        return 5
    elif ratio < 0.10:
        return 10
    elif ratio < 0.20:
        return 15
    else:
        return 20

def score_liquidite_generale(ratio):
    if ratio < 0:
        return 0
    elif ratio < 1:
        return 10
    elif ratio < 2:
        return 15
    else:
        return 20

def score_endettement(ratio):
    if ratio < 0:
        return 0
    elif ratio > 5:
        return 0
    elif ratio >= 2.5:
        return 5
    else:
        return 20

def feature_selection_view(request):
    return render(request, "feature_selection.html")
 

# @login_required
def modeling_view(request):
#     if "uploaded_data" in request.session:
#         uploaded_data = pd.read_json(request.session["uploaded_data"])
#         target = None
#         features_selected = []
#         summary_table = None
#         reg = None
#         performance_metrics = None
#         confusion_matrix_plot = None
#         X_train = X_test = y_train = y_test = None

#         if request.method == "POST":
#             target_selection_form = ColumnSelectionForm(
#                 request.POST, columns=uploaded_data.columns
#             )
#             feature_selection_form = MultipleColumnSelectionForm(
#                 request.POST, columns=uploaded_data.columns
#             )

#             if target_selection_form.is_valid() and feature_selection_form.is_valid():
#                 target = target_selection_form.cleaned_data["column"]
#                 features_selected = feature_selection_form.cleaned_data["columns"]

#                 # Remove target from features_selected if present
#                 if target in features_selected:
#                     features_selected.remove(target)

#                 # Store target and selected features in session
#                 request.session["selected_target"] = target
#                 request.session["selected_features"] = features_selected

#                 if "model_with_balance" in request.POST:
#                     summary_table, reg, X_train, X_test, y_train, y_test = (
#                         modelwithbalance(uploaded_data, target, features_selected)
#                     )
#                     request.session["model"] = base64.b64encode(
#                         pickle.dumps(reg)
#                     ).decode("utf-8")
#                     request.session["X_train"] = X_train.to_json()
#                     request.session["X_test"] = X_test.to_json()
#                     request.session["y_train"] = y_train.to_json()
#                     request.session["y_test"] = y_test.to_json()
#                     request.session["model_columns"] = X_train.columns.tolist()

#                 elif "model_without_balance" in request.POST:
#                     summary_table, reg, X_train, X_test, y_train, y_test = (
#                         modelwithoutbalance(uploaded_data, target, features_selected)
#                     )
#                     request.session["model"] = base64.b64encode(
#                         pickle.dumps(reg)
#                     ).decode("utf-8")
#                     request.session["X_train"] = X_train.to_json()
#                     request.session["X_test"] = X_test.to_json()
#                     request.session["y_train"] = y_train.to_json()
#                     request.session["y_test"] = y_test.to_json()
#                     request.session["model_columns"] = X_train.columns.tolist()

#             # Récupération du modèle et des données d'entraînement/test stockés dans la session
#             if "model" in request.session:
#                 reg = pickle.loads(base64.b64decode(request.session["model"]))
#                 X_train = pd.read_json(request.session["X_train"])
#                 X_test = pd.read_json(request.session["X_test"])
#                 y_train = pd.read_json(request.session["y_train"], typ="series")
#                 y_test = pd.read_json(request.session["y_test"], typ="series")

#             if reg is not None:
#                 if "show_metrics" in request.POST:
#                     metrics_set = request.POST.get("metrics_set")
#                     if metrics_set == "train":
#                         performance_metrics = print_performance_metrics(
#                             reg, X_train, y_train, "Train"
#                         )
#                         confusion_matrix_plot = plot_confusion_matrix(
#                             reg, X_train, y_train, "Train"
#                         )
#                     elif metrics_set == "test":
#                         performance_metrics = print_performance_metrics(
#                             reg, X_test, y_test, "Test"
#                         )
#                         confusion_matrix_plot = plot_confusion_matrix(
#                             reg, X_test, y_test, "Test"
#                         )
#                 else:
#                     performance_metrics = None
#                     confusion_matrix_plot = None

#         else:
#             target_selection_form = ColumnSelectionForm(columns=uploaded_data.columns)
#             feature_selection_form = MultipleColumnSelectionForm(
#                 columns=uploaded_data.columns
#             )

#         return render(
#             request,
#             "modeling.html",
#             {
#                 "target_selection_form": target_selection_form,
#                 "feature_selection_form": feature_selection_form,
#                 "summary_table": (
#                     summary_table.to_dict("records")
#                     if summary_table is not None
#                     else None
#                 ),
#                 "performance_metrics": performance_metrics,
#                 "confusion_matrix_plot": confusion_matrix_plot,
#             },
#         )
    return redirect("upload_file")


import pandas as pd
import numpy as np
#import statsmodels.api as sm # type: ignore
from joblib import Parallel, delayed
import base64
import pickle
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Include the stepwise regression functions here (include_all_levels, detect_categorical_vars, compute_p_value, stepwise_selection)

import base64
import pickle
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from sklearn.model_selection import train_test_split

@login_required
def modeling_view(request):
    # if "uploaded_data" in request.session:
#     uploaded_data = pd.read_json(request.session["uploaded_data"])
#     target_column = request.session.get("target_column")
#     summary_table = None
#     reg = None
#     performance_metrics = None
#     confusion_matrix_plot = None
#     X_train = X_test = y_train = y_test = None
#     selected_features = None  # Initialisation ici

#     if request.method == "POST" and "train_model" in request.POST:
#         if target_column and target_column in uploaded_data.columns:
#             target = target_column
#             features_selected = [col for col in uploaded_data.columns if col != target]

#             # Extract feature set and target
#             X = uploaded_data[features_selected]
#             y = uploaded_data[target]

#             # Preprocess data before feature selection
#             X_preprocessed, preprocessor = preprocess_data(X)

#             # Automatic feature selection using stepwise_selection
#             if "auto_selection" in request.POST:
#                 selected_features = stepwise_selection(
#                     pd.DataFrame(X_preprocessed, columns=preprocessor.get_feature_names_out()), y)
#                 X_preprocessed = pd.DataFrame(X_preprocessed, columns=preprocessor.get_feature_names_out())[selected_features]
                
#                 print("Forme du DataFrame transformé :", X_preprocessed.shape)
#                 # Save selected features to session for future use
#                 # Convert Index to list if needed
#                 if isinstance(selected_features, pd.Index):
#                     selected_features = selected_features.tolist()
#                 request.session["selected_features"] = selected_features
#                 print("Selected features after stepwise selection:", selected_features)

#             # Split the data
#             X_train, X_test, y_train, y_test = train_test_split(X_preprocessed, y, test_size=0.2, random_state=42)

#             # Call the appropriate modeling function
#             if "model_with_balance" in request.POST:
#                 summary_table, reg, X_train, X_test, y_train, y_test = modelwithbalance(uploaded_data, target, features_selected)
            
#             print("Shapes after balancing and encoding:")
#             print("X_train shape:", X_train.shape)
#             print("X_test shape:", X_test.shape)
#             print("y_train shape:", y_train.shape)
#             print("y_test shape:", y_test.shape)
            
#             # Check if summary_table is None and handle it
#             if summary_table is None:
#                 summary_table = pd.DataFrame()_

    return redirect("overview")



import pandas as pd
from io import StringIO
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required




    
from django.shortcuts import render, redirect
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse
import os
from django.conf import settings
from io import StringIO



from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc
import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
from django.conf import settings
from django.shortcuts import render, redirect
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
import plotly.express as px
import json 
from django.http import JsonResponse



def pd_view(request):
    if "uploaded_data" in request.session:
        uploaded_data_json = StringIO(request.session["uploaded_data"])
        df = pd.read_json(uploaded_data_json)
        print("Données chargées")

      
    
        return render(
            request,
            "pd.html",
            {

            }
        )
    return redirect("overview")




import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import classification_report, confusion_matrix, mean_absolute_error, mean_squared_error, r2_score
from io import StringIO

import pandas as pd
import numpy as np
import io
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, confusion_matrix, classification_report
from io import StringIO




def lgd_view(request):
    # Vérifier si les données ont été envoyées dans la session
    if "uploaded_data" in request.session:
        # Charger les données JSON depuis la session
        uploaded_data_json = StringIO(request.session["uploaded_data"])
        df = pd.read_json(uploaded_data_json)
        print("Données chargées")

       
        # Passer les résultats au template
        return render(request)

    return render(request, 'lgd.html')


import numpy as np
import pandas as pd


  


import pandas as pd
from io import StringIO
from django.shortcuts import render

import pandas as pd
from io import StringIO
from django.shortcuts import render


    
from django.shortcuts import render, redirect
import pandas as pd
from io import StringIO

def ead_view(request):
        # Vérifier si des données ont été téléchargées dans la session
        if "uploaded_data" in request.session:
            uploaded_data_json = StringIO(request.session["uploaded_data"])
            df = pd.read_json(uploaded_data_json)
            print("Données chargées :", df.head())  # Affiche les premières lignes des données

            
        return render(request, 'ead.html', {'message': "Une erreur est survenue lors du traitement des données."})




from django.http import JsonResponse
import pandas as pd
import numpy as np
from io import StringIO


from django.shortcuts import render
import pandas as pd
import numpy as np
from scipy.stats import norm

import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

def evaluation_view(request):
     return render(request, 'evaluation.html')
    
def vision360_view(request):
# try:
#     # Récupérer les données depuis la session
#     id_ead_list = request.session.get('id_ead_list', [])
#     id_pd2024_list = request.session.get('id_pd2024_list', [])
#     id_lgd_list = request.session.get('id_lgd_list', [])

#     # Vérifier si les données sont disponibles
#     if not id_ead_list or not id_pd2024_list or not id_lgd_list:
#         return render(request, 'vision360.html', {'message': "Les données nécessaires ne sont pas disponibles."})

#     # Convertir les listes en DataFrames
#     df_ead = pd.DataFrame(id_ead_list, columns=['id', 'ead'])
#     df_pd = pd.DataFrame(id_pd2024_list, columns=['id', 'pd'])
#     df_lgd = pd.DataFrame(id_lgd_list, columns=['id', 'lgd'])

#     # Fusionner les DataFrames sur la colonne 'id'
#     df_combined = df_ead.merge(df_pd, on='id', how='left').merge(df_lgd, on='id', how='left')

#     # Remplacer 'N/A' par NaN dans les colonnes 'pd', 'lgd' et 'ead' (sans chained assignment warning)
#     df_combined = df_combined.replace({'pd': {'N/A': np.nan},
#                                        'lgd': {'N/A': np.nan},
#                                        'ead': {'N/A': np.nan}})

#     # Convertir en float
#     df_combined['pd'] = df_combined['pd'].astype(float)
#     df_combined['lgd'] = df_combined['lgd'].astype(float)
#     df_combined['ead'] = df_combined['ead'].astype(float)

#     # Calculer les moyennes en ignorant NaN
#     mean_pd = df_combined['pd'].mean()
#     mean_lgd = df_combined['lgd'].mean()
#     mean_ead = df_combined['ead'].mean()

#     # Remplir les NaN avec la moyenne
#     df_combined['pd'] = df_combined['pd'].fillna(mean_pd)
#     df_combined['lgd'] = df_combined['lgd'].fillna(mean_lgd)
#     df_combined['ead'] = df_combined['ead'].fillna(mean_ead)

#     # Conversion de la PD en proportion
#     df_combined['PD'] = df_combined['pd'] / 100  # de % à proportion (0-1)

#     # Calcul de l'ECL (Expected Credit Loss)
#     df_combined['ECL'] = df_combined['PD'] * df_combined['lgd'] * df_combined['ead']

#     # Valeur du quantile à 99.9% pour UL
#     z_999 = norm.ppf(0.999)

#     # Facteur de corrélation rho
#     rho = 0.15

#     # Fonction pour calculer UL par ligne
#     def calculate_UL(row, z_999, rho):
#         pd = row['PD']
#         lgd = row['lgd']
#         ead = row['ead']
#         ul = ead * lgd * (norm.cdf((norm.ppf(pd) + np.sqrt(rho) * z_999) / np.sqrt(1 - rho)) - pd)
#         return ul

#     # Application du calcul UL
#     df_combined['UL'] = df_combined.apply(calculate_UL, axis=1, z_999=z_999, rho=rho)

#     # Taux de provisionnement
#     df_combined['taux_provisionnement'] = df_combined['ECL'] / df_combined['ead'] * 100

#     # Facteur de corrélation rho
#     rho = 0.15
#     df_combined['rho'] = rho 

#     # Fonction de calcul de K (extrait de ton code)
#     def calculate_K(PD, LGD, rho):
#         if PD >= 1.0 or PD <= 0.0:
#             return np.nan
#         z_PD = norm.ppf(PD)
#         z_999 = norm.ppf(0.999)
#         num = z_PD + np.sqrt(rho) * z_999
#         denom = np.sqrt(1 - rho)
#         return LGD * norm.cdf(num / denom)

#     # Calcul de K
#     df_combined['K'] = df_combined.apply(lambda row: calculate_K(row['PD'], row['lgd'], row['rho']), axis=1)

#     # Remplacer les NaN de K par 0
#     df_combined['K'] = df_combined['K'].fillna(0)

#     # Calcul de RWA et Capital Requis
#     df_combined['RWA'] = df_combined['K'] * df_combined['ead'] * 12.5
#     df_combined['fonds_propres'] = df_combined['RWA'] * 0.08

#     df_combined["level"], df_combined["comment"] = zip(
#         *df_combined["pd"].apply(lambda pd_value: get_risk_level_and_comment(pd_value / 100))
#     )

#     # Affichage pour debug
#     print("Liste combinée id/PD/LGD/EAD/ECL/UL/RWA/Fonds propres :", df_combined)

#     # Arrondir les colonnes aux formats souhaités
#     df_combined['id'] = df_combined['id'].astype(int)
#     df_combined['pd'] = df_combined['pd'].round(3)
#     df_combined['lgd'] = df_combined['lgd'].round(3)
#     df_combined['ead'] = df_combined['ead'].round(3)
#     df_combined['ECL'] = df_combined['ECL'].round(3)
#     df_combined['UL'] = df_combined['UL'].round(3)
#     df_combined['taux_provisionnement'] = df_combined['taux_provisionnement'].round(4)
#     df_combined['RWA'] = df_combined['RWA'].round(3)
#     df_combined['fonds_propres'] = df_combined['fonds_propres'].round(4)

#     # Convertir pour envoi au template
#     combined_list = df_combined.to_dict(orient='records')

#     # Création d’un résumé agrégé
#     ead_total = df_combined['ead'].sum().round(2)
#     ecl_total = df_combined['ECL'].sum().round(2)

#     # Calcul du taux de provision global
#     taux_prov_global = round((ecl_total / ead_total) * 100, 4) if ead*


        # Afficher l'erreur à l'utilisateur
        return render(request, 'vision360.html', {'message': f"Une erreur est survenue : {str(e)}"})

from django.shortcuts import render
import pandas as pd
import numpy as np
from scipy.stats import norm

def fiche_client_view(request):
    # try:
#     # Handle both GET and POST requests
#     client_id = request.POST.get('id') or request.GET.get('id')
#     if not client_id:
#         return render(request, 'fiche_client.html', {'message': "Veuillez fournir un ID de client."})

#     # Récupérer les données depuis la session
#     id_ead_list = request.session.get('id_ead_list', [])
#     id_pd2024_list = request.session.get('id_pd2024_list', [])
#     id_lgd_list = request.session.get('id_lgd_list', [])

#     # Vérifier si les listes sont vides
#     if not id_ead_list or not id_pd2024_list or not id_lgd_list:
#         return render(request, 'fiche_client.html', {'message': "Aucune donnée disponible dans la session."})

#     # Créer les DataFrames
#     df_ead = pd.DataFrame(id_ead_list, columns=['id', 'ead'])
#     df_pd = pd.DataFrame(id_pd2024_list, columns=['id', 'pd'])
#     df_lgd = pd.DataFrame(id_lgd_list, columns=['id', 'lgd'])

#     # Fusion et traitement
#     df = df_ead.merge(df_pd, on='id').merge(df_lgd, on='id')
#     df = df.replace({'pd': {'N/A': np.nan}, 'lgd': {'N/A': np.nan}, 'ead': {'N/A': np.nan}})
#     df[['pd', 'lgd', 'ead']] = df[['pd', 'lgd', 'ead']].astype(float)

#     # Remplissage des NaN
#     df.fillna(df.mean(numeric_only=True), inplace=True)

#     # Calculs
#     df['PD'] = df['pd'] / 100
#     df['ECL'] = df['PD'] * df['lgd'] * df['ead']
#     df['taux_provisionnement'] = df['ECL'] / df['ead'] * 100

#     z_999 = norm.ppf(0.999)
#     rho = 0.15

#     def calculate_K(PD, LGD):
#         if PD >= 1.0 or PD <= 0.0:
#             return np.nan
#         z_PD = norm.ppf(PD)
#         return LGD * norm.cdf((z_PD + np.sqrt(rho) * z_999) / np.sqrt(1 - rho))

#     df['K'] = df.apply(lambda row: calculate_K(row['PD'], row['lgd']), axis=1).fillna(0)
#     df['RWA'] = df['K'] * df['ead'] * 12.5
#     df['UL'] = df.apply(lambda row: row['ead'] * row['lgd'] *
#                         (norm.cdf((norm.ppf(row['PD']) + np.sqrt(rho) * z_999) / np.sqrt(1 - rho)) - row['PD']), axis=1)
#     df['fonds_propres'] = df['RWA'] * 0.08

#     # Fonction get_risk_level_and_comment (exemple si non définie)
#     def get_risk_level_and_comment(pd_val):
#         if pd_val > 0.1:
#             return 5, "Risque élevé"
#         elif pd_val > 0.05:
#             return 4, "Risque modéré"
#         elif pd_val > 0.02:
#             return 3, "Risque moyen"
#         elif pd_val > 0.01:
#             return 2, "Risque faible"
#         else:
#             return 1, "Risque très faible"

#     df["level"], df["comment"] = zip(*df["pd"].apply(lambda pd_val: get_risk_level_and_comment(pd_val / 100)))
#     risk_labels = {5: "À surveiller", 4: "Moyen", 3: "Bon", 2: "Très Bon", 1: "Excellent"}
#     df['classe'] = df['level'].map(risk_labels)

#     # Récupérer les données du client demandé
#     client_data = df[df['id'] == int(client_id)].copy()
#     client_data = client_data.round(3)
#     client_data['id'] = client_data['id'].astype(int)
#     if client_data.empty:
#         return render(request, 'fiche_client.html', {'message': "Aucun client trouvé avec cet ID."})

#     return render(request, 'fiche_client.html', {'client': client_data.iloc[0].to_dict()})

# except Exception as e:

        return render(request, 'fiche_client.html', {'message': f"Erreur : {str(e)}"})