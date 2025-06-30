import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

# App setup
app = Dash(__name__)
fs = 1000
T = 1.0
t = np.linspace(0.0, T, int(fs*T), endpoint=False)

# App layout
app.layout = html.Div([
    html.H2("Interactive Fourier Transform"),
    html.Div([
        html.Label("Frequency 1 (Hz):"),
        dcc.Slider(id="freq1", min=1, max=200, step=1, value=50,
                   marks={i: str(i) for i in range(0, 201, 50)}),
        html.Label("Frequency 2 (Hz):"),
        dcc.Slider(id="freq2", min=1, max=200, step=1, value=120,
                   marks={i: str(i) for i in range(0, 201, 50)}),
    ], style={'width': '80%', 'padding': '20px'}),

    dcc.Graph(id="time-domain"),
    dcc.Graph(id="freq-domain")
])

# Callback
@app.callback(
    Output("time-domain", "figure"),
    Output("freq-domain", "figure"),
    Input("freq1", "value"),
    Input("freq2", "value")
)
def update_graph(freq1, freq2):
    # Signal and FFT
    signal = np.sin(2 * np.pi * freq1 * t) + 0.5 * np.sin(2 * np.pi * freq2 * t)
    fft_vals = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(t), 1/fs)
    magnitude = 2.0 / len(t) * np.abs(fft_vals[:len(t)//2])
    freqs_half = freqs[:len(t)//2]

    # Time domain
    time_fig = go.Figure()
    time_fig.add_trace(go.Scatter(x=t, y=signal, mode='lines'))
    time_fig.update_layout(title="Time Domain Signal", xaxis_title="Time (s)", yaxis_title="Amplitude")

    # Frequency domain
    freq_fig = go.Figure()
    freq_fig.add_trace(go.Scatter(x=freqs_half, y=magnitude, mode='lines'))
    freq_fig.update_layout(title="Frequency Domain (FFT)", xaxis_title="Frequency (Hz)", yaxis_title="Magnitude")

    return time_fig, freq_fig

if __name__ == "__main__":
    app.run_server(debug=True)
