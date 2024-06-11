from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import datetime
import jieba
import pymysql
import wordcloud
import imageio


def get_stopword_list():
    stop_word_path = 'stopwords.txt'
    stopword_list = [sw.replace('\n', '') for sw in open(stop_word_path).readlines()]
    return stopword_list


def seg_to_list(sentence):
    jieba.add_word('五险一金')
    seg_list = jieba.cut(sentence)
    return seg_list


def word_filter(seg_list):
    stopword_list = get_stopword_list()
    filter_list = ""
    for seg in seg_list:
        if not seg in stopword_list and len(seg) > 1 and not seg.isnumeric():
            filter_list += seg + " "
    return filter_list


def load_data():
    conn = pymysql.connect(host="nj-cynosdbmysql-grp-b3f65mfl.sql.tencentcdb.com", port=25704, user="root",
                           passwd="huhu-1234", db="employment")
    cursor = conn.cursor()
    #  order by rand() limit 10000
    sql = "select description from info where season = %s"
    args = datetime.datetime.today().strftime('%Y-%m')
    cursor.execute(sql, args)
    conn.commit()
    data = cursor.fetchall()
    doc_list = []
    for description in data:
        if '福利' not in description[0]:
            continue
        if '能力' not in description[0]:
            continue
        doc_list.append(word_filter(seg_to_list(description[0])))
    return doc_list


def main():
    # 构造 TF-IDF
    tf_idf_vectorizer = TfidfVectorizer()
    tf_idf = tf_idf_vectorizer.fit_transform(load_data())
    # 特征词 TF-IDF 矩阵
    matrix = tf_idf.toarray()
    # 指定 lda 主题数
    n_topics = 3
    n_top_words = 30
    lda = LatentDirichletAllocation(
        n_components=n_topics, max_iter=50,
        learning_method='online',
        learning_offset=50.,
        random_state=0)
    # 使用tf_idf语料训练lda模型
    lda.fit(tf_idf)

    rows = []
    frequencies = []
    feature_names = tf_idf_vectorizer.get_feature_names_out()
    for topic in lda.components_:
        top_words = []
        frequency = []
        for i in topic.argsort()[:-n_top_words - 1:-1]:
            if feature_names[i] not in ['能力', '客户', '福利', '经验', '职位', '公司', '任职', '岗位职责']:
                top_words.append(feature_names[i])
                frequency.append(i)
        rows.append(top_words)
        frequencies.append(frequency)
    if min(len(rows[0]), len(rows[1]), len(rows[2])) == len(rows[0]):
        res = dict(zip(rows[0], frequencies[0]))
    elif min(len(rows[0]), len(rows[1]), len(rows[2])) == len(rows[1]):
        res = dict(zip(rows[1], frequencies[1]))
    else:
        res = dict(zip(rows[2], frequencies[2]))
    w = wordcloud.WordCloud(
        width=1000, height=700,
        background_color="white",
        font_path="msyh.ttc",
    )
    w.generate_from_frequencies(res)
    w.to_file("cloud.png")


if __name__ == '__main__':
    main()
