Problem Statement: US Visa Approval Status
Given certain set of features such as continent, education, job experience, training, employment, current age etc, we need to predict whether the application for the visa will be approved or rejected. 

Features:
- case_id: ID of each visa application
- continent: Information of continent the employee
- education_of_employee: Information of education of the employee
- has_job_experience: Does the employee has any job experience? Y= Yes; N = No
- requires_job_training: Does the employee require any job training? Y = Yes; N = No
- no_of_employees: Number of employees in the employer's company
- yr_of_estab: Year in which the employer's company was established
- region_of_employment: Information of foreign worker's intended region of employment in the US.
- prevailing_wage: Average wage paid to similarly employed workers in a specific occupation in the area of intended employment. The purpose of the prevailing wage is to ensure that the foreign worker is not underpaid compared to other workers offering the same or similar service in the same area of employment.
- unit_of_wage: Unit of prevailing wage. Values include Hourly, Weekly, Monthly, and Yearly.
- full_time_position: Is the position of work full-time? Y = Full Time Position; N = Part Time Position
- case_status: Flag indicating if the Visa was certified or denied

Solution Proposed: 
I will be using machine learning
1. Load the data from database
2. Perform EDA and feature engineering to select the desireable features
3. Fit the ML classification algorithm and find out which one performs better.
4. Select the top few and peform hyperparameter tuning
5. Select the best model based on desired metrics. 