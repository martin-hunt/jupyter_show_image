import plotly.graph_objects as go
from PIL import Image

# Based on code from
# https://plot.ly/python/images/


def show_image(img, width=1024, height=None, toolbar=True):
    """ Displays zoomable image in Jupyter.  Aspect ratio is always
    preserved.
    
    img: Filename, PIL image or numpy array (from opencv?)
    width: Output width. Defaults to 1024
    height: Output height.  If specified, width is ignored.
    toolbar: Display Plotly modebar? Default True.
    """
    if type(img) is str:
        img = Image.open(img)
    if not hasattr(img, 'width'):
        img = Image.fromarray(img)
    img_width = img.width
    img_height = img.height 

    if height is not None:
        scale_factor = height / img_height
    else:
        scale_factor = width / img_width
        
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=[0, img_width * scale_factor],
            y=[0, img_height * scale_factor],
            mode="markers",
            marker_opacity=0
        )
    )

    # Configure axes
    fig.update_xaxes(
        visible=False,
        range=[0, img_width * scale_factor]
    )

    fig.update_yaxes(
        visible=False,
        range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x"
    )

    # Add image
    fig.update_layout(
        images=[go.layout.Image(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source=img)]

    )

    # Configure other layout
    fig.update_layout(
        width=img_width * scale_factor,
        height=img_height * scale_factor,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )

    if toolbar is False:
        fig.show(config={'displayModeBar': False})
        return
    
    fig.show(config={
        'modeBarButtonsToRemove': ['toImage', 
                                   'select2d',
                                   'lasso2d',
                                   'autoScale2d',
                                   'toggleSpikelines',
                                   'hoverClosestCartesian',
                                   'hoverCompareCartesian'
                                  ],
        'scrollZoom': True,
        'displayModeBar': True,
        'displaylogo': False
    })
