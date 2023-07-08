# First step to import the required libraries. 
import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder,StandardScaler

from source.exception import CustomException
from source.logger import logging
import os
from source.utils import save_object #distance 

# Second step to create a pickle file. 
@dataclass
class DataTransformationConfig:
    # We will be creating the preprocessor.pickle file in this path.
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')


# Third step if to create a class with the data transformation pipline
class DataTransformation:

    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    # function with data transformation pipeline. 
    def get_data_transformation_object(self):

        try:
            logging.info('Data Transformation initiated')
            # Define which columns should be ordinal-encoded and which should be scaled
            # saperating the numerical and categorical columns into saperate data tables. 
            categorical_cols = ['Weather_conditions', 'Road_traffic_density','Type_of_order','Type_of_vehicle','Festival','City']
            numerical_cols = ['Delivery_person_Age', 'Delivery_person_Ratings','Vehicle_condition', 'multiple_deliveries','Distance']

            # Define the custom ranking for each ordinal variable
            # giving the ranking to the different categories of the data in order ad convert to numeric.

            weather = ["Sunny","Cloudy","Windy","Fog","Stormy","Sandstorms"]
            Trafic = ['Low','Medium','High','Jam']
            Order = ['Snack','Drinks','Meal','Buffet']
            vehicle = ['bicycle','scooter','electric_scooter','motorcycle']
            festival = ['Yes','No']
            city = ['Urban','Semi-Urban','Metropolitian']

             # creating the pipelines
            logging.info('Pipeline Initiated')

             # Numerical Pipeline
            numerical_pipeline = Pipeline(
                steps = [
                    # For handeling the missing values of Numerical data
                    ("imputer",SimpleImputer(strategy= "median")), 
                    #standardize features by removing the mean and scaling to unit variance. 
                    # This means that each feature will have a mean of 0 and a standard deviation of 1
                    ("scaler",StandardScaler())
                ]
            )

            # Categorical Pipeline
            categorical_pipeline = Pipeline(
                steps = [
                    # For handeling the missing values of categorical data
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    # Used for giving the rank or the values for the different category.
                    ("OrdinalEncoding",OrdinalEncoder(categories=[weather,Trafic,Order,vehicle,festival,city])),
                    #standardize features by removing the mean and scaling to unit variance. 
                    # This means that each feature will have a mean of 0 and a standard deviation of 1
                    ("scaler",StandardScaler())
                ]
            )

            preprocessor = ColumnTransformer(
                [
                    # Inserting the pipelines to combine them together.
                    ("numerical_pipeline", numerical_pipeline, numerical_cols),
                    ("categorical_pipeline", categorical_pipeline, categorical_cols)
                ]
            )

            return preprocessor

            logging.info('Pipeline Completed')

        except Exception as e:
            logging.info("Error in Data Trnasformation")
            raise CustomException(e,sys)

    
    def initaite_data_transformation(self,train_path,test_path):
        try:
            # Reading train and test data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Read train and test data completed')
            logging.info(f'Train Dataframe Head : \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head  : \n{test_df.head().to_string()}')

            logging.info('Obtaining preprocessing object') 

            # output of completely transformed pipeline. 
            preprocessing_obj = self.get_data_transformation_object()

            '''
            # calculating the distance from the distance function from utilis. 
            train_df["Distance"] = train_df.apply(lambda row:distance(row['Restaurant_latitude'],row['Restaurant_longitude'],row['Delivery_location_latitude'],row['Delivery_location_longitude']),axis=1)
            test_df["Distance"] = test_df.apply(lambda row:distance(row['Restaurant_latitude'],row['Restaurant_longitude'],row['Delivery_location_latitude'],row['Delivery_location_longitude']),axis=1)

            target_column_name = 'Time_taken (min)'
            drop_columns = [target_column_name,'ID','Delivery_person_ID','Delivery_person_Ratings','Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude','Order_Date','Time_Orderd'.'Time_Order_picked']
            '''
            target_column_name = 'Time_taken (min)'
            drop_columns = [target_column_name]
            
            input_feature_train_df = train_df.drop(columns=drop_columns,axis=1)  # independent columns
            target_feature_train_df=train_df[target_column_name]   # Dependent column or table. 

            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column_name] 

            ## Trnasformating using preprocessor obj
            # fitting the train and test data sets. 
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df) 

            logging.info("Applying preprocessing object on training and testing datasets.")
            
            # converting the data into array for easy ritrival process. 
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            # importing save object from utilis.py file to save the pickle file. 
            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )
            logging.info('Preprocessor pickle file saved')

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            logging.info("Exception occured in the initiate_datatransformation")

            raise CustomException(e,sys)
            