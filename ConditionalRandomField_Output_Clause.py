import sklearn_crfsuite
import spacy
import nltk

"""
Get the data 
"""
train_file = r"C:\Users\drewb\PycharmProjects\FirstProject\query_data.txt"
train_target_file = r"C:\Users\drewb\PycharmProjects\FirstProject\query_target.txt"
with open(train_file) as f:
    train_content = f.readlines()
with open(train_target_file) as f2:
    train_content_target = f2.readlines()

"""
spacy for dependency parser and POS tagging 
"""
nlp = spacy.load('en_core_web_sm')
train_x = list()
test_x = list()
"""
Lemmatizer for normalization
"""
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

"""
Gives the normalized representation of a sentence 
"""
def return_representation(sentence):
    sen = sentence.replace("\n", '')
    data = sen.replace('.', '')
    data = data.replace('?', '')
    data = data.replace(',', '')
    data = data.replace('\'', '')
    doc = nlp(data)
    new_sentence = list()
    for token in doc:
        if token.dep_.lower() == "punct" or token.text == '':
            continue
        word_dict = dict()
        word_dict["word"] = lemmatizer.lemmatize(token.text.lower())
        word_dict["dep"] = token.dep_
        word_dict["head"] = lemmatizer.lemmatize(token.head.text)
        word_dict["head_pos"] = token.head.pos_
        word_dict["head_dep"] = token.head.dep_
        word_dict["head_head"] = token.head.head.pos_
        word_dict["head_head_head"] = token.head.head.dep_
        word_dict["pos"] = token.pos_

        word_dict['tree'] = [lemmatizer.lemmatize(child.text) for child in token.children]
        new_sentence.append(word_dict)
    return new_sentence

"""
Split training and testing for target values 
"""
train_y = list()
test_y = list()
itr = 0
for sentence in train_content_target:
    list_to_add = list()
    for c in sentence:
        if c != '\n':
            list_to_add.append(c)
    if itr < 700:
        train_y.append(list_to_add)
    else:
        test_y.append(list_to_add)
    itr += 1




itr = 0
for sentence in train_content:
    new_sentence = return_representation(sentence)
    if itr < 700:
        train_x.append(new_sentence)
    else:
        test_x.append(new_sentence)
    itr += 1



"""
So this next part needs some explaining (Lines 96 - 108)

Basically right now the spacy dependency parser is splitting words 
like "id" into two different words and that is causing a the lengths
of the target and the data to differ by an offset of one. This only
happened a few times so the naive approach was to just exclude those
from training and testing.  
"""
new_train_x = list()
new_train_y = list()
for i in range(len(train_x)):
    if len(train_y[i]) == len(train_x[i]):
        new_train_x.append(train_x[i])
        new_train_y.append(train_y[i])
new_test_x = list()
new_test_y = list()
for i in range(len(test_x)):
    if len(test_x[i]) == len(test_y[i]):
        new_test_x.append(test_x[i])
        new_test_y.append(test_y[i])


"""
Create Model 
"""
crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)

"""
Train
"""
crf.fit(new_train_x, new_train_y)


print("SCORE:")
print(crf.score(new_test_x, new_test_y))
