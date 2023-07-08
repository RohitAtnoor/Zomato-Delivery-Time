# First step is to Import the required librarys.
import os
import sys
from source.logger import logging
from source.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from source.utils import distance
from source.components.data_transformation import DataTransformation 

@dataclass
#dataclass is a function used to directly initilize the variables in a class with out the __init__ process.
#This process is used when we want to only initilize the variables, and there are no functions in the class.

class DataIngestionconfig:
    train_data_path:str=os.path.join('artifacts','train.csv')
    test_data_path:str=os.path.join('artifacts','test.csv')
    raw_data_path:str=os.path.join('artifacts','raw.csv')


# Third Step is to create a class for Data Ingection
class DataIngestion:
    # initilizing the variable.
    def __init__(self):
        self.ingestion_config = DataIngestionconfig()

     # Initiating the Data ingection process.
    def initiate_data_ingestion(self):
        logging.info('Data Ingestion methods Starts') 

        try:
            df = pd.read_csv("Notebooks/Data/finalTrain.csv")  # reading the main dataset.
            logging.info('Pandas completed reading the Dataset')

            # calculating the distance from the distance function from utilis. 
            df["Distance"] = df.apply(lambda row:distance(row['Restaurant_latitude'],row['Restaurant_longitude'],row['Delivery_location_latitude'],row['Delivery_location_longitude']),axis=1)
            df["Distance"] = df.apply(lambda row:distance(row['Restaurant_latitude'],row['Restaurant_longitude'],row['Delivery_location_latitude'],row['Delivery_location_longitude']),axis=1)

            def drop_features(df, feature):
                 df = df.drop([feature], axis=1, inplace=True)
                 return df

            drop_features(df, 'ID')
            drop_features(df, 'Delivery_person_ID')
            drop_features(df, 'Restaurant_latitude')
            drop_features(df, 'Restaurant_longitude')
            drop_features(df, 'Delivery_location_latitude')
            drop_features(df, 'Delivery_location_longitude')
            drop_features(df, 'Order_Date')
            drop_features(df, 'Time_Orderd')
            drop_features(df, 'Time_Order_picked')
 

            # copy of the main data set to another folder artifacts and new file.
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False)   # saving the dataset to another folder.
            logging.info('Copying of the Raw Data is complete, Train and Test spliting is started.')

            # Split the data set to Train and Test data set.
            # train_test_split will return the Train , Test data set. 
            train_set,test_set=train_test_split(df,test_size=0.30,random_state=42) 

            # save the Train dataset to new folder and file. 
            # self.ingestion_config.train_data_path is the path to save the trained dataset. 
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            # save the Test data set to new folder and file.
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info('Data Spliting and Ingestion of Data is completed')

            return(

                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        
        # If there is any error then we will raise the custom exception from exception.py file. 
        except Exception as e:
            logging.info('Exception occured at Data Ingestion stage')
            # e is the error occured and sys is the system error.
            raise CustomException(e,sys) 
            

# Test running this file.
'''
if __name__=='__main__':
    obj=DataIngestion()
    train_data_path,test_data_path=obj.initiate_data_ingestion()
    data_transformation = DataTransformation()
    train_arr,test_arr,_=data_transformation.initaite_data_transformation(train_data_path,test_data_path)
'''