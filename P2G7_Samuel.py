import pandas as pd
import psycopg2 as db
from elasticsearch import Elasticsearch
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

def get_data():
    """
    Fungsi ini mengambil data dari database PostgreSQL dan mengembalikannya dalam bentuk DataFrame.

    Returns:
    pandas.DataFrame: Data dari tabel 'table_g7' dalam database PostgreSQL.
    """
    conn_string="dbname='ftds' host='localhost' user='postgres' password='scs1638' port=5432"
    conn=db.connect(conn_string)
    df=pd.read_sql("select * from table_g7", conn)
    return df

def normalcolumn(cf):
    """
    Fungsi ini membersihkan dan mengubah kolom DataFrame.

    Args:
    cf (pandas.DataFrame): DataFrame yang akan diubah.

    Returns:
    pandas.DataFrame: DataFrame yang sudah dibersihkan dan diubah nama kolomnya.
    """
    df = cf.copy()
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(' ','_')
    df.columns = df.columns.str.replace('?','')
    df = df.dropna()
    df['age'] = df['age'].astype(int)
    df.rename(columns={'choose_your_gender': 'gender', 'what_is_your_course': 'subject', 'your_current_year_of_study': 'current_year_study', 
                   'what_is_your_cgpa': 'cgpa', 'do_you_have_depression': 'have_depression', 'do_you_have_panic_attack': 'panic_attack',
                   'do_you_have_anxiety': 'have_anxiety', 'did_you_seek_any_specialist_for_a_treatment': 'specialist_treatment'}, inplace=True)
    df['cgpa'] = df['cgpa'].str.strip()
    df['current_year_study'] = df['current_year_study'].str.lower()
    df['subject'] = df['subject'].str.strip()
    df['subject'] = df['subject'].str.lower()
    df['subject'] = df['subject'].str.replace('islamic education', 'pendidikan Islam')
    return df

def save_data(df_clean):
    """
    Fungsi ini menyimpan DataFrame ke dalam file CSV.

    Args:
    df_clean (pandas.DataFrame): DataFrame yang akan disimpan.

    Returns:
    None
    """
    df_clean.to_csv(('P2G7_Samuel_data_clean.csv'), index=False)

def import_data(df_clean):
    """
    Fungsi ini mengimpor data dari DataFrame ke Elasticsearch.

    Args:
    df_clean (pandas.DataFrame): DataFrame yang akan diimpor ke Elasticsearch.

    Returns:
    None
    """
    es = Elasticsearch("http://localhost:9200") 
    for i,r in df_clean.iterrows():
        doc=r.to_json()
        res=es.index(index="gc7", body=doc)
        print('complete')

if __name__ == "__main__":
    df = get_data()
    df_clean = normalcolumn(df)
    save_data(df_clean)
    import_data(df_clean)
