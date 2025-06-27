import plotly.graph_objects as go

def bias_gauge(bias_label: str) -> go.Figure:
    """Render a stylized gauge to visualize political bias positioning."""
    
    mapping = {
        "left": -1,
        "center": 0,
        "right": 1
    }
    value = mapping.get(bias_label.lower(), 0)

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        delta={
            'reference': 0,
            'increasing': {'color': "#4C6FFF"},
            'decreasing': {'color': "#FF4C4C"}
        },
        title={
            'text': f"<b>Bias Position:</b> {bias_label.capitalize()}",
            'font': {'size': 20}
        },
        gauge={
            'axis': {
                'range': [-1, 1],
                'tickvals': [-1, -0.5, 0, 0.5, 1],
                'ticktext': ['Far Left', 'Left', 'Center', 'Right', 'Far Right'],
                'tickfont': {'color': "#FAFAFA"}
            },
            'bar': {'color': "#00F5A0"},
            'steps': [
                {'range': [-1, -0.33], 'color': "#FF4C4C"},
                {'range': [-0.33, 0.33], 'color': "#CCCCCC"},
                {'range': [0.33, 1], 'color': "#4C6FFF"}
            ],
            'threshold': {
                'line': {'color': "#FAFAFA", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor="#0A0A0A",
        font={'color': "#FAFAFA", 'family': "sans-serif"},
        margin=dict(t=40, b=20)
    )

    return fig


def emotion_bar(emotion_str: str) -> go.Figure:
    """Render a bar chart to visualize detected emotional tones with punch and clarity."""
    
    import random

    # Process input emotions
    emotions = [e.strip().capitalize() for e in emotion_str.split(",") if e.strip()]
    if not emotions:
        emotions = ["Neutral"]
    
    unique_emotions = list(dict.fromkeys(emotions))  # maintain order
    counts = {e: emotions.count(e) for e in unique_emotions}

    # Generate visually distinct colors for each bar (optional: make consistent for known emotions)
    color_palette = {
        "Joy": "#FFD93D",
        "Anger": "#FF6B6B",
        "Sadness": "#6A5ACD",
        "Fear": "#964B00",
        "Surprise": "#4D96FF",
        "Disgust": "#6BCB77",
        "Neutral": "#999999"
    }
    default_colors = ['#FF6B6B', '#FFD93D', '#6BCB77', '#4D96FF', '#E96479', '#A084E8']
    bar_colors = [color_palette.get(e, random.choice(default_colors)) for e in unique_emotions]

    # Create figure
    fig = go.Figure(go.Bar(
        x=list(counts.keys()),
        y=list(counts.values()),
        marker=dict(color=bar_colors, line=dict(color="#FAFAFA", width=1.2)),
        text=[f"{v}×" for v in counts.values()],
        textposition="outside",
        hoverinfo="x+y"
    ))

    # Layout updates
    fig.update_layout(
        title={
            'text': "<b>Emotion Footprint</b>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24}
        },
        xaxis=dict(
            title="Detected Emotions",
            
            showgrid=False
        ),
        yaxis=dict(
            title="Frequency",
            showgrid=True,
            gridcolor="#333"
        ),
        plot_bgcolor="#121212",
        paper_bgcolor="#0A0A0A",
        font=dict(color="#FAFAFA", family="sans-serif"),
        margin=dict(t=60, b=60),
        bargap=0.35
    )

    return fig
