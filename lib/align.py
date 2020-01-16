import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def run(input_location, runs_location, output_location):
    # openem_df = pd.read_csv("~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/transect_aligner/lib/input.csv")
    openem_df = pd.read_csv(input_location)

    # runs_df = pd.read_csv("~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/transect_aligner/lib/runs1.csv")
    runs_df = pd.read_csv(runs_location)

    print(pd.concat([runs_df, runs_df], axis=0))

    print(list(openem_df))

    plt.plot(openem_df['Longitude'], openem_df['Latitude'])
    for i in range(len(openem_df['ID'])):
        if not i % 10:
            plt.annotate(openem_df['ID'][i], xy=(openem_df['Longitude']
                                                 [i], openem_df['Latitude'][i]), color='purple')
    # plt.show()
    grads = []

    # sys.exit("End of code")

    for j in range(len(runs_df['direction'])):
        print(runs_df['start'][j], runs_df['end'][j])
        transect_df = openem_df[openem_df['ID'] > runs_df['start'][j]]
        transect_df = transect_df[transect_df['ID'] < runs_df['end'][j]]
        z = np.polyfit(x=transect_df['Longitude'], y=transect_df['Latitude'], deg=1)
        plt.plot(transect_df['Longitude'], transect_df['Latitude'],
                 label='run: ' + str(j) + '\ny={0:.2f} x + {1:.2f}'.format(z[0], z[1]))
        grads.append(z[0])
    plt.legend()
    # plt.show()
    grad = np.mean(grads)

    out_df = None
    cleck = 0
    for j in range(len(runs_df['direction'])):
        print(j)
        transect_df = openem_df[openem_df['ID'] > runs_df['start'][j]]
        transect_df = transect_df[transect_df['ID'] < runs_df['end'][j]]
        max = transect_df['Longitude'].max()
        min = transect_df['Longitude'].min()
        y_mean = transect_df['Latitude'].mean()
        x_mean = transect_df['Longitude'].mean()
        b1 = y_mean - grad*x_mean
        xs = [min, max]
        ys = [grad*min + b1, grad*max+b1]
        # plt.plot(xs, ys, c='black')
        in_grad = -1/grad
        for i in range(len(transect_df['Longitude'])):
            b2 = transect_df['Latitude'].iloc[i] - in_grad*transect_df['Longitude'].iloc[i]
            new_x = (-b1+b2)/(grad-in_grad)
            new_y = grad*new_x + b1
            transect_df['Latitude'].iloc[i] = new_y
            transect_df['Longitude'].iloc[i] = new_x
        if cleck:
            out_df = pd.concat([out_df, transect_df], axis=0)
            print('Add')
        else:
            cleck = 1
            print('Create')
            out_df = transect_df
        plt.plot(transect_df['Longitude'], transect_df['Latitude'], label='run: ' + str(j))

    plt.legend()
    # plt.show()

    plt.plot(out_df['Longitude'], out_df['Latitude'])
    # plt.show()
    plt.plot(out_df['ID'], out_df['Hp'])
    # plt.show()
    out_df.to_csv(output_location, index=False)
    # out_df.to_csv('~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/transect_aligner/lib/output.csv', index=False)
