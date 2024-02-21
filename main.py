import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Checkbutton, IntVar

import mplcursors


# Mapping of SRT metrics to their descriptions
metric_comments = {
    'pktFlowWindow': 'The maximum number of unacknowledged packets that can be in flight.',
    'pktCongestionWindow': 'The number of packets that can be sent without being acknowledged under congestion control.',
    'pktFlightSize': 'The number of packets currently in flight.',
    'msRTT': 'The round-trip time in milliseconds, measuring the time to go to the destination and back.',
    'mbpsBandwidth': 'The estimated bandwidth of the connection in megabits per second.',
    'mbpsMaxBW': 'The maximum bandwidth that the connection can use in megabits per second.',
    'pktSent': 'Total number of packets that have been sent.',
    'pktSndLoss': 'The number of packets that were detected as lost by the sender.',
    'pktSndDrop': 'The number of packets that were dropped by the sender due to reasons like buffer overflow.',
    'pktRetrans': 'The number of retransmitted packets.',
    'byteSent': 'Total number of bytes that have been sent.',
    'byteSndDrop': 'The number of bytes that were dropped by the sender.',
    'mbpsSendRate': 'The rate at which the sender is sending data in megabits per second.',
    'usPktSndPeriod': 'The time interval between sending individual packets in microseconds.',
    'pktRecv': 'Total number of packets that have been received.',
    'pktRcvLoss': 'The number of packets that were detected as lost by the receiver.',
    'pktRcvDrop': 'The number of packets that were dropped by the receiver.',
    'pktRcvRetrans': 'The number of retransmitted packets received.',
    'pktRcvBelated': 'The number of packets that arrived later than expected.',
    'byteRecv': 'Total number of bytes that have been received.',
    'byteRcvLoss': 'The number of bytes that were detected as lost by the receiver.',
    'byteRcvDrop': 'The number of bytes that were dropped by the receiver.',
    'mbpsRecvRate': 'The rate at which the receiver is receiving data in megabits per second.',
    'RCVLATENCYms': 'The latency in milliseconds on the receiving side.',
    'pktSndFilterExtra': 'Extra packets sent based on the filter configuration.',
    'pktRcvFilterExtra': 'Extra packets received based on the filter configuration.',
    'pktRcvFilterSupply': 'The number of supplied packets from the receiver filter.',
    'pktRcvFilterLoss': 'The number of lost packets according to the receiver filter.'
}

def load_log_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select log file", filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")])
    if not file_path:
        messagebox.showinfo("Info", "No file selected. Exiting application.")
        exit()
    return file_path


def plot_selected_metrics(df, selected_metrics):
    if not selected_metrics:
        messagebox.showinfo("Info", "No metrics selected. Exiting application.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    lines = []  # Store the line objects to link them with mplcursors
    for metric in selected_metrics:
        if metric in df.columns:
            # Plot the metric data
            line, = ax.plot(pd.to_datetime(df['Stamp']), df[metric], label=metric)
            lines.append(line)
        else:
            messagebox.showinfo("Error", f"Metric '{metric}' not found in the DataFrame.")
            return

    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('IPTV Channel Metrics Over Time')
    plt.xticks(rotation=45)
    legend = plt.legend()
    plt.tight_layout()

    # mplcursors will add tooltips to the lines
    cursor = mplcursors.cursor(lines, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(metric_comments[sel.artist.get_label()]))

    plt.show()


def select_metrics_gui(df):
    root = Toplevel()
    root.title("Select Metrics to Plot")
    variables = []

    for metric in df.columns:
        var = IntVar()
        # Display metric with its comment if available
        text = f"{metric}: {metric_comments.get(metric, 'No description available')}"
        Checkbutton(root, text=text, variable=var, wraplength=400, justify=tk.LEFT).pack(anchor="w", expand=True)
        variables.append((metric, var))

    def on_confirm():
        selected_metrics = [metric for metric, var in variables if var.get() == 1]
        root.destroy()
        plot_selected_metrics(df, selected_metrics)

    confirm_button = tk.Button(root, text="Confirm", command=on_confirm)
    confirm_button.pack(side="bottom")
    root.mainloop()

def main():
    file_path = load_log_file()
    df = pd.read_csv(file_path)

    # Assume 'Stamp' is the timestamp column
    df['Stamp'] = pd.to_datetime(df['Stamp'])

    select_metrics_gui(df)

if __name__ == "__main__":
    main()
