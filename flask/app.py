import flask
from flask import render_template
from ta import tweetprepared
import pickle
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


app = flask.Flask(__name__, template_folder='templates')
model_mnb = pickle.load(open('/app/model_mnb_r2_1.pkl','rb'))
vocabulary = pickle.load(open('/app/vocabulary_r2_1.pkl','rb'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])


def main():
    if flask.request.method == 'GET':
        return render_template('main.html' )

    if flask.request.method == 'POST':
        #answer = ''
        exp_s = flask.request.form['tweet']
        exp = tweetprepared.tw_full_preprocess(exp_s)
        count_vect = CountVectorizer(analyzer='word', encoding='cp1251', vocabulary=vocabulary)
        count_vect._validate_vocabulary()
        exp_vect_2 = count_vect.transform([exp])
        tfidf_transformer = TfidfTransformer(use_idf=False)
        exp_vect_2_tfidf = tfidf_transformer.transform(exp_vect_2)
        predict = model_mnb.predict(exp_vect_2_tfidf)
        if predict[0] == 0:
            answer = 'Негативное'
        else:
            answer = 'Позитивное'
        #temp = predict[0]
        return render_template('main.html', tweet=exp_s, result=answer)

if __name__ == '__main__':
    app.run()
