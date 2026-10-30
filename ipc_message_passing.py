import streamlit as st

def _log(message):
    st.session_state.mp_events.insert(0, message)
    st.session_state.mp_events = st.session_state.mp_events[:16]

def message_passing_page():
    st.title("✉️ Message Passing")
    st.write(
        "In message passing, processes exchange information using send and receive operations. "
        "A communication channel can temporarily hold messages until the receiving process is ready."
    )
    st.caption("Simulation model: asynchronous FIFO mailbox / pipe-like message queue.")

    if "mp_queue" not in st.session_state:
        st.session_state.mp_queue = []
    if "mp_events" not in st.session_state:
        st.session_state.mp_events = ["Communication channel initialized."]
    if "mp_received" not in st.session_state:
        st.session_state.mp_received = []

    st.markdown("### Channel configuration")
    config1, config2 = st.columns([1, 2])
    with config1:
        channel_type = st.selectbox(
            "Channel representation",
            ["Mailbox (message queue)", "Pipe-like FIFO channel"],
            key="mp_channel_type",
        )
    with config2:
        capacity = st.select_slider(
            "Maximum waiting messages",
            options=[2, 3, 4, 5, 6, 8, 10],
            value=5,
            key="mp_capacity",
        )
    st.caption("This teaching model uses FIFO ordering for both representations. Real pipes and mailboxes have different OS-level semantics.")

    sender, channel, receiver = st.columns([1, 1.2, 1])
    with sender:
        st.subheader("🟦 Process A · Sender")
        payload = st.text_area("Message content", key="mp_payload", height=110, placeholder="Type a message...")
        if st.button("➤ Send message", key="mp_send", use_container_width=True):
            if not payload.strip():
                st.warning("Enter a message before sending.")
            elif len(st.session_state.mp_queue) >= capacity:
                _log("Send blocked: communication channel is full.")
                st.error("Channel full. Sender must wait until space is available.")
            else:
                number = len(st.session_state.mp_events) + len(st.session_state.mp_received) + 1
                st.session_state.mp_queue.append({"number": number, "text": payload.strip()})
                _log(f"Process A sent message: {payload.strip()}")
                st.success("Message sent to channel.")

        st.metric("Waiting to be received", len(st.session_state.mp_queue))

    with channel:
        st.subheader("Communication channel")
        st.markdown(f"**{channel_type}**")
        current = len(st.session_state.mp_queue)
        st.progress(current / capacity, text=f"Queue occupancy: {current}/{capacity}")
        if st.session_state.mp_queue:
            for index, item in enumerate(st.session_state.mp_queue):
                st.markdown(
                    f"<div style='background:#f1f7fb;border:1px solid #d6e5ef;border-radius:9px;padding:9px 11px;margin:6px 0;color:#24465e'><b>Position {index+1}</b><br>{item['text']}</div>",
                    unsafe_allow_html=True,
                )
        else:
            st.info("The channel is empty.")
        st.caption("FIFO = First In, First Out. The oldest waiting message is received first.")
        if st.button("Clear channel", key="mp_clear", use_container_width=True):
            removed = len(st.session_state.mp_queue)
            st.session_state.mp_queue = []
            _log(f"Channel cleared. {removed} waiting message(s) discarded.")
            st.rerun()

    with receiver:
        st.subheader("🟩 Process B · Receiver")
        st.write("Receives the oldest message in the channel.")
        if st.button("⬇ Receive next message", key="mp_receive", use_container_width=True):
            if st.session_state.mp_queue:
                item = st.session_state.mp_queue.pop(0)
                st.session_state.mp_received.insert(0, item["text"])
                _log(f"Process B received: {item['text']}")
                st.success(f"Received: {item['text']}")
            else:
                _log("Receive blocked: channel is empty.")
                st.warning("Channel empty. Receiver must wait.")
        st.metric("Messages received", len(st.session_state.mp_received))

    st.markdown("### Received message history")
    if st.session_state.mp_received:
        for index, message in enumerate(st.session_state.mp_received[:8], start=1):
            st.write(f"{index}. {message}")
    else:
        st.caption("No messages have been received yet.")

    st.markdown("### Communication log")
    for event in st.session_state.mp_events:
        st.write("• " + event)

    if st.button("Reset Message Passing", key="mp_reset"):
        for key in ["mp_queue", "mp_events", "mp_received"]:
            st.session_state.pop(key, None)
        st.rerun()
