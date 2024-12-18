import streamlit as st
from functions.get_stock_price import stock_price
from functions.urls import normalize_url
from datetime import datetime, timezone, timedelta

def initialize_variables():
    if ''

# Set title of the web app
    if 'title_shown' not in st.session_state:
        st.session_state.title_shown = True

    if 'stock_code' not in st.session_state:
        st.session_state.stock_code = ""

    if 'image_path' not in st.session_state:
        st.session_state['image_path'] = "/home/meet.shingala/Downloads/RAGinvest.webp"  # Replace with the path to your image
        st.sidebar.image(st.session_state['image_path'], use_container_width=True)
    
    if 'function_output' not in st.session_state:
        st.session_state.function_output = {}
    
    if 'names' not in st.session_state:
        st.session_state.names = []
    


# Function to be called after entering the stock code
def run_function(stock_code):
    # Example: You can replace this with any function you want to run
    return f"Function output for stock code {stock_code}"
def business_code():
    # Create a button labeled "Enter"
    if st.button('Enter'):
        # Display the entered stock code when the button is pressed
        if stock_code:
            # The offset between GMT and IST
            ist_offset = timedelta(hours=5, minutes=30)

            # Current time in UTC + Offset = IST
            current_time = datetime.now(timezone.utc) + ist_offset

            # The output of the code will be as dd:mm:yyyy hh:mm:ss.ffffff + IST
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
                            <h1 style="margin: 0; font-size: 2.5rem;">{function_output['Stock Price']}</h1><h5 style="position:absolute; bottom: -12px;"> on {formatted_time}</h5>
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
                            name = names[i].lower()
                            # Convert the website to URL and provide anchor tag
                            if name == "website":
                                naive_url = str(figures[i])
                                url = normalize_url(naive_url)
                                html += f'''<tr>
                                <td style="font-weight:bold;">{str(names[i])}</td>
                                <td style="text-align:right;"><a href={url}>{naive_url}</a></td>
                                </tr>                            '''    
                            
                            # provide a google search for the CEO
                            elif name == "ceo":
                                ceo = str(figures[i])
                                ceo_url = ceo.replace(" ","%20")

                                url = f"https://www.google.com/search?q={ceo_url}&hl=en"
                                html += f'''<tr>
                                    <td style="font-weight:bold;">{str(names[i])}</td>
                                    <td style="text-align:right;"><a href={url}>{ceo}</a></td>
                                    </tr>                            '''
                            # All the other field are treated normally
                            else:
                                html += f'''<tr>
                                    <td style="font-weight:bold;">{str(names[i])}</td>
                                    <td style="text-align:right;">{str(figures[i])}</td>
                                    </tr>                            '''
                        html += """</table></div>"""
                        # print(html)
                        st.markdown(html, unsafe_allow_html=True)
                except Exception as e:
                    print(e)
                else:
                    st.markdown("---")
                    html = """<h3>Stock Charts</h3>
                    """
                    st.markdown(html, unsafe_allow_html = True)
                    # Adding buttons for the time chart
                    buttons = {
                        "Button 1": "1D",
                        "Button 2": "5D",
                        "Button 3": "1M",
                        "Button 4": "3M",
                        "Button 5": "6M",
                        "Button 6": "1Y",
                        "Button 7": "3Y",
                        "Button 8": "5Y",
                    }

                    # Create columns for buttons
                    cols = st.columns(len(buttons))

                    # Display buttons in one row
                    for col, (label, message) in zip(cols, buttons.items()):
                        if col.button(message, use_container_width = True):
                            print(message)


            if function_output['code'] == 310 and not function_output['Stock Price']:
                st.warning('The stock code seems faulty. Please check!')


        else:
            st.write('Please enter a stock code.')


def main():
    try:
        st.set_page_config(
            page_title="RAGInvest",  # Title of the browser tab
            page_icon="/home/meet.shingala/Downloads/RAGinvest.ico",                  # Optional: favicon icon for the tab
            layout="centered"                # Layout: "centered" or "wide"
        )
        business_code()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()