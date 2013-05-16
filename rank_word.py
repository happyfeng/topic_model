#coding:utf-8
#计算每篇文章top-n主题下的所有单词概率总和
import gensim
txt = open(r'D:\citeulike\temp.dat','r').readlines()
def get_txt(texts):
    #去停用词 
    stopword = open(r'D:\citeulike\stopword_en.dat','r')
    sw = stopword.readlines()
    stoplist = []
    for w in sw:
        stoplist.append(w.rstrip())
    text = []
    for word in texts.split(' '):
        if word not in stoplist and len(word)>1:
            text.append(word)
    return text 

def print_topic():
    #输出概率最大的n个主题
    file_rate = open(r'D:\citeulike\dic\rank_word.dat','a')
    diction = gensim.corpora.Dictionary.load('citeulike.dict')
    batch_lda = gensim.models.LdaModel.load(r'D:\citeulike\dic\batch_lda.lda')
    for i in range(len(txt)):
        topic_rate_new = 0
        content_list =get_txt(txt[i])
        doc_bow = diction.doc2bow(content_list)
        doc_lda = batch_lda[doc_bow]
        #print doc_lda
        # 输出概率最大的前三个主题
        tP_batch = []
        for yuanzu in doc_lda:
            tP_batch.append(list(yuanzu))
        for i in range(len(tP_batch)):
            tmp = tP_batch[i][0]
            tP_batch[i][0] = tP_batch[i][1]
            tP_batch[i][1] = tmp
        tP_batch.sort()
        tP_batch_new = tP_batch[-3:]
        
        #计算每篇文章top-n主题下的单词概率总和
        for m in range(len(tP_batch_new)):
            dic = {}
            word_rate = 0
            tp_id = tP_batch_new[m][1]
            #ladmodel.py源代码568行自己改了id2word[id],topic[id]输出顺序
            word_list = batch_lda.show_topic(tp_id,500000)
            dic = dict(word_list)  #将showtopic的[(a,b),(),()]形式转换成字典
            for w in list(set(content_list)):
                #print dic[w]
                word_rate += dic[w] #计算总的主题下单词概率
            #乘以该主题的概率并除以文章内单词总个数，防止有些文章词很多，值也就很大
            topic_rate = tP_batch_new[m][0] * word_rate/ len(set(content_list)) 
            topic_rate_new += topic_rate
        print topic_rate_new
        #写入文件
        file_rate.write(str(topic_rate_new)+'\n')
    file_rate.close()
if __name__ == '__main__':
	print_topic()


