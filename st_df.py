import streamlit as st
from PIL import Image

# Define the data
previous_close = 1865.20
day_range = (1831.90, 1862.35)
year_range = (1363.55, 1880.00)
market_cap = 14.01
avg_volume = 19.79

# Create the HTML graphic
html = f"""
<div style="background-color:#f2f2f2;padding:20px;border-radius:10px;">
  <h3>Stock Information</h3>
  <table style="width:100%;">
    <tr>
      <td style="font-weight:bold;">PREVIOUS CLOSE</td>
      <td style="text-align:right;">₹{previous_close}</td>
    </tr>
    <tr>
      <td style="font-weight:bold;">DAY RANGE</td>
      <td style="text-align:right;">₹{day_range[0]} - ₹{day_range[1]}</td>
    </tr>
    <tr>
      <td style="font-weight:bold;">YEAR RANGE</td>
      <td style="text-align:right;">₹{year_range[0]} - ₹{year_range[1]}</td>
    </tr>
    <tr>
      <td style="font-weight:bold;">MARKET CAP</td>
      <td style="text-align:right;">{market_cap} INR</td>
    </tr>
    <tr>
      <td style="font-weight:bold;">AVG VOLUME</td>
      <td style="text-align:right;">{avg_volume}M</td>
    </tr>
  </table>
</div>
"""

# Display the HTML graphic
st.write(html, unsafe_allow_html=True)