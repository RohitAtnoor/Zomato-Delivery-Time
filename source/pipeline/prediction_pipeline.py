import sys
import os
from source.exception import CustomException
from source.logger import logging
from source.utils import load_object
import pandas as pd

# creating the class for predicting the new data. 
class PredictPipeline:
    def __init__(self):
        pass
    
    # function returns the predicted value.
    # features is the input columns details.
    def predict(self,features):
        try:
            # getting the preprocessor and model pickle files path. 
            preprocessor_path=os.path.join('artifacts','preprocessor.pkl')
            model_path=os.path.join('artifacts','model.pkl')

            # opening the preprocessor and model file 
            # load_object is function in utilis to open the files. 
            preprocessor=load_object(preprocessor_path)
            model=load_object(model_path)

            # transforming the new data. 
            data_scaled=preprocessor.transform(features)

            # predicting the price. 
            pred=model.predict(data_scaled)
            return pred
            

        except Exception as e:
            logging.info("Exception occured in prediction")
            raise CustomException(e,sys)

class CustomData:
    def __init__(self,
                 Delivery_person_Age:float,
                 Delivery_person_Ratings:float,
                 Weather_conditions:str,
                 Road_traffic_density:str,
                 Vehicle_condition:int,
                 Type_of_order:str,
                 Type_of_vehicle:str,
                 multiple_deliveries:float,
                 Festival:str,
                 City:str,
                 Distance:float) -> None:
        
        self.Delivery_person_Age = Delivery_person_Age
        self.Delivery_person_Ratings = Delivery_person_Ratings
        self.Weather_conditions = Weather_conditions
        self.Road_traffic_density = Road_traffic_density
        self.Vehicle_condition = Vehicle_condition
        self.Type_of_order = Type_of_order
        self.Type_of_vehicle = Type_of_vehicle
        self.multiple_deliveries = multiple_deliveries
        self.Festival = Festival
        self.City = City
        self.Distance = Distance

# storing the variables in the dictionary and converting to Dataframe. 
    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'Delivery_person_Age':[self.Delivery_person_Age],
                'Delivery_person_Ratings':[self.Delivery_person_Ratings],
                'Weather_conditions':[self.Weather_conditions],
                'Road_traffic_density':[self.Road_traffic_density],
                'Vehicle_condition':[self.Vehicle_condition],
                'Type_of_order':[self.Type_of_order],
                'Type_of_vehicle':[self.Type_of_vehicle],
                'multiple_deliveries':[self.multiple_deliveries], 
                'Festival':[self.Festival],
                'City':[self.City],
                'Distance':[self.Distance]
            }
            df = pd.DataFrame(custom_data_input_dict)
            logging.info('Dataframe Gathered')
            return df
        except Exception as e:
            logging.info('Exception Occured in prediction pipeline')
            raise CustomException(e,sys)