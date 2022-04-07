from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pandas as pd

def create_dataset():
    audi = pd.read_csv("main/data/audi.csv")
    bmw = pd.read_csv("main/data/bmw.csv")
    mercedes= pd.read_csv("main/data/merc.csv")
    skoda= pd.read_csv("main/data/skoda.csv")
    ford= pd.read_csv("main/data/ford.csv")
    volkswagen= pd.read_csv("main/data/vw.csv")

    #MERGING 

    audi["company"]="Audi"
    bmw["company"]="BMW"
    ford["company"]="Ford"
    mercedes["company"]="Mercedes"
    skoda["company"]="Skoda"
    volkswagen["company"]="Volkswagen"

    df = pd.concat([audi,bmw,ford,mercedes,skoda,volkswagen])
    df= df.reset_index()
    df['id']= df.index
    return df
def find_car(df,price,company,fuel_type ):
    df_new = df[(df['fuelType']==fuel_type) & (df['company'] == company)]
    # df_new = df_new.drop_duplicates(['model'])
    # df_final = df_new.iloc[(df_new['price']-price).abs().argsort()[:4]]


    df_final = df_new.iloc[(df_new['price']-price).abs().argsort()[:50]]
    df_final = df_final.drop_duplicates(['model'])
    df_final = df_final.iloc[:4]
    # df_new.reset_index(inplace=True)
    # df_new['id']=df_new.index
    
    # list_models = []
    # car_index = df_new.iloc[(df_new['price']-price).abs().argsort()[:1]].index
    

    # df_pivot = df_new.pivot(index = 'id', columns = 'model', values = 'price').fillna(0)
    # df_matrix = csr_matrix(df_pivot.values)
    
    # model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
    # model_knn.fit(df_matrix)
    
    # query_index = car_index
    # distances, indices = model_knn.kneighbors(df_pivot.iloc[query_index, :].values.reshape(1, -1), n_neighbors = 5)

    # for i in range(0, len(distances.flatten())):
    #     if i == 0:
    #         print('Recommendations for {0}:\n'.format(df_pivot.index[query_index]))
    #     else:
    #         print('{0}: {1}, with distance of {2}:'.format(i, df_pivot.index[indices.flatten()[i]], distances.flatten()[i]))
    #         list_models.append([df_pivot.index[indices.flatten()[i]], distances.flatten()[i]][0])
    # data = list_models
    return df_final