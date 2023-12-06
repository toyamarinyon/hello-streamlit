from openai import OpenAI
import streamlit as st
import random
import time
import pandas as pd
import numpy as np

# st.title("Plain AI")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


user_messages = list(filter(lambda message: message["role"] == "user", st.session_state.messages))
if len(user_messages) > 0:
    # Display assistant response in chat message container
    last_user_message = user_messages[-1]["content"]
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # assistant_response = random.choice(
        #     [
        #         "Hello there! How can I assist you today?",
        #         "Hi, human! Is there anything I can help you with?",
        #         "Do you need help?",
        #     ]
        # )
        if "グラフ" in last_user_message:
            full_response += f"{last_user_message}ですね。かしこまりました。少々お待ちください。"
            st.write(full_response)
            time.sleep(1)
            chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

            st.line_chart(chart_data)
            st.write("お待たせしました。")
        else:
            assistant_response = f"{last_user_message}ですね。かしこまりました！OpenAIを使って、{last_user_message}を調べてみます。"
            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            message_placeholder2 = st.empty()
            full_response2 = ""
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": "user", "content": last_user_message}
                ],
                stream=True,
            ):
                full_response2 += (response.choices[0].delta.content or "")
                message_placeholder2.markdown(full_response2 + "▌")
            message_placeholder2.markdown(full_response2)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = "こんにちは！何をお手伝いしましょうか？"
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
