import asyncio
import sys
import time
import csv
import os
from datetime import datetime
from pytest_dt_mt.client import DittoClient
from ut_helpers import UT_TENANT

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Globale Datenspeicher, um sie sicher nach dem Beenden abzurufen
history = {}
csv_rows = []
start_time = None

async def monitor_things(thing_ids):
    global start_time
    dt = DittoClient(http_url="http://127.0.0.1:8083")
    
    print("====================================================")
    print("Digital Twin: Live Sensor Monitor (with CSV & Plot)")
    print(f"Monitoring: {len(thing_ids)} things")
    print("Press Ctrl+C to stop and generate plot")
    print("====================================================\n")

    start_time = time.time()
    
    try:
        while True:
            current_time_str = time.strftime("%H:%M:%S")
            elapsed = time.time() - start_time
            print(f"--- Snapshot at {current_time_str} ---")
            
            for t_id in thing_ids:
                clean_id = t_id.split(":")[-1] if ":" in t_id else t_id
                
                try:
                    state = await dt.fetch_state(clean_id)
                    
                    if 'features' in state:
                        for feat_name, feat_data in state['features'].items():
                            val = feat_data.get('properties', {}).get('value', 'N/A')
                            print(f"  > {clean_id} [{feat_name}]: {val}")
                            
                            # In Liste zwischenspeichern
                            csv_rows.append([current_time_str, clean_id, feat_name, val])
                            
                            # Numerische Werte für den Plot zwischenspeichern
                            try:
                                float_val = float(val)
                                key = f"{clean_id} [{feat_name}]"
                                if key not in history:
                                    history[key] = ([], [])
                                history[key][0].append(elapsed)
                                history[key][1].append(float_val)
                            except (ValueError, TypeError):
                                pass
                            
                    else:
                        print(f"  ? {clean_id}: No features found or device offline")
                
                except Exception as e:
                    print(f"  ! {clean_id}: Error fetching state ({e})")
            
            print("")
            await asyncio.sleep(1.0)
            
    finally:
        try:
            await dt.close()
        except BaseException:
            pass

def save_data_and_plot():
    """Wird ganz am Ende nach dem Event-Loop sicher aufgerufen."""
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. CSV Speichern
    if csv_rows:
        csv_filename = f"monitor_data_{timestamp_str}.csv"
        csv_path = os.path.abspath(csv_filename)
        try:
            with open(csv_path, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['timestamp', 'thing_id', 'feature_name', 'value'])
                writer.writerows(csv_rows)
            print(f"\n[ERFOLG] CSV gespeichert unter:\n -> {csv_path}")
        except Exception as e:
            print(f"\n[FEHLER] Konnte CSV nicht speichern: {e}")
    else:
        print("\n[INFO] Keine Daten empfangen, daher keine CSV erstellt.")

    # 2. Plot Generieren
    if MATPLOTLIB_AVAILABLE and history:
        try:
            # Trenne in binäre (light/switch) und andere (kontinuierliche) Sensoren
            binary_keys = [k for k in history.keys() if "light." in k.lower() or "switch." in k.lower()]
            continuous_keys = [k for k in history.keys() if k not in binary_keys]
            
            fig, ax1 = plt.subplots(figsize=(12, 6))
            lines = []
            labels = []
            
            # Plot kontinuierliche Daten auf der primären Y-Achse
            for key in continuous_keys:
                x, y = history[key]
                l, = ax1.plot(x, y, label=key)
                lines.append(l)
                labels.append(key)
            
            ax1.set_xlabel("Time (seconds)")
            ax1.set_ylabel("Continuous Values")
            ax1.grid(True)
            
            # Plot binäre Daten (0/1) auf einer sekundären Y-Achse
            if binary_keys:
                ax2 = ax1.twinx()
                for key in binary_keys:
                    x, y = history[key]
                    # Gestrichelte Linie für binäre Daten zur besseren Unterscheidung
                    l, = ax2.plot(x, y, linestyle='--', marker='o', markersize=4, label=key)
                    lines.append(l)
                    labels.append(key)
                
                ax2.set_ylabel("Binary State (0 / 1)")
                ax2.set_ylim(-0.1, 1.1)
                ax2.set_yticks([0, 1])
            
            # Gemeinsame Legende
            ax1.legend(lines, labels, loc='upper left', bbox_to_anchor=(1.05, 1))
            plt.title("Live Sensor Monitor Data")
            plt.tight_layout() # Verhindert, dass die Legende abgeschnitten wird
            
            plot_filename = f"monitor_plot_{timestamp_str}.png"
            plot_path = os.path.abspath(plot_filename)
            plt.savefig(plot_path)
            print(f"[ERFOLG] Plot gespeichert unter:\n -> {plot_path}")
        except Exception as e:
            print(f"[FEHLER] Konnte Plot nicht generieren: {e}")
    elif not MATPLOTLIB_AVAILABLE:
        print("[WARNUNG] matplotlib nicht installiert. Plot übersprungen. (pip install matplotlib)")
    else:
        print("[INFO] Keine numerischen Daten zum Plotten vorhanden.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mt_live_monitor_plot.py <thingId1> <thingId2> ...")
        sys.exit(1)
        
    ids_to_monitor = sys.argv[1:]
    
    try:
        asyncio.run(monitor_things(ids_to_monitor))
    except KeyboardInterrupt:
        # Hier landet das Skript sicher, wenn man Ctrl+C drückt!
        pass
    except Exception as e:
        print(f"\n[FEHLER] Unerwarteter Absturz: {e}")
    finally:
        # Wird garantiert IMMER am Ende aufgerufen.
        save_data_and_plot()
