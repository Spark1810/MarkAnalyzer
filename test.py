import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import pickle
from PIL import Image
import bamboolib as bam
import plotly.express as px
import matplotlib.pyplot as plt

sns.set()

st.title('Dr Grader : Unleash the Power of Data to Decode Your Academic Destiny')

activities = ["Introduction", "Histo Grader","Mark Analyzer", "About Us"]
choice = st.sidebar.selectbox("Select Activities", activities)
if choice == 'Introduction':
    st.markdown("Suggestive Histogram based grading for effective grading:")
    st.write("Histogram of Students marks are generated, sometimes due to lack of clear boundary marks of students are graded in a way that can be improved. We need to generate a system, which suggest effective way of grading students. ")

elif choice=="Histo Grader":
    st.sidebar.title("Data Upload")
    uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx", "xls"])
    if uploaded_file is not None:
        marks_df = pd.read_excel(uploaded_file)
        marks = marks_df["mark"].values
    # Create a histogram of student marks
    st.subheader("Student Marks Histogram")
    plt.figure(figsize=(8, 6))
    sns.histplot(marks, bins=10, kde=True)
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    st.pyplot()

    #   Calculate suggested grading boundaries
    grade_boundaries = [ 40, 60, 75, 90, 100]
    grades = ["F", "D", "C", "B", "A"]  

    # Create a function to suggest grades based on marks
    def suggest_grade(mark):
        for i, boundary in enumerate(grade_boundaries):
            if mark <= boundary:
                return grades[i]

    # Get user's input mark
    user_mark = st.slider("Enter your mark:", min_value=0, max_value=100, value=50)

    # Suggest a grade based on the user's mark
    suggested_grade = suggest_grade(user_mark)   

    # Display the suggested grade
    st.subheader("Suggested Grade")
    st.write(f"For a mark of {user_mark}, your suggested grade is {suggested_grade}")

    # Provide information about grading
    st.subheader("Grading Scheme")
    for i in range(len(grade_boundaries)):
        st.write(f"Grade {grades[i]}: Marks up to {grade_boundaries[i]}")

    # Statistical analysis report generation
    st.subheader("Statistical Analysis Report")
    if st.button("Generate Report"):
        stats_report = pd.DataFrame({
            "Statistic": ["Mean", "Median", "Standard Deviation", "Minimum", "Maximum"],
            "Value": [np.mean(marks), np.median(marks), np.std(marks), np.min(marks), np.max(marks)]
        })
        st.table(stats_report)


elif choice=="Mark Analyzer":
    uploaded_file=st.file_uploader('Upload your CSV file', type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df.head(3))
    df3=df
    bam.enable()

    st.header('Data Exploration and Manipulation')
    st.subheader(' ')

    # Add data exploration and manipulation steps using bamboolib
    col1, col2 = st.columns(2)

    # Add checkboxes to the first column
    with col1:
        st.set_option('deprecation.showPyplotGlobalUse', False)
        if st.checkbox("Correlation Plot"):
            plt.matshow(df3.corr())
            st.pyplot()

    # Add the filtered DataFrame to the second column
    with col2:
        if st.checkbox("Summary"):
            st.write(df3.describe())
    st.subheader(' ')
    st.subheader('Filtering Columns ')

    selected_column = st.selectbox('Select Column', df3.columns)

    # ======================================================================

    unique_values = df3[selected_column].unique()

    # Create a multiselect dropdown with the unique values
    selected_values = st.multiselect('Select Values to Filter ', unique_values)

    # Filter the DataFrame based on the selected values
    filtered_df = df3[df3[selected_column].isin(selected_values)]

    # Display the filtered DataFrame
    st.write(filtered_df)
    st.subheader(' ')
    st.subheader('Aggregation Function ')

    selected_function = st.selectbox('Select Function', ['Mean', 'Sum', 'Max', 'Min'])

    # Display the results
    st.subheader(f'{selected_function} of {selected_column}')
    st.write(df3.groupby(selected_column).agg(selected_function.lower()))

    # ======================================================================
    st.subheader(' ')
    st.subheader('Visualizations ')
    # Add data exploration and manipulation steps using bamboolib
    col3, col4 = st.columns(2)

    # Add checkboxes to the first column
    with col3:
        st.set_option('deprecation.showPyplotGlobalUse', False)
        column = st.selectbox('Select column to plot Y axis', df3.columns)
        column2 = st.selectbox('Select column to plot X axis', df3.columns)
        chart_type = st.radio('Select Chart Type', ('Line Chart', 'Bar Chart', 'Scatter Plot', 'Pie Chart','Histogram'))
        if chart_type == 'Line Chart':
            chart = px.line(df3, x=column2, y=column)
        elif chart_type == 'Bar Chart':
            chart = px.bar(df3, x=column2, y=column)
        elif chart_type == 'Scatter Plot':
            chart = px.scatter(df3, x=column2, y=column)
        elif chart_type == 'Pie Chart':
            chart = px.pie(df3, values=column2, names=column)
        elif chart_type == 'Histogram':
            plt.figure(figsize=(8, 6))
            sns.histplot(df3[column], bins=10, kde=True)
            plt.xlabel(column)
            plt.ylabel("Frequency")
            chart = plt
            st.pyplot()

    # Add the filtered DataFrame to the second column
    with col4:
        st.plotly_chart(chart)

elif choice == "About Us":
    st.header("CREATED BY _**TEAM MATRIX**_")