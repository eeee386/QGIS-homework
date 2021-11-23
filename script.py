project = QgsProject.instance()

context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(v))

v_telep = project.mapLayersByName('JNK-settlements')[0]
features_telep = v_telep.getFeatures()

v_telep.startEditing()
v_telep.addAttribute(QgsField('KUTAK_SZAMA', QVariant.Int, 'int', 2))
v_telep.updateFields()
v_telep.commitChanges()
iface.vectorLayerTools().stopEditing(v_telep)


v_fuel = project.mapLayersByName('fuel_JNK')[0]
features_fuel = v_fuel.getFeatures()


 
with edit(v_telep):
    for t in features_telep:
        counter = 0
        context.setFeature(t)
        t_geom = t.geometry()
        for f in features_fuel:
            f_geom = f.geometry()
            if t_geom.contains(f_geom):
                counter += 1
        t['KUTAK_SZAMA']=counter
        v_telep.updateFeature(feature)