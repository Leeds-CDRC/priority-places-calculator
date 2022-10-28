import pandas as pd
import geopandas as gpd
import shapely
from geovoronoi import voronoi_regions_from_coords
from shapely.ops import polygonize

def calculate_bipartite_nearest_distance(pntsA, pntsB, outlinePolygon):
    '''
    This function takes in two GeoDataFrames or GeoSeries (pntsA and pntsB) whose geometries are both defined by a series of points.
    
    For every point in pntsA, this function calculates the smallest distance to a point in pntsB. 
    
    An outlinePolygon is also required that contains the study area of interest.
    
    This function will run quickest (I think) when pntsA is the larger of the two GeoDataFrames.
    
    Parameters
    ----------
    pntsA : GeoDataFrame or GeoSeries with geometries consisting Points projected in EPSG:4326
    pntsB : GeoDataFrame or GeoSeries with geometries consisting Points projected in EPSG:4326
    outlinePolygon : A shapely geometry MultiPolygon object containing the study area of interest (e.g. a bounding box)
    
    Returns
    -------
    GeoSeries with the same index as pntsA containing the distance of each point to the nearest point in pntsB.
    '''
    
    # Validate parameters 
    if type(pntsA) not in [gpd.GeoDataFrame, gpd.GeoSeries]:
        raise TypeError("First argument must be a GeoDataFrame or GeoSeries")
    if type(pntsB) not in [gpd.GeoDataFrame, gpd.GeoSeries]:
        raise TypeError("Second argument must be a GeoDataFrame or GeoSeries")
    if list(pntsA.geometry.type.unique()) != ['Point']:
        raise TypeError("First argument must have a geometry that is all Points")
    if list(pntsB.geometry.type.unique()) != ['Point']:
        raise TypeError("Second argument must have a geometry that is all Points")
    if type(outlinePolygon) != shapely.geometry.polygon.Polygon:
        raise TypeError("Third argument must be a shapely geometry Polygon object")
    
    # Calculate the voronoi partition of pntsB
    voronoi_polys, voronoi_pts = voronoi_regions_from_coords(pntsB.geometry, outlinePolygon)

    # Turn the voronoi output into a GeoDataFrame with geometry given by the voronoi polygons
    voronoi_polys = gpd.GeoDataFrame(index=voronoi_polys.keys(), geometry=list(voronoi_polys.values()), crs='EPSG:4326')
    
    # Perform spatial join on the voronoi polygons with pntsA. 
    # The inner join will exclude any points in pntsA that are contained in the outlinePolygon.
    joined = gpd.sjoin(pntsA, voronoi_polys, how='inner', predicate='within')
    
    # Map the joined index to the corresponding point in pntsB
    joined['closest_point'] = joined['index_right'].apply(lambda x: pntsB.index[voronoi_pts[x][0]])
    
    # Merge back with pntsB. Resulting geodataframe contains the Point of each point in pntsA with the closest Point in pntsB.
    joined_wgeom = pd.merge(joined, pntsB, left_on='closest_point', right_index=True)
    
    # Convert to a non-geographic CRS (BNG in this case), set the geometry accordingly, then compute distance.
    df_pntsA = gpd.GeoDataFrame(joined_wgeom, geometry=joined_wgeom['geometry_x']).to_crs('EPSG:27700')
    df_pntsB = gpd.GeoDataFrame(joined_wgeom, geometry=joined_wgeom['geometry_y']).to_crs('EPSG:27700')
    
    return df_pntsA.distance(df_pntsB)


def count_bipartite_within_tolerance(pntsA, pntsB, tolerance):
    
    '''
    This function takes in two GeoDataFrames or GeoSeries (pntsA and pntsB) whose geometries are both defined by a series of points.
    
    For every point in pntsA, this function calculates the number of points in pntsB that are within a distance set by the tolerance value.
    
    Parameters
    ----------
    pntsA : GeoDataFrame with geometries consisting Points projected in EPSG:4326
    pntsB : GeoDataFrame with geometries consisting Points projected in EPSG:4326
    tolerance : int giving the distance over which to perform the count.
    
    Returns
    -------
    GeoSeries with the same index as pntsA containing the distance of each point to the nearest point in pntsB.
    '''
    
    pntsB = pntsB.to_crs('EPSG:27700')
    
    # Buffer around pntsB points
    buffered_pntsB = gpd.GeoDataFrame(index=pntsB.index, geometry=pntsB.buffer(tolerance), crs=27700)
    
    # create polygon array
    exterior_geom = list(polygonize(buffered_pntsB.exterior.unary_union))
    # create gdf out of the dissolved features
    pntsB_overlaps = gpd.GeoDataFrame({'id':range(0, len(exterior_geom))}, geometry=exterior_geom, crs=buffered_pntsB.crs).explode().reset_index(drop=True)
    pntsB_overlaps['id'] = pntsB_overlaps.index
    
    pntsB_overlaps['overlap_count'] = pntsB_overlaps.overlay(buffered_pntsB).groupby('id').count()
    pntsB_overlaps = pntsB_overlaps.to_crs('EPSG:4326')

    pntsB_overlaps_pntsA_joined = pntsA.sjoin(pntsB_overlaps, how='left', predicate='intersects')
    pntsB_overlaps_pntsA_joined['overlap_count'] = pntsB_overlaps_pntsA_joined['overlap_count'].fillna(0)
    
    return pntsB_overlaps_pntsA_joined['overlap_count']