import streamlit as st
from functions.get_stock_price import stock_price


# Set title of the web app
if 'title_shown' not in st.session_state:
    st.session_state['title_shown'] = True

# Display text asking for stock code
if st.session_state['title_shown']:
    st.title('Enter Stock Code')

# Create text input box for the user to enter the stock code
stock_code = st.text_input('Stock Code')

# Create a sidebar with an image
image_path = "/home/meet.shingala/Downloads/RAGinvest.webp"  # Replace with the path to your image file
st.sidebar.image(image_path, use_container_width=True)

# Function to be called after entering the stock code
def run_function(stock_code):
    # Example: You can replace this with any function you want to run
    return f"Function output for stock code {stock_code}"

# Create a button labeled "Enter"
if st.button('Enter'):
    # Display the entered stock code when the button is pressed
    if stock_code:
        st.write(f'You entered the stock code: {stock_code}')
        # Call the function and display its output
        function_output = stock_price(stock_code)
        print(function_output)
        if function_output['code'] == 200:
            st.markdown(f"<h1>{function_output['Stock Price']}</h1>", unsafe_allow_html=True)
            # st.write(function_output)
            previous_close = function_output['Previous Close']

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




    else:
        st.write('Please enter a stock code.')
