import streamlit as st
import pymysql
from tensorflow.keras.utils import load_img
from keras.models import load_model
import numpy as np

model = load_model('maogou.h5',compile=False)
st.set_page_config(page_title="西华大学猫与狗区分网站",layout="wide")

con = pymysql.connect(host="localhost", user="root", password="root",database="test1",charset="utf8")

c= con.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')

def add_userdata(username,password):

     if c.execute('SELECT username FROM userstable WHERE username = %s',(username)):
        st.warning("用户名已存在，请更换一个新的用户名。")
     else:
          c.execute('INSERT INTO userstable(username,password) VALUES(%s,%s)',(username,password))
          con.commit()
          st.success("恭喜，您已成功注册。")
          st.info("请在左侧选择“登录”选项进行登录。")

def login_user(username,password):
   if c.execute('SELECT username FROM userstable WHERE username = %s',(username)):
       c.execute('SELECT * FROM userstable WHERE username = %s AND password = %s',(username,password))
       data=c.fetchall()
       return data
   else:
       st.warning("用户名不存在，请先选择注册按钮完成注册。")

def view_all_users():
   c.execute('SELECT * FROM userstable')
   data = c.fetchall()
   return data



def main():
   menu = ["首页","登录","注册", "注销"]

   if 'count' not in st.session_state:
       st.session_state.count = 0

   choice = st.sidebar.selectbox("选项",menu)
   st.sidebar.markdown(
   """
   <style>
   [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
       width: 250px;
   }
   [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
       width: 250px;
       margin-left: -250px;
   }
   </style>
   """,
   unsafe_allow_html=True,)

   if choice =="首页":
       st.subheader("首页")
       st.write('这个网站展示了如何识别猫猫和狗狗')
       st.image('https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png', width=250)
       c1, c2 = st.columns(2)
       with c1:
          st.header("A cat")
          st.image("https://static.streamlit.io/examples/cat.jpg")
       with c2:
           st.header("A dog")
           st.image("https://static.streamlit.io/examples/dog.jpg")

   elif choice =="登录":
       st.sidebar.subheader("登录区域")

       username = st.sidebar.text_input("用户名")
       password = st.sidebar.text_input("密码",type = "password")
       if st.sidebar.checkbox("开始登录"):
           logged_user = login_user(username,password)
           if logged_user:

               st.session_state.count += 1

               if st.session_state.count >= 1:

                   st.sidebar.success("您已登录成功，您的用户名是 {}".format(username))

                   st.title("成功登录后可以看到的内容")
                   st.balloons()
                   st.header('欢迎光临')
                   uploaded_file = st.file_uploader("当你不知道如何区分图片中的猫狗的时候，请选择一张图片上传",type=["jpg", "jpeg", "png"])
                   if uploaded_file is not None:
                      img = load_img(uploaded_file, target_size=(150, 150))
                      x = np.expand_dims(img, axis=0)
                      x = x / 255.0
                      prediction = model.predict(x)
                      if prediction < 0.5:
                         st.write("这是一张猫的图片")
                      else:
                         st.write("这是一张狗的图片")
                      st.image(img, caption='Uploaded Image', use_column_width=True)
                   
           else:
               st.sidebar.warning("用户名或者密码不正确，请检查后重试。")   

   elif choice =="注册":
       st.subheader("注册")
       new_user = st.sidebar.text_input("用户名")
       new_password = st.sidebar.text_input("密码",type = "password")

       if st.sidebar.button("注册"):
            create_usertable()
            add_userdata(new_user,new_password)

   elif choice =="注销":
        st.session_state.count = 0
        if st.session_state.count == 0:
            st.info("您已成功注销，如果需要，请选择左侧的登录按钮继续登录。")


if __name__ == '__main__':
   main()
