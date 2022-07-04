import pandas as pd
import numpy as np
from regex import P, X
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import cross_decomposition

def sort_legend(col, cols_to_be_sorted, data, other_values={}):
    if ((col in data.columns) and (col in cols_to_be_sorted)):
        indexed_names = enumerate((set(data[col])))
        sorted_names_indices = sorted((name,index) for index,name in indexed_names)
        alpha_order = [n for n,_ in sorted_names_indices]
        if col in other_values.keys():
            alpha_order.remove(other_values[col])
            alpha_order.append(other_values[col])
        legend_order=alpha_order
    else:
        legend_order = None
    return legend_order

def plot(data,
        x=None,
        y=None,
        hue=None,
        size=None,
        style=None,

        drop_doubles=None,
        drop_na=False,

        slice_top = False,
        split=False,
        yscale=None,

        title='',
        legend_position=None,
        xlabel='',
        ylabel='',
        huelabel='',
        sort_alpha=[],

        vlines='',
        figsize=(5,5),
        palette='tab10',
        
        type='dist',
        bins=25,
        
        save_path='',
        ):

    ## df preprocessing
    data = data.copy()

    if drop_na:
        for i in drop_na:
            data = data.dropna(subset=i)

    if drop_doubles:
        for i in drop_doubles:
            data = data.drop_duplicates(subset=i)


    if slice_top:
        for k,v in slice_top.items():
            top = pd.value_counts(data[k]).iloc[0:v].index
            data = data[data[k].isin(top)]

    if split:
        other_values = {}
        for k,v in split.items():
            other_slice = pd.value_counts(data[k]).iloc[v-1:].index
            other_value = 'other {0}'.format(['('+str(n)+')' if n>1 else '' for n in [len(other_slice)]][0])
            data.loc[data[k].isin(other_slice), k] = other_value
            other_values[k] = other_value
    else: 
        other_values = {}

    if sort_alpha:
        sorted_idxs = dict()
        for v in sort_alpha:
            sorted_idxs[v] = pd.value_counts(data[v]).index

    #data = data.sort_values([sorting_value]).reset_index(drop=True)

    ## fig 
    sns.set_style("darkgrid")

    if type == 'violin':
        split = len(set(data[hue]))==2
        hue_order = sort_legend(hue, sort_alpha, data, other_values)
        ax = sns.violinplot(data=data,
                    x=x,
                    y=y,
                    hue=hue,
                    legend=True,
                    split=split,
                    palette=palette,
                    cut=0,
                    )
    elif type == 'dist':
        hue_order = sort_legend(hue, sort_alpha, data, other_values)
        ax = sns.displot(data=data,
                    x=x,
                    y=y,
                    hue=hue,      
                    kind='kde',
                    legend=True,
                    palette=palette,
                    cut=0,
                    hue_order=hue_order,
                    )
    elif type == 'hist':
        hue_order = sort_legend(hue, sort_alpha, data, other_values)
        ax = sns.histplot(data=data,
                    x=x,
                    y=y,
                    hue=hue,
                    bins=bins,      
                    legend=True,
                    palette=palette,
                    hue_order=hue_order,
                    )
    elif type == 'scatter':
        hue_order = sort_legend(hue, sort_alpha, data, other_values)
        size_order = sort_legend(size, sort_alpha, data, other_values)
        style_order = sort_legend(style, sort_alpha, data, other_values)
        ax = sns.scatterplot(data=data,
                    x=x,
                    y=y,
                    hue=hue,
                    size=size,
                    style=style,
                    legend=True,
                    palette=palette,
                    hue_order=hue_order,
                    size_order=size_order,
                    style_order=style_order,
                    )
    elif type == 'count':
        ax = sns.countplot(data=data,
                    x=x,
                    palette=palette,
                    )
    elif type == 'perc':
        sns.set_style("white")
        if x:
            index = data[x]
        else:
            index = np.zeros(len(data))
                    
        cross_tab = pd.crosstab(
                            index=index,
                            columns=data[hue],
                            normalize='index',
                            )
        cross_tab = cross_tab.T
        cross_tab = cross_tab.sort_values(cross_tab.columns[0], ascending = False).T
        kind = 'bar'+ ('h' * (not bool(x)))
        ax = cross_tab.plot(
                        kind = kind, 
                        stacked = True, 
                        mark_right = True,
                        color=sns.color_palette(palette),
                        )
        ax.set(ylabel=None)
        if not x:
            ax.set(xlabel=None)
        

    sns.set(rc={'figure.figsize':figsize})

    if yscale:
        plt.yscale(yscale)

    if not ylabel:
        ylabel = y
    if not xlabel:
        xlabel = x
    if not huelabel:
        huelabel = hue

    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
     
    try:
        labels = [len(str(x)) for x in ax.get_xticklabels()]
        max_xtick_len = max(labels)
        if max_xtick_len > 5:
            plt.xticks(rotation = min(90, max_xtick_len*10))
    except AttributeError:
        for a in ax.axes.flat:
            labels = [len(str(x)) for x in a.get_xticklabels()]
            max_xtick_len = max(labels)
            break
        if max_xtick_len > 5:
            plt.xticks(rotation = min(90, max_xtick_len*10))
            
    try:
        if legend_position=='out':
            sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
        elif legend_position=='over':
            sns.move_legend(
                ax, "lower center",
                bbox_to_anchor=(.5, .25), ncol=3, title=None, frameon=False,
            )
        elif legend_position=='under':
            sns.move_legend(
                ax, "lower center",
                bbox_to_anchor=(.5, -.25), ncol=3, title=None, frameon=False,
            )
        else:
            sns.move_legend(ax, legend_position) # 'best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left', 'center right', 'lower center', 'upper center', 'center'
    except ValueError:
        pass
    if not title:
        if hue and x and not y:
            title = 'Distribution of ' + str(huelabel)+ (' by ' + str(xlabel))*bool(xlabel)
        elif hue:
            'Number of instances grouped by ' + str(huelabel)*bool(huelabel)
        else:
            title = str(xlabel)+ (' vs ' + str(ylabel))*bool(ylabel) + (' grouped by ' + str(huelabel))*bool(huelabel)

    if vlines:
        for vline in vlines:
            plt.axvline(**vline)
    plt.title(title)
    #plt.legend(title=huelabel)
    if save_path:
        plt.savefig(save_path)
    plt.show()
    