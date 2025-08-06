import folium


class Map(folium.Map):
    def __init__(self, center=(0, 0), zoom=3, **kwargs):
        super().__init__(location=center, zoom_start=zoom, **kwargs)
        folium.LayerControl().add_to(self)
