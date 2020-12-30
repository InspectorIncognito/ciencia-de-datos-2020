import pickle

POLI_REG = '../test401/polynomial401.sav'
MODEL_PATH = '../test401/PRegressor401.sav'

def predict(data):
    poli = pickle.load(open(POLI_REG, 'rb'))
    reg = pickle.load(open(MODEL_PATH, 'rb'))
    #print(data.values)
    data = poli.transform(data.values)
    #print(data.shape)
    y_pred = reg.predict(data)
    return y_pred