import polars as pl

output_df = pl.read_csv("output.csv")


import plotly.express as px

# Group by 'date' and count the number of rows for each date
date_counts = output_df.group_by('date').count()

# Create a bar plot using Plotly
fig = px.bar(date_counts, x='date', y='count', title='Count of Rows for Each Date')

# Show the plot
fig.show()
