from flask import Flask
from flask import render_template, url_for, request, redirect
import pandas as pd
from pymorphy2 import MorphAnalyzer

morph = MorphAnalyzer()

list_of_tags = ['NOUN', 'ADJ', 'COMP', 'VERB', 'PRT', 'GRND', 'NUMR', 'ADVB', 'NPRO', 'PRED', 'PREP', 'CONJ', 'PRCL', 'INTJ', 'None']
df = pd.read_csv('data_table.csv', header=0)
data = []
for v in df.values:
    sent = [v[0], v[1], v[2], v[3], v[4]]
    data += [sent]

def get_lat(line):
    line = line.split("""'], ['""")
    line = [w.strip("""[['""").strip("""']]""").split("""', '""") for w in line]
    return line

for d in data:
    d[1] = get_lat(d[1])

def get_result(searchline):
    resultlist = []
    s = searchline.split(' ')
    
    if len(s) == 1:
        for sent in data:
            for word in sent[1]:
                check1 = s[0].startswith('"') and s[0].strip('"') == word[0]
                check2 = s[0] in list_of_tags and s[0] == word[2]
                check3 = '+' in s[0] and s[0].split('+')[0] == word[0] and s[0].split('+')[1] == word[2]
                check4 = morph.parse(s[0])[0].normal_form == word[1]
                if check1 or check2 or check3 or check4:
                    if sent not in resultlist:
                        resultlist += [sent]
    if len(s) == 2:
        for sent in data:
            for w in range(len(sent[1])-1):
                word1 = sent[1][w]
                word2 = sent[1][w+1]
                check1 = s[0].startswith('"') and s[0].strip('"') == word1[0]
                check2 = s[0] in list_of_tags and s[0] == word1[2]
                check3 = '+' in s[0] and s[0].split('+')[0] == word1[0] and s[0].split('+')[1] == word1[2]
                check4 = morph.parse(s[0])[0].normal_form == word1[1]
                if check1 or check2 or check3 or check4:
                    check11 = s[1].startswith('"') and s[1].strip('"') == word2[0]
                    check22 = s[1] in list_of_tags and s[1] == word2[2]
                    check33 = '+' in s[1] and s[1].split('+')[0] == word2[0] and s[1].split('+')[1] == word2[2]
                    check44 = morph.parse(s[1])[0].normal_form == word2[1]
                    if check11 or check22 or check33 or check44:
                        if sent not in resultlist:
                            resultlist += [sent]
    if len(s) == 3:
        for sent in data:
            for w in range(len(sent[1])-2):
                word1 = sent[1][w]
                word2 = sent[1][w+1]
                word3 = sent[1][w+2]
                check1 = s[0].startswith('"') and s[0].strip('"') == word1[0]
                check2 = s[0] in list_of_tags and s[0] == word1[2]
                check3 = '+' in s[0] and s[0].split('+')[0] == word1[0] and s[0].split('+')[1] == word1[2]
                check4 = morph.parse(s[0])[0].normal_form == word1[1]
                if check1 or check2 or check3 or check4:
                    check11 = s[1].startswith('"') and s[1].strip('"') == word2[0]
                    check22 = s[1] in list_of_tags and s[1] == word2[2]
                    check33 = '+' in s[1] and s[1].split('+')[0] == word2[0] and s[1].split('+')[1] == word2[2]
                    check44 = morph.parse(s[1])[0].normal_form == word2[1]
                    if check11 or check22 or check33 or check44:
                        check111 = s[2].startswith('"') and s[2].strip('"') == word3[0]
                        check222 = s[2] in list_of_tags and s[2] == word3[2]
                        check333 = '+' in s[2] and s[2].split('+')[0] == word3[0] and s[2].split('+')[1] == word3[2]
                        check444 = morph.parse(s[2])[0].normal_form == word3[1]
                        if check111 or check222 or check333 or check444:
                            if sent not in resultlist:
                                resultlist += [sent]
    return resultlist

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/results')
def results():
    searchlink = request.args.get('searchlink')
    resultlist = get_result(searchlink)
    return render_template('results.html', resultlist=resultlist)

if __name__ == "__main__":
    app.run()
    
