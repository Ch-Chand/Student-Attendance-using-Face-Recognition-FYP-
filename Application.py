# Importing Modules
import os
import datetime
import cv2 as cv
import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf
import streamlit_authenticator as stauth

# Some changes in App
hide_menu ="""
<style>
    #MainMenu {
        visibility:hidden;
</style>
"""

# Setting Paths
# Put the Project Here
path_proj = r"D:\CHAND's DATA\Study data\Semester's Data\Final Year Project"


# Navigation Bar
st.markdown(hide_menu, unsafe_allow_html=True)
rad = st.sidebar.radio("Select your Mode", ("Admin", "Professor"))

if rad == "Admin":
    names = ['Imran Nazir', 'Chand Ali']
    usernames = ['imran', 'chand']
    passwords = ['123', '456']

    hashed_passwords = stauth.hasher(passwords).generate()
    authenticator = stauth.authenticate(names, usernames, hashed_passwords,
                                        'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)

    name, authentication_status = authenticator.login('Login', 'main')

    if authentication_status:
        st.write('Welcome *%s*' % (name))
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Check System Detail")
            with st.expander(label="Check System Detail"):
                st.write("If you want to check the details of previously trained system then click here")
                btn_detail = st.button(label="Check Detail")
        with col2:
            st.subheader("Retrain your Application")
            with st.expander(label="Retrain your Application"):
                st.write("If you want to restart the system for a new class then first RESET the application")
                btn_reset = st.button(label="Reset")

        if btn_detail:
            hide_menu = """
            <style>
                #stblock {
                    visibility:hidden;
            </style>
            """
            st.markdown(hide_menu, unsafe_allow_html=True)
        if btn_reset:
            path = path_proj + "\\Project Data"
            try:
                if os.path.exists(path):
                    import shutil
                    shutil.rmtree(path)
                os.remove(path_proj + "\\Attendance_Notebook.csv")
                st.write("Reset Complete")
            except:
                st.write("Already Reset")

            # c1, c2 = st.columns(2)
            # with c1:
            #     btn_add = st.button(label="New Student")
            # with c2:
            #     btn_train = st.button(label="Train Model")
            #
            # print("-->", btn_add)
            # if btn_add:
            with st.form("Student Record", clear_on_submit=True):
                st.subheader("Give Students details")
                cl1, cl2, cl3 = st.columns(3)
                with cl1:
                    name = st.text_input(label="Student Name")
                with cl2:
                    rollno = st.number_input(label="Student Roll_No", min_value=1)
                with cl3:
                    session = st.text_input(label="Student Session")
                uploaded_file = st.file_uploader(label="Choose Student videos", type=["mp4", "mkv"], accept_multiple_files=False)
                submitted = st.form_submit_button("Submit")

                if submitted:
                    path = path_proj + "\\Project Data"
                    if os.path.exists(path):
                        # Storing Student Video
                        file = open(path + "\\Videos" + f"\\BS_{session}_{rollno}.mp4", "w")
                        file.write(uploaded_file)
                        file.close()

                        # Storing Student details
                        student_details = pd.read_csv(path + "\\Student_Details.csv")
                        row = {"Roll_No": rollno, "Name": name, "Session": session}
                        student_details = student_details.append(row)
                        student_details.sort_values("Roll_No", ascending=True)
                        student_details.to_csv(path + "\\Student_Details.csv")

                        # Displaying Student details
                        st.subheader("All Students Details")
                        st.dataframe(student_details)


    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')



##### ATTENDANCE FUNCTION START #####
def start_attendance(total_time):
    # Setting Paths to subdirectories of project
    path_proj = r"D:\CHAND's DATA\Study data\Semester's Data\Final Year Project"
    path_dat = path_proj + "\\Project Data"

    # Loading Face Cascade for detecting face from image
    face_cascade = cv.CascadeClassifier(path_dat + "\\" + "haarcascade_frontalface_default.xml")

    # Loading trained model
    model = tf.keras.models.load_model(path_dat + "\\model.h5")

    # Loading Notebook
    notebook = pd.read_csv(path_proj + "\\" + "Attendance_Notebook.csv")
    notebook.index = pd.to_datetime(notebook.index)



# st.title("Mark Student's Attendance")
# total_time = st.number_input("Set Timer", min_value=1, max_value=10)
# start = st.button("Start", on_click=start_attendance(total_time))
# pause = st.button("Pause")
#
# print(start)