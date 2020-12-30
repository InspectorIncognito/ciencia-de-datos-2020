import argparse
import pandas as pd
import sys
import numpy as np

#sys.path.append('../limpieza')
sys.path.append('..')
import limpieza
import model

def arguments_to_dict(arguments):
    arg_dict = dict(
        user=dict(service=arguments.user[0], route_distance=arguments.user[1], query_time=arguments.user[2]),
        machine=list()
    )
    for machine in arguments.machine:
        arg_dict['machine'].append(dict(
            license_plate=machine[0], service=machine[1], route_distance=machine[2], measurement_time=machine[3]
        ))
    return arg_dict

def indices_to_one_hot(data, nb_classes=7):
    days = np.array(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    dummies = pd.get_dummies(days, columns=['dias'], drop_first=False) 
    df = pd.DataFrame(dummies[data].T.values, columns=["dia_"+d for d in days])
    return df

def clean(data):
    data = limpieza.gpsDia(data)
    data = limpieza.servicio(data)
    data = limpieza.distancia(data)
    data = limpieza.notnull_serv(data)
    data = limpieza.habilday(data)
    cod = indices_to_one_hot(data["dias"])
    data = pd.concat([data, cod], axis=1)
    data = data.drop(columns=['dias', 'GPS_time', 'dia_Friday'])
    data = pd.concat([data.iloc[0].add_suffix('1'), data.iloc[1].add_suffix('2')], axis=0)
    data = pd.DataFrame(data).transpose()
    data = data.drop(columns=["Servicio2", "dia_habil2", "dia_Monday2", "dia_Saturday2", "dia_Sunday2", "dia_Thursday2", "dia_Tuesday2", "dia_Wednesday2"])

    data = limpieza.normalize(data)
    data = data.drop(columns=["Latitud1", "Longitud1", "Latitud2", "Longitud2", "Servicio1"])
    return data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate predictions using --user and --machine descriptors')
    parser.add_argument('--user', required=True, nargs=3,
                        metavar=("<service>", "<route_distance>", "<query_time>"),
                        help='User descriptors. <query_time> is in local time. '
                             'Example: --user "T506 00I" 3200 "2020-08-20 14:05:00"')
    parser.add_argument('--machine', required=True, nargs=4, action='append',
                        metavar=("<license_plate>", "<service>", "<route_distance>", "<measurement_time>"),
                        help='machine descriptors. <measurement_time> is in local time. '
                             'Example: --machine AABB11 "T506 00I" 1234 "2020-08-20 14:00:00"')
    args = parser.parse_args()
    parsed_args_dict = arguments_to_dict(args)
    # Here you should call the prediction method with the parsed argument to generate the results.
    data = pd.DataFrame({
        "Servicio": [parsed_args_dict['user']["service"], parsed_args_dict['machine'][0]["service"]],
        "GPS_time": [parsed_args_dict['user']["query_time"], parsed_args_dict['machine'][0]["measurement_time"]],
        "DistanciaInicio": [parsed_args_dict['user']["route_distance"], parsed_args_dict['machine'][0]["route_distance"]],
        "DistanciaRuta": [0, 0],
        "Latitud": [0, 0],
        "Longitud": [0, 0]
    })
    data["DistanciaInicio"] = data["DistanciaInicio"].astype(int)
    data = clean(data)
    pred = model.predict(data)
    print(pred)


    # result example:
    result_list = [dict(license_plate="AABB11", arrival_time="2020-08-20 14:06:00"),
                   dict(license_plate="CCDD11", arrival_time="2020-08-20 14:05:45")]

    for result in result_list:
        print("- Machine '{0}' will arrive at '{1}'".format(result['license_plate'], result['arrival_time']))
