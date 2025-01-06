import matplotlib.pyplot as plt
import mplfinance as fin
import matplotlib.dates as mdates
from sqlite3 import connect
from pandas import read_sql_query
from geopandas import GeoDataFrame


def citireTabelaDb(nume_db, nume_tabela, coloana_index=None):
    con = connect(nume_db)
    t = read_sql_query("select * from " + nume_tabela, con, index_col=coloana_index)
    con.close()
    return t


def candle(x, titlu="Candle", volume=False):
    if volume:
        fin.plot(x, type="candle", volume=True, mav=(3, 6, 9))
    else:
        f = plt.figure(figsize=(10, 7))
        ax = f.add_subplot(1, 1, 1)
        assert isinstance(ax, plt.Axes)
        ax.set_title(titlu, fontsize=16, color='b')
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d:%m:$Y"))
        ax.tick_params(axis='x', rotation=30)
        fin.plot(x, type="candle", ax=ax, mav=(3, 6, 9))
    plt.show()

def plot_gpd(t, coloana=None, legenda=False, rampa_culori=None, titlu=None):
    f = plt.figure(figsize=(11, 9))
    ax = f.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    ax.set_title(titlu, fontsize=16, color='b')
    assert isinstance(t, GeoDataFrame)
    t.plot(column=coloana, legend=legenda, cmap=rampa_culori, ax=ax)
    plt.show()
