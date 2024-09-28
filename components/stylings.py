def promptStyle(message):
    return f"""
       <div style="position: relative; background-color:#E1F5FE; padding:10px; border-radius:15px; margin-bottom:10px;
                   word-wrap: break-word;">
           <p style="color:#000; font-size:16px; margin:0;">You: {message}</p>
           <div style="position: absolute; top:10px; right:-10px; width:0; height:0; 
                       border-top:10px solid transparent; border-left: 10px solid #E1F5FE;
                       border-bottom:10px solid transparent;"></div>
       </div>
       """

# can rename to style_bot_message
def botMessageStyle(message):
    return f"""
       <div style="position: relative; background-color:#C8E6C9; padding:10px; border-radius:15px; margin-bottom:10px;
                   word-wrap: break-word;">
           <p style="color:#000; font-size:16px; margin:0;">Bot: {message}</p>
           <div style="position: absolute; top:10px; left:-10px; width:0; height:0; 
                       border-top:10px solid transparent; border-right: 10px solid #C8E6C9;
                       border-bottom:10px solid transparent;"></div>
       </div>
       """