import ee
from geeS2downloader import GEES2Downloader
import tqdm
from tqdm import tqdm
import logging
import sys
import datetime


class GeoDownloader_landset():
    def __init__(self, is_verbose=False, selected_regions=[], bands=['SR_B4', 'SR_B5'], startDate="", endDate=""):
        # configuring log
        if (is_verbose):
            self.log_level = logging.DEBUG
        else:
            self.log_level = logging.INFO
        log_format = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
        self.log = logging.getLogger(__name__)
        self.log.setLevel(self.log_level)

        # writing to stdout
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(self.log_level)
        handler.setFormatter(log_format)
        self.log.addHandler(handler)

        self.log.debug("test")
        self.selected_regions = selected_regions
        self.product_id = 'LANDSAT/LC08/C02/T1_L2'
        self.startDate = startDate
        self.endDate = endDate
        self.isAuthenticate = True;
        self.isInit = False
        self.regions = []
        self.downloader = ""
        self.bands = bands

    def authenticate(self):
        ee.Authenticate()
        self.isAuthenticate = True

    def initialaze(self):
        if self.isAuthenticate:
            ee.Initialize()
            table_asset = ee.FeatureCollection("projects/ee-sswaad06/assets/provinces")
            self.regions = table_asset.getInfo()['features']
            self.downloader = GEES2Downloader()
            self.isInit = True
        else:
            self.log.error("You must Authenticated Fisrt !")

    def getRegionList(self):
        if self.isInit:
            self.region_list = [feature['properties']['Nom_Provin'] for feature in self.regions]
            return self.region_list
        else:
            self.initialaze()
            self.region_list = [feature['properties']['Nom_Provin'] for feature in self.regions]
            self.log.error("You must Init the Gee  Fisrt !")
            return self.region_list


    def getRegionSublist(self):
        subRegionList = []
        for re in self.regions:
            if re['properties']['Nom_Provin'] in self.selected_regions:
                subRegionList.append(re);

        self.redyToDownlaodList = subRegionList;
        return subRegionList

    def get_date_from_image_id(self, image_id):
        # Extract the date substring from the image ID
        if(self.product_id=='LANDSAT/LC08/C02/T1_L2'):
            date_str = image_id.split("_")[-1]
            date_obj = datetime.datetime.strptime(date_str, '%Y%m%d')
            formatted_date = date_obj.strftime('%Y-%m-%d')

        # Return the formatted date as a string
        return formatted_date


    def downalodImages_landset(self):
        cloud_thresh=20
        zones_images = []
        for feature in tqdm(self.redyToDownlaodList):
            feature_dict = {}
            feature_dict["images"] = []
            feature_dict["zone"] = feature['properties']['Nom_Provin']
            feature_dict["geometry"] = feature['geometry']

            # Get the geometry of the feature
            geometry = ee.Geometry(feature['geometry'])
            # Load the Landsat images for the defined date range and geometry

            collection = ee.ImageCollection(self.product_id) \
                .filterDate(self.startDate, self.endDate) \
                .filterBounds(geometry)\
                .filterMetadata('CLOUD_COVER', 'less_than', cloud_thresh)
            collection = collection.map(self.maskClouds)
            print("----------------------------------->",len(collection.getInfo()['features']))
            for image in collection.getInfo()['features']:
                bands_dict = {}
                image_id = image['id']
                image = ee.Image(image_id)
                cloud_cover = image.get('CLOUD_COVER').getInfo()
                bands_dict['date'] = ee.Date(image.date())
                bands_dict['id'] = image_id
                bands_dict["geometry"]=image.geometry().getInfo()
                bands_dict["date"] = self.get_date_from_image_id(image_id)
                metadata=image.getInfo()["properties"]
                bands_dict["metadata"]=metadata
                for band in self.bands:
                    if band =="SR_B4":
                        band2 = image.select(band)
                        # Get the projection information
                        projection = band2.projection()
                        # Get the affine transformation matrix
                        transform = projection.getInfo()['transform']
                        bands_dict["metadata"]["transform"]=transform
                        bbox = band2.geometry().bounds().getInfo()['coordinates'][0]
                        # Print the CRS
                    # Print the transformation matrix
                    self.downloader.download(img=image, band=band)
                    bands_dict[band] = self.downloader.array
                feature_dict["images"].append(bands_dict)

            zones_images.append(feature_dict)
        return zones_images

    def maskClouds(self,image):
        # Extract the QA band
        qa = image.select('QA_PIXEL')
        # Bits 2 and 3 indicate clouds and cloud shadows, respectively
        cloudMask = qa.bitwiseAnd(1 << 2).neq(0) \
            .Or(qa.bitwiseAnd(1 << 3).neq(0))
        # Apply the mask to the image and return it
        return image.updateMask(cloudMask.Not())

    def runAll(self):
        if not self.isAuthenticate:
            self.authenticate()
        if not self.isInit:
            self.initialaze()
        self.getRegionSublist()

        return self.downalodImages_landset()