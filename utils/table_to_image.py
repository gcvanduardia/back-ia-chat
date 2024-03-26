import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

def create_image_base64(combined_json):
    # Convert your data to a DataFrame
    df = pd.DataFrame(combined_json)

    # Create a figure and add a table
    fig, ax = plt.subplots(1, 1)
    table = pd.plotting.table(ax, df, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    plt.axis('off')

    # Save the figure to an image file
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Read the image file and encode it to base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return 'data:image/png;base64,'+image_base64