import shapely.geometry as geom
import geopandas as gpd
import matplotlib.pyplot as plt
from functii import plot_gpd

punct = geom.Point(0, 0)
linie = geom.LineString(((10, 10), (10, 20), (20, 20)))
triunghi = geom.Polygon([(10, 10), (20, 10), (30, 15)])
patrat = geom.Polygon([(10, 10), (20, 10), (20, 20), (10, 20)])

print("Arii:", triunghi.area, patrat.area, sep="\n")
serie1 = gpd.GeoSeries([triunghi, patrat])
serie2 = gpd.GeoSeries([punct, linie])

print("\nSeria 1", serie1)
print("\nSuprafete seria 1:", serie1.area, sep="\n")
print("\nIncadrare seria 1:", serie1.bounds, serie1.total_bounds, sep="\n")
print("\nDistanta serie 1 fata de punctul (0,0)",
      serie1.distance(punct), sep="\n")
print("\nDistanta dintre serii:", serie1.distance(serie2), sep="\n")

ax1 = serie1.plot()
ax1.set_title("Seria 1")
ax2 = serie2.plot()
ax2.set_title("Seria 2")
exista_intersectie = serie1.intersects(serie2)
print("\nExistenta intersectii:", exista_intersectie, sep="\n")
intersectii = serie1.intersection(serie2)
ax3 = intersectii.plot()
ax3.set_title("Intersectii")
intersectie_patrat_triunghi = patrat.intersection(triunghi)
ax4 = gpd.GeoSeries(intersectie_patrat_triunghi).plot()
ax4.set_title("Intersectie patrat-triunghi")

plt.show()

world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
print(world.head())
print(list(world))
plot_gpd(world, rampa_culori="RdYlBu", titlu="Harta lumii")
plot_gpd(world, coloana="continent", rampa_culori="RdYlBu",
         titlu="Harta lumii pe continente", legenda=True)
plot_gpd(world, coloana="gdp_md_est", rampa_culori="Reds",
         titlu="Harta lumii dupa GDP",legenda=True)
