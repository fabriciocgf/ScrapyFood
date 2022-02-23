#import contextily as ctx
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon, MultiPolygon
import folium
import numpy as np
#import fiona
import streamlit as st
import os
from streamlit_folium import folium_static

def app():
    if 'button1' not in st.session_state:
        st.session_state.button1 = False

    st.markdown("## GIS Analysis")
    left_column, right_column = st.columns(2)
    with left_column:
        if st.button('Proceed using database from second step'):
            df = pd.read_csv("Restaurants.csv")
            st.session_state.button1 = True
    with right_column:
        uploaded_file = st.file_uploader('Upload your links')
        if uploaded_file is not None:
            if not st.session_state.button1:
                st.write('Loading your Database')
                with open(os.path.join(uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                os.rename(uploaded_file.name, 'Restaurants.csv')
                df = pd.read_csv("Restaurants.csv")
                st.session_state.button1 = True

    if st.session_state.button1:
        st.write('Database Loaded')
        st.markdown("## Let's see the distribution of our data")
        df['Lat'].replace('', np.nan, inplace=True)
        df.dropna(subset=['Lat'], inplace=True)
        df = df.reset_index(drop=True)
        geometry = df.apply(lambda row: Point(row.Long, row.Lat), axis=1)
        gdf = gpd.GeoDataFrame(df.drop(['Lat', 'Long'], axis=1), geometry=geometry, crs="EPSG:4326")  # projeção long lat

        m = gdf.explore(
            column="Bairro",  # make choropleth based on "BoroName" column
            tooltip="Nome",  # show "BoroName" value in tooltip (on hover)
            popup=True,  # show all values in popup (on click)
            tiles="cartodbpositron",
            legend=False,
            name="Restaurants"
            , width=1000, height=800
        )

        new_crs = gdf.to_crs(crs='EPSG:22523')  # projeção utm corrego alegre
        buffer_union = new_crs.buffer(1200).unary_union  # foi necessário mudar a projeção para que se possa usar a unidade do buffer em metros
        buffer_union_gdf = gpd.GeoDataFrame(geometry=[buffer_union], crs=new_crs.crs)
        buffer_union_gdf.explore(m=m, tiles="cartodbpositron", name="Area", tooltip=False)

        folium.LayerControl().add_to(m)  # use folium to add layer control

        folium_static(m)

        st.markdown("## How is it concentrated")
        # Create thresholds
        levels = np.linspace(0, 1, 13)
        levels = levels[1:]
        # Create plot
        f, ax = plt.subplots(ncols=1, figsize=(20, 8))
        # Kernel Density Estimation
        kde = sns.kdeplot(
            ax=ax,
            x=gdf['geometry'].x,
            y=gdf['geometry'].y,
            levels=levels,
            shade=True,
            cmap='Reds',
            alpha=0.5
        )

        level_polygons = []
        i = 0
        for col in kde.collections:
            paths = []
            # Loop through all polygons that have the same intensity level
            for contour in col.get_paths():
                # Create a polygon for the countour
                # First polygon is the main countour, the rest are holes
                for ncp, cp in enumerate(contour.to_polygons()):
                    x = cp[:, 0]
                    y = cp[:, 1]
                    new_shape = Polygon([(i[0], i[1]) for i in zip(x, y)])
                    if ncp == 0:
                        poly = new_shape
                    else:
                        # Remove holes, if any
                        poly = poly.difference(new_shape)

                # Append polygon to list
                paths.append(poly)
            # Create a MultiPolygon for the contour
            multi = MultiPolygon(paths)
            # Append MultiPolygon and level as tuple to list
            level_polygons.append((levels[i], multi))
            i += 1

            # Create DataFrame
            df = pd.DataFrame(level_polygons, columns=['level', 'geometry'])
            df['level'] = df.apply(lambda row: np.round((1 - row.level) * 100, 2), axis=1)
            # Convert to a GeoDataFrame
            geo = gpd.GeoDataFrame(df, geometry='geometry', crs=gdf.crs)
            #m = geo.explore(tiles="cartodbpositron", width=1000, height=800)
            m = folium.Map(location=[geo['geometry'][0].centroid.y, geo['geometry'][0].centroid.x], zoom_start=1000, tiles='CartoDB positron', width=1000, height=800)
            for _, r in geo.iterrows():
                # Without simplifying the representation of each borough,
                # the map might not be displayed
                sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
                geo_j = sim_geo.to_json()
                geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'blue'})
                folium.Tooltip(r['level']).add_to(geo_j)
                geo_j.add_to(m)
                
            folium_static(m)
