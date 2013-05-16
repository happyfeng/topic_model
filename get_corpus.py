#coding:utf-8
##��ȡciteulike���Ͽ�
from gensim import corpora,models
import re
import os

def get_cp(files):

    content = open(files,'rb')
    #���жϸ��ļ��Ƿ����
    if os.path.exists(r'D:\citeulike\temp.dat'):
        content2 = open('temp.dat','w')
    else:
        content2 = open('temp.dat','a')
    txt = content.readlines()
    stopword = open('stopword_en.dat','rb')
    sw = stopword.readlines()
    stoplist = []
    for w in sw:
        stoplist.append(w.rstrip())
    for txt2 in txt:
        #ֻ����Ӣ�ģ�ȥ�����ź����� 
        newcontent = re.sub('[^a-zA-Z]',' ',txt2)
        content2.write(newcontent+'\n')
    content2.close()
    newtxt = open('temp.dat','rb')
    text = [[word for word in texts.split() if word not in stoplist]for texts
            in newtxt.readlines() ]
    stopword.close()
    dictionary = corpora.Dictionary(text)
    dictionary.save(r'D:\citeulike\dic\citeulike.dict')
    print 'finish saveing dict'
    corpus = [dictionary.doc2bow(texts) for texts in text]
    corpora.MmCorpus.serialize(r'D:\citeulike\dic\citeulike.mm', corpus)
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    corpora.MmCorpus.serialize(r'D:\citeulike\dic\citeulike_tfidf.mm', corpus_tfidf)
    
	#��batchldaѵ������ 
    batch_lda = models.ldamodel.LdaModel(corpus=corpus_tfidf,
        id2word=dictionary,num_topics=30, update_every=0, passes=10)
    batch_lda.save('batch_lda.lda')
	
get_cp('raw-data.csv')
