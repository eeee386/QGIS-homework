# Első része

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


v_fuel = project.mapLayersByName('fuel_JNK')[0]
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
        
# Második része
project = QgsProject.instance()

v = project.mapLayersByName("fuel_JNK")[0]

renderer = QgsRuleBasedRenderer(QgsMarkerSymbol())

# az eredő szabályt eltároljuk változóba
root_rule = renderer.rootRule()

# az eredő szabály gyerekét másoljuk, majd a másolat tulajdonságait módosítjuk
rule1 = root_rule.children()[0].clone()
rule1.setLabel("MOL")
rule1.setFilterExpression('brand = \'MOL\'')
props1 = v.renderer().symbol().symbolLayer(0).properties()
props1['color'] = 'green'
props1['size'] = '3'
rule1.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(props1)));
# az eredő szabáályhoz hozzáadjuk gyerekként az új szabályt
root_rule.appendChild(rule1)

rule2 = root_rule.children()[0].clone()
rule2.setLabel("OMV")
rule2.setFilterExpression('brand = \'OMV\'')
props2 = v.renderer().symbol().symbolLayer(0).properties()
props2['color'] = 'blue'
props2['size'] = '5'
rule2.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(props2)));
root_rule.appendChild(rule2)

rule3 = root_rule.children()[0].clone()
rule3.setLabel("Shell")
rule3.setFilterExpression('brand = \'Shell\'')
props3 = v.renderer().symbol().symbolLayer(0).properties()
props3['color'] = 'yellow'
props3['size'] = '7'
props3['name'] = 'diamond'
rule3.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(props3)));
root_rule.appendChild(rule3)

rule3 = root_rule.children()[0].clone()
rule3.setLabel("all")
rule3.setFilterExpression('')
props3 = v.renderer().symbol().symbolLayer(0).properties()
props3['color'] = 'white'
props3['size'] = '2'
props3['name'] = 'triangle'
rule3.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(props3)));
root_rule.appendChild(rule3)

# töröljük az eredő szabályt
root_rule.removeChildAt(0) 

v.setRenderer(renderer)
v.triggerRepaint()
