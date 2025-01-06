import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
import pandas.api.types as pdt
from geopandas import GeoDataFrame
import numpy as np
from statsmodels.graphics.mosaicplot import mosaic
import mplfinance as fin
import matplotlib.dates as mdates


def scatterplot_sb(t, var1, var2, by1=None, by2=None, titlu="Scatterplot"):
    fig = plt.figure(figsize=(13, 8))
    assert isinstance(fig, plt.Figure)
    ax = fig.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    ax.set_title(titlu, fontdict={"fontsize": 16, "color": "b"})
    ax.set_xlabel(var1, fontdict={"fontsize": 12, "color": "b"})
    ax.set_ylabel(var2, fontdict={"fontsize": 12, "color": "b"})
    sb.scatterplot(x=var1, y=var2, hue=by1, style=by2, data=t, ax=ax, s=100)
    for i in range(len(t)):
        ax.text(t[var1].iloc[i], t[var2].iloc[i], t.index[i])
    plt.show()


def heatmap(t, vmin, vmax, titlu="Heatmap"):
    fig = plt.figure(figsize=(9, 8))
    assert isinstance(fig, plt.Figure)
    ax = fig.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    ax.set_title(titlu, fontsize=16, color='b')
    ax_ = sb.heatmap(t, vmin=vmin, vmax=vmax, cmap="RdYlBu", annot=True, ax=ax)
    ax_.set_xticklabels(t.index, rotation=30, ha="right")
    plt.show()


def histograma(t, vars, titlu="Grafic histograma"):
    for v in vars:
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(1, 1, 1)
        assert isinstance(ax, plt.Axes)
        ax.set_title(titlu, fontdict={"fontsize": 16, "color": 'b'})
        ax.set_xlabel(v, fontsize=14)
        ax.set_ylabel("Frecventa", fontsize=12)
        ax.hist(t[v], color='g', rwidth=0.9)
    plt.show()


def histograma2(t, vars, titlu="Histograme"):
    fig = plt.figure(figsize=(14, 8))
    assert isinstance(fig, plt.Figure)
    fig.suptitle(titlu, fontsize=18, color='b')
    q = len(vars)
    axe = fig.subplots(1, q, sharey=True)
    for i in range(q):
        axa = axe[i]
        assert isinstance(axa, plt.Axes)
        axa.set_xlabel(vars[i])
        x = t[vars[i]].values
        axa.hist(x, rwidth=0.9)
    plt.show()


def distributie(t, vars, titlu="Distributie de probabilitate", eticheta_x=""):
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(titlu, fontsize=16, color='b')
    for v in vars:
        sb.kdeplot(t[v], shade=True, ax=ax, label=v)
    ax.set_xlabel(eticheta_x, fontsize=12, color='b')
    ax.legend()
    plt.show()


def distributie2D(t, var1, var2, titlu="Distributie de probabilitate 2D"):
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(titlu, fontsize=16, color='b')
    sb.kdeplot(x=t[var1], y=t[var2], shade=True, ax=ax)
    plt.show()


def boxplot(t, vars, titlu="Grafic box"):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    ax.set_title(titlu, fontdict={"fontsize": 16, "color": 'b'})
    ax.boxplot(t[vars].values, labels=vars, showmeans=True, meanline=True)
    plt.show()


def boxplot_sb(t, vars, titlu="Grafic boxplot", by1=None, by2=None):
    fig = plt.figure("hhh", figsize=(10, 7))
    ax = fig.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    if by1 is None:
        sb.boxplot(data=t[vars], ax=ax)
    else:
        if by2 is None:
            titlu = titlu + ". Grupare dupa " + by1
        else:
            titlu = titlu + ". Grupare dupa " + by1 + " si " + by2
        sb.boxplot(x=vars[0], y=by1, hue=by2, data=t, ax=ax)
    ax.set_title(titlu, fontdict={"fontsize": 16, "color": 'b'})
    plt.show()

def catplot(t, var, by1=None, by2=None, titlu="Grafice de imprastiere"):
    fig = plt.figure(figsize=(10, 7))
    assert isinstance(fig, plt.Figure)
    fig.suptitle(titlu)
    ax = fig.add_subplot(1, 1, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    assert isinstance(ax, plt.Axes)
    sb.stripplot(x=var, y=by1, hue=by2, data=t, size=10, ax=ax)
    sb.violinplot(x=var, y=by1, hue=by2, data=t, size=10, ax=ax2)
    plt.show()



def pie(t, var, by=None, titlu="Diagrama de structura"):
    assert isinstance(t, pd.DataFrame)
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    ax.set_title(titlu, fontdict={"fontsize": 16, "color": 'b'})
    if by is None:
        ax.pie(t[var], labels=t.index)
        ax.set_xlabel(var)
    else:
        tg = t[[var, by]].groupby(by=by).agg(np.mean)
        ax.pie(tg[var], labels=tg.index)
        ax.set_xlabel(var + ": Grupare dupa " + by)
    plt.show()


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



def count_chart(t, var, nbins=5, by=None, titlu="Grafic de frecvente"):
    fig = plt.figure(figsize=(14, 8))
    assert isinstance(fig, plt.Figure)
    ax = fig.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    ax.set_title(titlu, fontdict={"fontsize": 16, "color": "b"})

    if pd.api.types.is_numeric_dtype(t[var]):
        # Transformare de variabila
        etichete = [var + str(i) for i in range(1, nbins + 1)]
        v = pd.cut(t[var], bins=nbins, include_lowest=True,
                   labels=etichete)
        sb.countplot(x=v, ax=ax, hue=by, data=t)
    else:
        sb.countplot(x=t[var], ax=ax)
    plt.show()


def codificare(x, bins, valori, nume=None):
    v = np.histogram_bin_edges(x, bins)
    assert isinstance(v, np.ndarray)
    if valori:
        if nume is None:
            etichete = [format(v[i], "5.2f") + ":" + format(v[i + 1], "5.2f") for i in range(bins)]
        else:
            etichete = [nume + "_" + format(v[i], "5.2f") + ":" + format(v[i + 1], "5.2f") for i in range(bins)]
    else:
        if nume is None:
            nume = ""
        etichete = [nume + "_" + str(i) for i in range(1, bins + 1)]
    y = pd.cut(x, v, include_lowest=True, labels=etichete)
    return list(y.values)


def mozaic(t, varx, vary, bins=5, valori=False):
    fig = plt.figure(figsize=(10, 7))
    assert isinstance(fig, plt.Figure)
    ax = fig.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    t_nou = pd.DataFrame()
    if pdt.is_numeric_dtype(t[varx]):
        t_nou[varx] = codificare(t[varx], bins, valori, varx)
    else:
        t_nou[varx] = t[varx]
    if pdt.is_numeric_dtype(t[vary]):
        t_nou[vary] = codificare(t[vary], bins, valori, vary)
    else:
        t_nou[vary] = list(t[vary])
    mosaic(t_nou, [varx, vary], ax=ax, gap=0.01, label_rotation=45)
    plt.show()


def plot_gpd(t, coloana=None, legenda=False, rampa_culori=None, titlu=None):
    f = plt.figure(figsize=(11, 9))
    ax = f.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    ax.set_title(titlu, fontsize=16, color='b')
    assert isinstance(t, GeoDataFrame)
    t.plot(column=coloana, legend=legenda, cmap=rampa_culori, ax=ax)
    plt.show()
