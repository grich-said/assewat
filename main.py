from geo_downloader import GeoDownloader
from geojson_loader import GeoJsonLoaderNdvi
from geojson_transformer import geojson_transformer

if __name__ == '__main__':

    downloader = GeoDownloader(is_verbose=False, selected_regions=["CHICHAOUA"], bands=['B4', 'B8'], startDate="2019-2-18",
                     endDate="2019-2-26")
    zones_data = downloader.getRegionList()
    transformer=geojson_transformer(zones_data);
    loader_ndvi=GeoJsonLoaderNdvi()
    docs=transformer.to_raster();
    for doc in docs:
        loader_ndvi.insetOne(doc)



