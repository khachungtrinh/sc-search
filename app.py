import streamlit as st
from deep_translator import GoogleTranslator
import requests


st.set_page_config(
    page_title='sutta',
    page_icon='🎨' ,
    layout="wide")


def smarkdown(oj):
    st.markdown(oj, unsafe_allow_html=True)


def smarkdown_none(oj):
    if oj is None:
        pass
    elif len(oj) == 0:
        pass
    else:
        smarkdown(oj)


def md_define(lw: list):
    md = ''
    for name in lw:
        md = md + '[{}](https://suttacentral.net/define/{}?lang=en)'.format(name, name) + ', '
    return smarkdown(md)


def find_id_line(line_sutta: str):
    a = line_sutta.find('id="')
    b = line_sutta[a + 4:].find('"')
    return line_sutta[a + 4:a + 4 + b]


def find_line_num(p: str, s: str):
    i = s.find(p)
    dem = 0
    while i != -1:
        i = s.find(p, i+1)
        dem = dem + 1
    return dem


def find_in_sutta_num(p: str, data: str):
    dem = 0
    for line in data:
        dem = dem + find_line_num(p, line)
    return dem


def find_in_nikaya(data: list):
    dem_dn = 0
    dem_mn = 0
    dem_sn = 0
    dem_an = 0
    dem_snp = 0
    dem_kp = 0
    dem_iti = 0
    dem_ud = 0
    dem_dhp = 0
    dem_thig = 0
    dem_thag = 0

    for name in data:
        try:
            check_ = name['acronym'][:3]
        except:
            check_ = ''
            pass
        match check_:
            case 'DN ':
                dem_dn = dem_dn + 1
            case 'MN ':
                dem_mn = dem_mn + 1
            case 'SN ':
                dem_sn = dem_sn + 1
            case 'AN ':
                dem_an = dem_an + 1
            case 'Snp':
                dem_snp = dem_snp + 1
            case 'kp ':
                dem_kp = dem_kp + 1
            case 'Iti':
                dem_iti = dem_iti + 1
            case 'Ud ':
                dem_ud = dem_ud + 1
            case 'Dhp':
                dem_dhp = dem_dhp + 1
            case 'Thi':
                dem_thig = dem_thig + 1
            case 'Tha':
                dem_thag = dem_thag + 1
    return {'dn': dem_dn, 'mn': dem_mn, 'sn': dem_sn, 'an': dem_an, 'snp': dem_snp, 'kp': dem_kp, 'iti': dem_iti, 'ud': dem_ud, 'dhp': dem_dhp, 'thig': dem_thig, 'thag': dem_thag}



def creat_link(name, url):
    return '[{}]({})'.format(name, url)


def md_thamkhao(sutta_id: str, sutta_name: str):
    sutta_name = sutta_id.upper() + ' -- ' + sutta_name
    sutta_id = sutta_id.lower()
    sutta_book = sutta_id.rstrip('0123456789 -.')
    url_all = 'https://suttacentral.net/{}?view=normal&lang=en'.format(sutta_id)
    url_en = 'https://suttacentral.net/{}/en/sujato?lang=en&layout=sidebyside&reference=none&notes=asterisk&highlight=false&script=latin'.format(
        sutta_id)
    url_vi = 'https://suttacentral.net/{}/vi/minh_chau?lang=en&reference=none&highlight=false'.format(sutta_id)
    url_the = 'https://thebuddhaswords.net/{}/{}.html#content'.format(sutta_book, sutta_id)
    smarkdown('###### ' + sutta_name + '  (' +
              creat_link('all', url_all) + '; ' +
              creat_link('en', url_en) + '; ' +
              creat_link('vi', url_vi) + '; ' +
              creat_link('the', url_the) + '; ' +
              ')')


def show_muti_lang(lang1, lang2, lang3):
    c_l1, c_l2, c_l3 = st.columns([1, 1, 1])
    with c_l1:
        smarkdown(lang1)
    with c_l2:
        smarkdown(lang2)
    with c_l3:
        smarkdown(lang3)


def get_url(url):
    res = requests.get(url)
    return res.json()


@st.cache_data()
def get_sutta_sujato(sutta):
    url = 'https://suttacentral.net/api/bilarasuttas/{}/sujato?lang=en'.format(sutta)
    data = get_url(url)
    return data['root_text'], data['translation_text']


@st.cache_data()
def get_pali_en(pali_word: str):
    url = 'https://suttacentral.net/api/dictionary_full/{}?language=en'.format(pali_word)
    data = get_url(url)
    return data


@st.cache_data()
def get_adjacent(pali_word):
    url = 'https://suttacentral.net/api/dictionary_full/adjacent/{}'.format(pali_word)
    data = get_url(url)
    return data


@st.cache_data()
def get_similar(pali_word):
    url = 'https://suttacentral.net/api/dictionary_full/similar/{}'.format(pali_word)
    data = get_url(url)
    return data


@st.cache_data()
def get_search(p, litmit=100, match_p='false'):
    url = 'https://suttacentral.net/api/search/instant?limit={}&query={}&language=en&restrict=all&matchpartial={}'.format(litmit, p, match_p)
    data = get_url(url)
    data_s = data['hits']
    data_t = data['suttaplex']
    tongkq = data['total']
    return data_s, data_t, tongkq


@st.cache_data()
def show_search(data, p, trans='true'):
    for i, name in enumerate(data):
        st.write('-----------------------------------')
        try:
            check_acr = name['acronym']
            if check_acr is None:
                try:
                    smarkdown(name['heading']['title'])
                    for kq in name['highlight']['content']:
                        smarkdown(kq)
                except:
                    for kq in name['highlight']['content']:
                        smarkdown(kq)
            else:
                sutta_id = name['uid']
                md_thamkhao(sutta_id, name['name'])
    
                dem = 0
                for kq in name['highlight']['content']:
                    id_line = find_id_line(kq)
                    id_line_sutta = sutta_id + ':' + id_line
                    if '-' in id_line_sutta:
                        pass
                    else:
                        if name['lang'] == 'pli':
                            try:
                                data_sutta_pali, data_sutta_en = get_sutta_sujato(sutta_id)
                                # kq_pli = data_sutta_pali[id_line_sutta]
                                kq_en = data_sutta_en[id_line_sutta]
                                dem = find_in_sutta_num(p, data_sutta_pali.values())
                                # st.text(kq_en)
                                # st.text(kq_vi)
                                if trans == 'true':
                                    kq_vi = GoogleTranslator(source='auto', target='vi').translate(kq_en)
                                    show_muti_lang(kq, kq_en, kq_vi)
                                else:
                                    show_muti_lang(kq, kq_en, '')
                            except:
                                smarkdown(kq)
                        else:
                            try:
                                if trans:
                                    kq_vi = GoogleTranslator(source='auto', target='vi').translate(kq)
                                    show_muti_lang(kq, kq_vi, '')
                                else:
                                    show_muti_lang(kq, '', '')
                            except:
                                smarkdown(kq)
    
                if dem > 1:
                    st.text('{} lần'.format(dem))
        except:
            dict_a = data[0]['highlight']['detail'][0]
            dict_text = dict_a['text']
            dict_text_new = dict_text.replace("href='/", "href='https://suttacentral.net/")
            dict_name = dict_a['dictname']
            smarkdown_none('(<b>{}</b>)'.format(dict_name))
            smarkdown_none(dict_a['grammar'])
            smarkdown_none(dict_a['definition'])
            smarkdown_none(dict_text_new)

            dict_full = get_pali_en(dict_a['word'])

            for name_ in dict_full:
                st.write('-----------------------------------')
                if name_['dictname'] == dict_name:
                    pass
                else:
                    smarkdown_none('(<b>{}</b>)'.format(name_['dictname']))
                    smarkdown_none(name_['grammar'])
                    dict_def = name_['definition']
                    if isinstance(dict_def, list):
                        for name__ in dict_def:
                            smarkdown_none(name__)
                    else:
                        smarkdown_none(dict_def)
                    smarkdown_none(name_['text'])

            p_adjacent = get_adjacent(p)
            smarkdown_none('(<b>adjacent terms</b>)')
            md_define(p_adjacent[0])
            st.write('-----------------------------------')
            p_similar = get_similar(p)
            smarkdown_none('(<b>similar spelling</b>)')
            md_define(p_similar[0])


try:
    query_p = st.query_params.p
except:
    query_p = ''
    
c_s1, c_s2, c_s3, c_s4, c_s5 = st.columns([2, 1, 1, 1, 5])
with c_s1:
    p = st.text_input('search pali', query_p)
with c_s2:
    limit_kq = st.selectbox('limit', [20, 50, 100, 200, 500, 1000], index=1)
with c_s3:
    match_p = st.selectbox('matchpartial', ['false', 'true'])
with c_s4:
    to_vi = st.selectbox('vitrans', ['false', 'true'])

if len(p) > 0:
    data_search, data_title, tongkq = get_search(p=p, litmit=limit_kq, match_p=match_p)
    d = find_in_nikaya(data_search)
    with c_s5:
        st.text('thống kê {} / tổng {} kết quả'.format(limit_kq, tongkq))
        st.text(d)
    if len(data_title) > 0:
        c_s5, c_s6 = st.columns([1, 3])
        for name in data_title:
            with c_s5:
                md_thamkhao(name['uid'], name['original_title'])
            with c_s6:
                st.write(name['blurb'])
    show_search(data_search, p, trans=to_vi)

