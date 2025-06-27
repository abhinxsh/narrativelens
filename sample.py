import plotly.graph_objects as go

def bias_gauge(bias_label):
    mapping = {
        "left": -1,
        "center": 0,
        "right": 1
    }
    value = mapping.get(bias_label.lower(), 0)

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        gauge = {
            'axis': {'range': [-1,1]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [-1, -0.33], 'color': "red"},
                {'range': [-0.33,0.33], 'color': "lightgray"},
                {'range': [0.33,1], 'color': "blue"}
            ],
        },
        title = {'text': "Political Bias (-1=Left, +1=Right)"}
    ))
    return fig

def emotion_bar(emotion_str):
    emotions = [e.strip() for e in emotion_str.split(",")]
    counts = {e:1 for e in emotions}

    fig = go.Figure([go.Bar(
        x=list(counts.keys()),
        y=list(counts.values()),
        marker_color='indianred'
    )])
    fig.update_layout(title="Detected Emotions")
    return fig
