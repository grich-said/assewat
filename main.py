from geo_downloader import GeoDownloader
from geojson_loader import GeoJsonLoaderNdvi
from geojson_transformer import geojson_transformer

if __name__ == '__main__':
    loader_ndvi=GeoJsonLoaderNdvi()
    downloader = GeoDownloader(is_verbose=False, selected_regions=["AL HAOUZ","CHICHAOUA"], bands=['B4', 'B8'], startDate="2019-6-1",endDate="2019-8-30")
    zones_data = downloader.runAll()
    transformer=geojson_transformer(zones_data);
    docs=transformer.to_raster();
    loader_ndvi.inset(docs)





