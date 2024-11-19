Pour recuperer les fichiers audios.
pipeline_API_xeno_extract : recupère toutes les données de xeno_canto en france resultat:  oiseaux_data_full.csv (inutile à refaire)
pipeline_API_xeno_transform: effectue un premier tri par qualité micro, interval de temps et region (choisir ile de france, bretagne, etc...); resultats oiseaux_data_transformed.csv (inutile de le refaire), oiseaux_data_ile_de_france.csv
pipeline_API_xeno_add: ajout d'un colonne dans le csv: resultats oiseaux_data_ile_de_france_type.csv
pipeline_API_xeno_final: ne recupère que les lignes de type MP3 resultat: oiseaux_data_ile_de_france_final.csv