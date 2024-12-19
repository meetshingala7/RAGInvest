import streamlit as st
from functions.get_stock_price import stock_price
from functions.urls import normalize_url
from datetime import datetime, timezone, timedelta

def initialize_variables():
    if 'title' not in st.session_state:
        st.session_state.title = 'Enter Stock Code'
        

    if 'stock_code' not in st.session_state:
        st.session_state.stock_code = ""

    if 'image_path' not in st.session_state:
        st.session_state.image_path = "/home/meet.shingala/Downloads/RAGinvest.webp"  # Replace with the path to your image
        # st.sidebar.image(st.session_state.image_path, use_container_width=True)
    
    if 'function_output' not in st.session_state:
        st.session_state.function_output = {}
    
    if 'names' not in st.session_state:
        st.session_state.names = []
    
    if 'figures' not in st.session_state:
        st.session_state.figures = []
    
    if 'buttons' not in st.session_state:
        st.session_state.buttons = {
            "Button 1": "1D",
            "Button 2": "5D",
            "Button 3": "1M",
            "Button 4": "3M",
            "Button 5": "6M",
            "Button 6": "1Y",
            "Button 7": "3Y",
            "Button 8": "5Y",
        }
    
    if 'cols' not in st.session_state:
        st.session_state.cols = 0

    st.session_state.enter_pressed = False


    
def business_code():
    # Create a button labeled "Enter"
    if st.session_state['stock_code'] == "":
        st.session_state.enter_pressed = False
        st.session_state.stock_code = st.text_input('Stock Code')
    st.sidebar.image(st.session_state.image_path, use_container_width=True)

    if st.button('Enter') or st.session_state.enter_pressed:
        st.session_state.enter_pressed = True
        # Display the entered stock code when the button is pressed

        if st.session_state.stock_code:
            # The offset between GMT and IST
            ist_offset = timedelta(hours=5, minutes=30)

            # Current time in UTC + Offset = IST
            current_time = datetime.now(timezone.utc) + ist_offset

            # The output of the code will be as dd:mm:yyyy hh:mm:ss.ffffff + IST
            formatted_time = current_time.strftime("%d/%m/%Y %H:%M:%S.%f") + " +IST"

            st.write(f'You entered the stock code: {st.session_state.stock_code}')
            # Call the function and display its output
            st.session_state.function_output = stock_price(st.session_state.stock_code)
            # print('st.session_state.function_output', st.session_state.function_output)
            if st.session_state.function_output['code'] == 200 and st.session_state.function_output['Stock Price']:
                # try:
                # Display the stock price and time with HTML for alignment
                st.markdown(
                    f"""
                    <div style="text-align: left; margin-bottom: 0px; display: flex;">
                        <h1 style="margin: 0; font-size: 2.5rem;">{st.session_state.function_output['Stock Price']}</h1><h5 style="position:absolute; bottom: -12px;"> on {formatted_time}</h5>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                
                st.session_state.names = st.session_state.function_output['names']
                st.session_state.figures = st.session_state.function_output['figure']
                if st.session_state.names and st.session_state.figures:
                    try:
                        html = '''<div style="background-color:#f2f2f2;padding:20px;border-radius:10px;">
                        <h3>Stock Information</h3>
                        <table style="width:100%;">'''
                        print(st.session_state.names)
                        print()    
                        for i in range(len(st.session_state.names)):
                            name = st.session_state.names[i].lower()

                            # Convert the website to URL and provide anchor tag
                            if name == "website":
                                naive_url = str(st.session_state.figures[i])
                                url = normalize_url(naive_url)
                                html += f'''<tr>
                                <td style="font-weight:bold;">{str(st.session_state.names[i])}</td>
                                <td style="text-align:right;"><a href={url}>{naive_url}</a></td>
                                </tr>                            '''    
                            
                            # provide a google search for the CEO
                            elif name == "ceo":
                                ceo = str(st.session_state.figures[i])
                                ceo_url = ceo.replace(" ","%20")

                                url = f"https://www.google.com/search?q={ceo_url}&hl=en"
                                html += f'''<tr>
                                    <td style="font-weight:bold;">{str(st.session_state.names[i])}</td>
                                    <td style="text-align:right;"><a href={url}>{ceo}</a></td>
                                    </tr>                            '''
                            
                            # All the other field are treated normally
                            else:
                                html += f'''<tr>
                                    <td style="font-weight:bold;">{str(st.session_state.names[i])}</td>
                                    <td style="text-align:right;">{str(st.session_state.figures[i])}</td>
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
                        st.session_state.cols = st.columns(len(st.session_state.buttons))
                        # Display buttons in one row
                        # print(st.session_state.cols)
                        # print(st.session_state.buttons.items())
                        st.write(st.session_state.enter_pressed)
                        st.write(st.session_state['stock_code'])
                        if st.button('1D'):
                        # for col, (label, message) in zip(st.session_state.cols, st.session_state.buttons.items()):
                        #     if col.button(message, use_container_width = True):
                            st.write("It works")
                            # st.write(message)


            if st.session_state.function_output['code'] == 310 and not st.session_state.function_output['Stock Price']:
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
        initialize_variables()
        business_code()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()