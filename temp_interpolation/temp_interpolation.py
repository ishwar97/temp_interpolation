"""Main module."""

import os
import ipyleaflet


class Map(ipyleaflet.Map):
    def __init__(self, center=[19, 72], zoom=2, height="600px", **kwargs):
        """Map class to create Map View

        Args:
            center (list, optional): Map Center. Defaults to [19, 72]
            zoom (int, optional): Zoom level. Defaults to 2.
            height (str, optional): Map Height. Defaults to "600px".
        """
        super().__init__(center=center, zoom=zoom, **kwargs)
        self.layout.height = height
        self.scroll_wheel_zoom = True

    def add_basemap(self, basemap="OpenTopoMap"):
        """Adds basemap to Map View

        Args:
            basemap (str, optional): Base Map. Defaults to "OpenTopoMap".
        """

        try:
            url = eval(f"ipyleaflet.basemaps.{basemap}").build_url()
            layer = ipyleaflet.TileLayer(url=url, name=basemap)
            self.add_layer(layer)
        except:
            url = eval(f"ipyleaflet.basemaps.OpenTopoMap").build_url()
            layer = ipyleaflet.TileLayer(url=url, name=basemap)
            self.add_layer(layer)

    def add_google_map(self, map_type="ROADMAP"):
        """Adds Google Maps layer to Map View

        Args:
            map_type (str, optional): Type of Google Map.
                Defaults to "ROADMAP". Available options : "ROADMAP", "SATELLITE", "HYBRID","TERRAIN"
        """

        map_types = {"ROADMAP": "m", "SATELLITE": "s", "HYBRID": "h", "TERRAIN": "t"}
        map_type = map_types[map_type.upper()]

        url = (
            f"https://mt1.google.com/vt/lyrs={map_type.lower()}&x={{x}}&y={{y}}&z={{z}}"
        )
        layer = ipyleaflet.TileLayer(url=url, name="Google Map")
        self.add_layer(layer)

    def add_vector(
        self,
        vector,
        zoom_to_layer=True,
        hover_style=None,
        **kwargs,
    ):
        """Adds Vector layer to Map View

        Args:
            vector (str or dict): URL or path to vector file. Can be a shapefile, GeoDataFrame, GeoJSON, etc.
            zoom_to_layer (bool, optional): Whether to zoom to added layer. Defaults to True.
            hover_style (dict, optional): Style to apply on hover. Defaults to Defaults to {'color':'yellow', 'fillOpacity':0.2}.
            **kwargs: Additional keyword arguments passed to ipyleaflet.GeoJSON.
        """

        import geopandas as gpd

        if hover_style is None:
            hover_style = {"color": "yellow", "fillOpacity": 0.2}

        if isinstance(vector, str):
            gdf = gpd.read_file(vector)
            gdf = gdf.to_crs(epsg=4326)
            data = gdf.__geo_interface__
        elif isinstance(vector, dict):
            data = vector

        gjson = ipyleaflet.GeoJSON(data=data, hover_sytle=hover_style, **kwargs)
        self.add_layer(gjson)

        if zoom_to_layer:
            bounds = gdf.total_bounds
            self.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

    def add_layer_control(self):
        """Adds Layer Control Button to Map View

        This control allows users to toggle the visibility of layers.
        """
        self.add_control(control=ipyleaflet.LayersControl())

    def add_raster(self, url, name=None, colormap=None, opacity=None, **kwargs):
        """Adds Raster layer to Map View

        Args:
            url (str): URL or path to raster file. Can be a GeoTIFF, rasterio object, etc.
            name (str, optional): Name of the layer. Defaults to None.
            colormap (function, optional): Colormap function to apply to raster values. Defaults to None.
            zoom_to_layer (bool, optional): Whether to zoom to added layer. Defaults to True.
            **kwargs: Additional keyword arguments passed to ipyleaflet.ImageOverlay.
        """
        from localtileserver import TileClient, get_leaflet_tile_layer

        client = TileClient(url)
        tile_layer = get_leaflet_tile_layer(
            client, name=name, colormap=colormap, opacity=opacity, **kwargs
        )
        self.add_layer(tile_layer)
        self.center = client.center()
        self.zoom = client.default_zoom

    def add_image(
        self,
        url,
        bounds,
        opacity=1,
        **kwargs,
    ):
        """Adds Image layer to Map View

        Args:
            url (str): URL or path to image file. Can be a PNG, JPEG, etc.
            bounds (list): Bounds of the image in the format [[south, west], [north, east]].
            opacity (float, optional): Opacity of the image layer. Defaults to 1.
            **kwargs: Additional keyword arguments passed to ipyleaflet.ImageOverlay.
        """

        layer = ipyleaflet.ImageOverlay(
            url=url,
            bounds=bounds,
            opacity=opacity,
            **kwargs,
        )
        self.add_layer(layer)

    def add_video(
        self,
        url,
        bounds,
        opacity=1,
        **kwargs,
    ):
        """Adds Video layer to Map View

        Args:
            url (str): URL or path to video file. Can be a MP4, OGG, etc.
            bounds (list): Bounds of the video in the format [[south, west], [north, east]].
            opacity (float, optional): Opacity of the video layer. Defaults to 1.
            **kwargs: Additional keyword arguments passed to ipyleaflet.VideoOverlay.
        """

        layer = ipyleaflet.VideoOverlay(
            url=url,
            bounds=bounds,
            opacity=opacity,
            **kwargs,
        )
        self.add_layer(layer)

    def add_wms_layer(
        self,
        url,
        layers,
        name=None,
        format="image/png",
        transparent=True,
        version="1.1.1",
        **kwargs,
    ):
        """Adds WMS layer to Map View

        Args:
            url (str): URL of the WMS service.
            layers (str): Comma-separated list of layer names to add.
            name (str, optional): Name of the layer. Defaults to None.
            format (str, optional): Image format. Defaults to "image/png".
            transparent (bool, optional): Whether the image should have transparency. Defaults to True.
            version (str, optional): WMS version. Defaults to "1.1.1".
            **kwargs: Additional keyword arguments passed to ipyleaflet.WMSLayer.
        """

        layer = ipyleaflet.WMSLayer(
            url=url,
            layers=layers,
            name=name,
            format=format,
            transparent=transparent,
            version=version,
            **kwargs,
        )
        self.add_layer(layer)
