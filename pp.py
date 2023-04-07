import streamlit as st
st.set_page_config(layout="wide")
from tensorflow.keras.utils import load_img
from keras.models import load_model
import numpy as np

# 定义用户名和密码
username = "admin"
password = "password"

# 创建登录页面

st.title("用户登录")

form = st.form(key='login_form')
form.text_input('用户名')
password_input = form.text_input('密码', type='password')

submit_button = form.form_submit_button(label='登录')

# 验证用户名和密码是否正确
if  submit_button and password_input == password:
    st.success("登录成功！")
    st.title('西华大学猫狗区分网')

    with st.expander('关于本网站'):
        st.write('这个网站展示了如何识别猫猫和狗狗')
        st.image('https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png', width=250)

    st.sidebar.header('欢迎光临')
    user_name = st.sidebar.text_input('您的名字？')
    user_emoji = st.sidebar.selectbox('选择一个 emoji 吧', ['', '😄', '😆', '😊', '😍', '😴', '😕', '😱'])
    user_food = st.sidebar.selectbox('您最喜欢的食物是什么呢？', ['', 'Tom Yum Kung', 'Burrito', 'Lasagna', 'Hamburger', 'Pizza'])

    st.header('你好，请输入你的基本信息，以便我们预测你喜欢猫还是喜欢狗')

    col1, col2, col3 = st.columns(3)

    with col1:
        if user_name != '':
            st.write(f'👋 Hello {user_name}!')
        else:
            st.write('👈  请键入你的 **名字**!')

    with col2:
        if user_emoji != '':
            st.write(f'{user_emoji}是你最喜欢的 **emoji**!')
        else:
            st.write('👈 请选择一个 **emoji**!')

    with col3:
        if user_food != '':
            st.write(f'🍴 **{user_food}** 是你最喜欢的 **食物**!')
        else:
            st.write('👈 请选择你最喜欢的 **食物**!')

    st.title('年龄和性别')

    # 添加滑动条组件，用于选择年龄
    age = st.slider('请选择您的年龄', 0, 130, 25)

    # 添加单选框组件，用于选择性别
    gender = st.radio('请选择您的性别', ('男', '女'))

    # 添加按钮，用于记录年龄和性别并显示结果
    if st.button('上传'):
        st.write(f'您选择的年龄是：{age} 岁，性别是：{gender}')

    # 加载训练好的模型
    model = load_model('maogou.h5')

    # 添加文件上传组件，用户可以上传待分类的图像
    uploaded_file = st.file_uploader("当你不知道如何区分图片中的猫狗的时候，请选择一张图片上传", type=["jpg", "jpeg", "png"])

    # 如果用户上传了图像
    if uploaded_file is not None:
        # 加载图像
        img = load_img(uploaded_file, target_size=(150, 150))
        # 将图像转化为numpy数组
        x = np.expand_dims(img, axis=0)
        # 对图像进行预处理
        x = x / 255.0
        # 使用模型进行预测
        prediction = model.predict(x)
        # 根据预测结果显示对应的标签
        if prediction < 0.5:
            st.write("这是一张猫的图片")
        else:
            st.write("这是一张狗的图片")
        # 显示上传的图像
        st.image(img, caption='Uploaded Image', use_column_width=True)
    st.header('')

    option = st.selectbox(
        '你最喜欢的动物是?',
        ('修狗', '小猫'))

    st.write('你最喜欢的动物是 ', option)
    import time

    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.005)
        my_bar.progress(percent_complete + 1)

    st.balloons()
elif    submit_button and password_input != password:
            st.error("用户名或密码错误！")