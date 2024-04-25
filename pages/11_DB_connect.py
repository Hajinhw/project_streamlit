import streamlit as st

# mysql 연결(접속)
conn = st.connection('shopdb',
                    type='sql',
                    url='mysql://streamlit:1234@localhost:3306/shopdb')

# 질의 수행
df = conn.query('SELECT * FROM customer;', ttl=600)

st.write(df)

# for row in df.itertuples():
#     st.write(f'이름 : {row.customer_name}, 번호 : {row.phone}')
#
# sql = '''INSERT INTO customer (customer_id, customer_name, phone, birthday)
#  values (:id, :name, :phone, :birth);'''
#
# with conn.session as s:
#     s.execute(sql, {'id':6, 'name':"홍길동", 'phone':"010-1111-1111", 'birth':"2000-01-30"})
#     s.commit()
#
# df = conn.query('SELECT * FROM customer;', ttl=600)
# st.write(df)

