from A_pipeline_API_xeno_extract import oiseaux_data
from B_pipeline_API_xeno_transform import transform_data
from C_pipeline_API_xeno_add_type import add_type
from D_pipeline_API_xeno_final import data_final
from E_pipeline_API_download_file import download_file

liste_region=["ile-de-france","bretagne"]

def pipeline_API_without_WAV():


    for region in liste_region:
        transform_data(region)
        print("transform data effectuée")
        #definir dans add_type des conditions pour ne pas repeter le processus qui est long
        #en utilisant les return comparant le dataframe existant avec le nouveau
        add_type(region)
        print("add data effectuée")
        data_final(region)
        print("tri data effectuée")

    return()


def pipeline_API():


    for region in liste_region:
        transform_data(region)

    return()

#pipeline_API_without_WAV()

def download():


    for region in liste_region:
        download_file(region)

    return()
        
download()

