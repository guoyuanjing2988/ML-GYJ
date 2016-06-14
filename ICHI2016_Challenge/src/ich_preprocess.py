from nltk.corpus import stopwords
def preprocess(s,need_vocab=False,min_df=20):
    s1 = ''
    for i in range(len(s)):
        x=s[i]
        if ((s[i] >= 'a') and (s[i] <= 'z')) or ((s[i] >= 'A') and (s[i] <= 'Z')) or ((s[i]>='0') and (s[i]<='9')):
            s1 = s1 + s[i]
        else:
            s1 = s1 + ' '
    while (len(s1) > 0) and (s1[len(s1) - 1] == ' '):
        s1 = s1[:len(s1) - 1]
    stop=stopwords.words('english')
    s1=s1.split(' ')
    for i in range(len(s1)):
        if (s1[i].lower() in stop):
            s1[i]=' '
    s2=''
    for i in range(len(s1)):
        s2=s2+s1[i]+' '
    string = s2.lower()
    if need_vocab==True:
        a = string.split()
        vocab = []
        count = []
        for i in range(len(a)):
            f = True
            for j in range(len(vocab)):
                if vocab[j] == a[i]:
                    f = False
                    count[j] += 1
                    break
            if f == True:
                vocab.append(a[i])
                count.append(1)
        i = 0
        while i < len(vocab):
            if count[i] < min_df:
                del (vocab[i])
                del (count[i])
            else:
                i += 1
        return vocab
    else:
        return string

