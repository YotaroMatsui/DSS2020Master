import pandas as pd
from pandas import DataFrame
# from arcgis.gis import GIS
# from arcgis import geocoding
import googlemaps
import ssl
import os

def arcgis_geocode(df: DataFrame, arcgis_user: str, arcgis_pass: str):
    ssl._create_default_https_context = ssl._create_unverified_context
    arcgis_user = arcgis_user
    arcgis_pass = arcgis_pass

    my_gis = GIS('https://www.arcgis.com', arcgis_user, arcgis_pass)

    # arcGis
    for index, row in df.iterrows():
        address = row['医療機関所在地']
        print(address)  # GeoCodingする住所設定
        result = geocoding.geocode(address)
        try:
            print(result[0]['location']['y'])  # 緯度の表示
            print(result[0]['location']['x'])  # 経度の表示
            print(result[0]['score'])  # 一致スコアの表示
            df.at[index, 'X'] = result[0]['location']['x']
            df.at[index, 'Y'] = result[0]['location']['y']
            df.at[index, 'ArcGIS Score'] = result[0]['score']
            if result[0]['score'] == 100:
                df.at[index, 'Manual'] = 0
        except IndexError:
            pass
    return df


def google_geocode(googleapikey: str, df: DataFrame, row_name: str):
    googleapikey = googleapikey
    gmaps = googlemaps.Client(key=googleapikey)
    count = 0

    for index, row in df[df['Manual'] == 1].iterrows():
        if count >= 1000:
            print('The number of times geocoding has reached the APIs usage limit.')
            break

        address = row[row_name]
        # print(address)  # GeoCodingする住所設定
        result = gmaps.geocode(address)[0]
        # print(result['geometry']['location_type'])  # google scoreの精度が出る
        count += 1

        try:
            print(result['geometry']['location']['lat'])  # 緯度の表示
            print(result['geometry']['location']['lng'])  # 経度の表示
            df.at[index, 'X'] = result['geometry']['location']['lng']  # x
            df.at[index, 'Y'] = result['geometry']['location']['lat']  # y
            df.at[index, 'Google Score'] = result['geometry']['location_type']  # Google Scoreの置換
            if result['geometry']['location_type'] == 'ROOFTOP':
                df.at[index, 'Google Score'] = 100
                df.at[index, 'Manual'] = 0
        except IndexError:
            pass
    return df


if __name__ == '__main__':
    arcgis_usr = os.environ['GIS_USER_NAME']
    arcgis_ps = os.environ['GIS_PASSWORD']
    google_api_key = os.environ['GOOGLE_API_KEY']
    print('google_api_key is ')
    print(google_api_key)

    input_file_path = '../../../resource/Term2/train2.csv'
    output_file_path = '../../../resource/Term2/train2.csv'

    input_df = pd.read_csv(input_file_path)
    input_df['Manual'] == 1
    # output_df = arcgis_geocode(input_df, arcgis_user=arcgis_usr, arcgis_pass=arcgis_ps)
    output_df = google_geocode(googleapikey=google_api_key, df=input_df, row_name='所在地')

    output_df.to_csv(output_file_path)
