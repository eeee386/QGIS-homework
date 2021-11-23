project = QgsProject.instance()


v_telep = project.mapLayersByName('JNK-settlements')[0]
features_telep = v_telep.getFeatures()

context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(v_telep))

v_telep.startEditing()
v_telep.addAttribute(QgsField('KUT_SZAM', QVariant.Int, 'int', 2))
#pr = v_telep.dataProvider()
#pr.addAttributes([QgsField('KUT_SZAM', QVariant.Int)])
v_telep.updateFields()
v_telep.commitChanges()
iface.vectorLayerTools().stopEditing(v_telep)


v_fuel = project.mapLayersByName('fuel')[0]
features_fuel = v_fuel.getFeatures()

 
with edit(v_telep):
    for t in v_telep.getFeatures():
        counter = 0
        context.setFeature(t)
        t_geom = t.geometry()
        for f in features_fuel:
            f_geom = f.geometry()
            if t_geom.contains(f_geom):
                counter += 1
        t['KUT_SZAM']=counter
        v_telep.updateFeature(t)
        