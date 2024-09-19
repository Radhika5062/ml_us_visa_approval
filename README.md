Problem Statement: US Visa Approval Status
Given certain set of features such as continent, education, job experience, training, employment, current age etc, we need to predict whether the application for the visa will be approved or rejected. 

Features:
- Continents: Asia, Africa, North America, Europe, South America, Oceania
- Education: High School, Master's degree, Bachelor's. Doctorate
- Job experience: Yes, No
- Required training: Yes, No
- Number of employees: 15000 to 40000
- Region of employment: West, Northeast, South, Midwest, Island
- Prevailing Wage: 700 to 70000
- Contract tenure: Hour, Year, Week, Month
- Full time: Yes, No
- Age of company: 15 to 180

Solution Proposed: 
We will be using machine learning
1. Load the data from database
2. Perform EDA and feature engineering to select the desireable features
3. Fit the ML classification algorithm and find out which one performs better.
4. Select the top few and peform hyperparameter tuning
5. Select the best model based on desired metrics. 