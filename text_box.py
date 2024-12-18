import streamlit as st
from functions.get_stock_price import stock_price
from datetime import datetime, timezone, timedelta


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
        ist_offset = timedelta(hours=5, minutes=30)
        current_time = datetime.now(timezone.utc) + ist_offset
        formatted_time = current_time.strftime("%d/%m/%Y %H:%M:%S.%f") + " +IST"

        st.write(f'You entered the stock code: {stock_code}')
        # Call the function and display its output
        function_output = stock_price(stock_code)
        print('function_output', function_output)
        if function_output['code'] == 200 and function_output['Stock Price']:
            # st.write(function_output)
            try:

                # Display the stock price and time with HTML for alignment
                st.markdown(
                    f"""
                    <div style="text-align: left; margin-bottom: 0px; display: flex;">
                        <h1 style="margin: 0; font-size: 2.5rem;">{function_output['Stock Price']}</h1><h5 style="position:absolute; bottom: -12px;"> {formatted_time}</h5>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                # st.markdown(f"<h1>{function_output['Stock Price']}</h1>", unsafe_allow_html=True)

                names = function_output['names']
                figures = function_output['figure']
                if names and figures:
                    html = '''<div style="background-color:#f2f2f2;padding:20px;border-radius:10px;">
                    <h3>Stock Information</h3>
                    <table style="width:100%;">'''
                    for i in range(len(names)):
                        html += f'''<tr>
                            <td style="font-weight:bold;">{str(names[i])}</td>
                            <td style="text-align:right;">{str(figures[i])}</td>
                            </tr>                            '''
                    html += """</table></div>"""
                    print(html)
                    st.markdown(html, unsafe_allow_html=True)
            except Exception as e:
                print(e)
        if function_output['code'] == 310 and not function_output['Stock Price']:
            st.warning('The stock code seems faulty. Please check!')


    else:
        st.write('Please enter a stock code.')
