project = QgsProject.instance()


v_telep = project.mapLayersByName('JNK-settlements')[0]
features_telep = v_telep.getFeatures()

v_fuel = project.mapLayersByName('amenity_fuel_JNK')[0]
features_fuel = v_fuel.getFeatures()
 
for f in features_fuel:
    f_geom = f.geometry()
    for t in features_telep:
        t_geom = t.geometry()
        print(t_geom.contains(f_geom))
        if t_geom.contains(f_geom):
            print(t)
    