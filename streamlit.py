import streamlit as st
from PIL import Image
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import pandas as pd
import gensim
from gensim import corpora

def topic_modeling():
    data = pd.read_csv('D:/Artus/École/A5/Machine Learning for NLP/Projet 2/trustpilot_en_50_page.csv')
    doc_complete =data['Review']

    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    def clean(doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        return normalized

    doc_clean = [clean(doc).split() for doc in doc_complete] 

    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    Lda = gensim.models.ldamodel.LdaModel
    ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=50)
    return ldamodel

# Personnalisation de la barre latérale
st.markdown(
    """
    <style>
        .sidebar {
            background-color: #000;
            padding: 10px;
            color: #fff;
        }
        .sidebar .sidebar-content {
            max-width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True
)

image = Image.open('/visualisation_word2vec.jpg')

# Création de la barre latérale
sidebar = st.sidebar

# Ajout des options à la barre latérale
selected_tab = sidebar.radio('Navigation', ['Accueil', 'Word2Vec', 'Topic modeling'])

# Affichage du contenu en fonction de l'onglet sélectionné
if selected_tab == 'Accueil':
    st.title('Bienvenue sur le Streamlit du projet 2 de Machine Learning for NLP')
    st.write('Thomas Bouguet - Artus Chapelain')
    st.write('')
    st.write('Nous avons choisi de scraper les données de Trustpilot sur les restaurants, bar et entreprises de livraison de nourriture')

elif selected_tab == 'Word2Vec':
    st.title('Word2Vec')
    st.write('Après avoir train nos données avec Word2Vec, nous pouvons les visualiser avec MatPlotLib')
    st.image(image)
    st.write('Nous pouvons voir que les mots fréquemment utilisés dans les mêmes reviews apparaissent dans les mêmes groupes')

elif selected_tab == 'Topic modeling':
    st.title('Topic modeling')
    st.write('Here is our Topic modeling computed with Lda Model')
    topic_modeling_computed = [(0, '0.012*"starbucks" + 0.010*"coffee" + 0.010*"customer"'), (1, '0.044*"order" + 0.028*"grubhub" + 0.018*"food"'), (2, '0.031*"meal" + 0.021*"food" + 0.020*"great"')]
    st.write(topic_modeling_computed)
    recompute = st.button("Recompute Topic modeling")
    if(recompute):
        topic_modeling_computed = topic_modeling().print_topics(num_topics=3, num_words=3)
        st.write(topic_modeling_computed)
        recompute = False
    