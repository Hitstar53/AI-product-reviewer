from joblib import load
from sklearn.linear_model import LinearRegression

lr_model=load('rating_predictor_updated.joblib')
def rating(score_list):
    star=lr_model.predict(score_list)
    print(star)
    return star
