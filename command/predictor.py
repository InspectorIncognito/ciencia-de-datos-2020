import argparse
import pandas as pd
import sys
#import pickle
import datetime

sys.path.append('../limpieza')
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
        "Servicio": [parsed_args_dict['machine'][0]["service"], parsed_args_dict['user']["service"]],
        "GPS_time": [parsed_args_dict['machine'][0]["measurement_time"], parsed_args_dict['user']["query_time"]],
        "DistanciaInicio": [parsed_args_dict['machine'][0]["route_distance"], parsed_args_dict['user']["route_distance"]],
        "DistanciaRuta": [0, 0],
        "Latitud": [0, 0],
        "Longitud": [0, 0]
    })
    data["DistanciaInicio"] = data["DistanciaInicio"].astype(int)
    data = limpieza.clean(data)
    #with open('../notebooks/encoding1.pickle', 'rb') as handle:
    #    servs_encoding = pickle.load(handle)
    #data['Servicio'] = data['Servicio'].apply(lambda x: servs_encoding[x])
    #print(data.values)
    pred = model.predict(data)
    #print(pred)
    #datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
    
    time_user = datetime.datetime.strptime(parsed_args_dict['user']["query_time"], '%Y-%m-%d %H:%M:%S')
    time_machine = datetime.datetime.strptime(parsed_args_dict['machine'][0]["measurement_time"], '%Y-%m-%d %H:%M:%S')
    
    delta = (time_user-time_machine)
    #print(delta)
    
    delta = datetime.timedelta(seconds = pred[0]) - delta
    time_user += delta

    # result example:
    result_list = [dict(license_plate=parsed_args_dict['machine'][0]["license_plate"], arrival_time=time_user.strftime("%Y-%m-%d %H:%M:%S"))]

    for result in result_list:
        print("- Machine '{0}' will arrive at '{1}'".format(result['license_plate'], result['arrival_time']))
