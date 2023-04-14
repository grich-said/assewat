import os
import numpy as np
import rasterio
import datetime

class geojson_transformer_landser():
    def __init__(self, dataset):
        self.dataset = dataset
        self.output_dir = "/data/landset2/ndvi/"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def calculate_ndvi(self, red_band, nir_band):
        ndvi = np.where(
            (nir_band + red_band) == 0.,
            0,
            (nir_band - red_band) / (nir_band + red_band))
        return ndvi

    def to_raster(self):
        for dict_ in self.dataset:
            dict_["ndvi"] = []
            for image_dict in dict_["images"]:
                # Get the red and near-infrared bands
                red = image_dict["SR_B4"]
                nir = image_dict["SR_B5"]

                # Calculate the NDVI
                ndvi = self.calculate_ndvi(red, nir)

                # Get the image ID from the original image
                image_id = image_dict["id"]
                meta = image_dict["metadata"]

                if image_id.startswith("LANDSAT/LC08/C02/T1_L2"):
                    image_id = image_id[len("LANDSAT/LC08/C02/T1_L2"):]
                zone_output_dir = self.output_dir + dict_["zone"] + "/" + image_dict["date"] + "/"
                if not os.path.exists(zone_output_dir):
                    os.makedirs(zone_output_dir)

                # Define the output file name with the image ID
                output_file = zone_output_dir + image_id + "_ndvi.tif"

                # Write the NDVI image to a GeoTIFF file using rasterio
                with rasterio.open(output_file, "w", driver="GTiff", height=ndvi.shape[0], width=ndvi.shape[1], count=1,
                                   dtype=np.float32, nodata=-9999, crs="+init=epsg:32629", **meta,
                                   compress='lzw') as dst:
                    dst.write(ndvi, 1)
                dict_["ndvi"].append(
                    {"date": image_dict["date"], "geometry": image_dict["geometry"], "path": output_file,"product":"LANDSAT",
                     "created_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})
            dict_.pop("images")
        return self.dataset