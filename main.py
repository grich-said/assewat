import calendar
import datetime

from geo_downloader import GeoDownloader_sentinel
from geojson_loader import GeoJsonLoaderNdvi
from landset_download import GeoDownloader_landset
from landset_transformer import geojson_transformer_landser

#smothing
if __name__ == '__main__':
    loader_ndvi=GeoJsonLoaderNdvi()
    years_list=[2020,2021]

    for year in years_list:
        # Loop over the months
        for month in range(1, 13):
            # Get the start and end dates for the month
            days_in_month = calendar.monthrange(year, month)[1]
            start_date = datetime.datetime(year, month, 1)
            end_date = datetime.datetime(year, month, days_in_month)
            print("----------------------------------------->",start_date,end_date)
            # downloader_sentinel = GeoDownloader_sentinel(is_verbose=False, selected_regions=["AL HAOUZ"], bands=['B4', 'B8'], startDate="2017-5-1",endDate="2017-5-30")
            downloader_landset = GeoDownloader_landset(is_verbose=False, selected_regions=["AL HAOUZ"], bands=['SR_B4', 'SR_B5'], startDate=start_date,endDate=end_date)

            # zones_data_sentinel = downloader_sentinel.runAll()
            zones_data_landset = downloader_landset.runAll()

            # transformer=geojson_transformer(zones_data_sentinel);
            transformer_landset=geojson_transformer_landser(zones_data_landset);

            docs=transformer_landset.to_raster();
            loader_ndvi.inset(docs)





