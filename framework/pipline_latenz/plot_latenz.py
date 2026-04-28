import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# 1. Alle CSV-Dateien laden
files = sorted(glob.glob('sensor_data_*.csv'))
if not files:
    print("Keine Dateien gefunden!")
    exit()

current_idx = 0


def plot_file(idx):
    plt.clf()  # Den alten Plot löschen
    file = files[idx]
    df = pd.read_csv(file)

    # Alle Sensoren in der Datei plotten
    for sensor_name in df['sensor'].unique():
        subset = df[df['sensor'] == sensor_name]
        label = sensor_name.split('.')[-1]
        plt.step(subset['rel_time_ms'], subset['value'], where='post', label=label)

    plt.title(f"Datei ({idx + 1}/{len(files)}): {os.path.basename(file)}\n"
              f"(Nutze Pfeiltasten ← → zum Blättern)", fontsize=12, fontweight='bold')
    plt.xlabel('Relative Zeit (ms)')
    plt.ylabel('Sensorwert')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='best')
    plt.draw()


def on_key(event):
    global current_idx
    if event.key == 'right':
        current_idx = (current_idx + 1) % len(files)
        plot_file(current_idx)
    elif event.key == 'left':
        current_idx = (current_idx - 1) % len(files)
        plot_file(current_idx)


# Figure aufsetzen
fig = plt.figure(figsize=(10, 6))
fig.canvas.mpl_connect('key_press_event', on_key)

# Ersten Plot anzeigen
plot_file(current_idx)

print(f"Interaktiver Modus gestartet.")
print(f"Klicke in das Plot-Fenster und nutze die Pfeiltasten (Links/Rechts) zum Blättern.")
plt.show()