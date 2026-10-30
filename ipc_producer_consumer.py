import streamlit as st

def _log(message):
    st.session_state.pc_events.insert(0, message)
    st.session_state.pc_events = st.session_state.pc_events[:18]

def producer_consumer_page():
    st.title("📦 Producer–Consumer Problem")
    st.write(
        "The producer generates items and inserts them into a bounded buffer. "
        "The consumer removes items. Synchronization prevents the producer from inserting "
        "when the buffer is full and the consumer from removing when it is empty."
    )
    st.caption("Simulation model: bounded buffer with mutex, empty-slot count, and full-slot count.")

    defaults = {
        "pc_buffer": [],
        "pc_next_id": 1,
        "pc_events": ["Buffer initialized. Mutex unlocked."],
        "pc_mutex": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    capacity = st.select_slider(
        "Buffer capacity",
        options=[2, 3, 4, 5, 6, 7, 8],
        value=4,
        key="pc_capacity",
    )
    buffer = st.session_state.pc_buffer
    count = len(buffer)
    empty_slots = max(0, capacity - count)
    full_slots = count
    over_capacity = count > capacity

    st.markdown("### Buffer status")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Items in buffer", count)
    c2.metric("Empty slots", empty_slots)
    c3.metric("Full slots", full_slots)
    c4.metric("Mutex", "Locked" if st.session_state.pc_mutex else "Unlocked")

    st.markdown("### Visual bounded buffer")
    slots = st.columns(capacity)
    for i in range(capacity):
        if i < count:
            item = buffer[i]
            slots[i].markdown(
                f"<div style='height:88px;background:#e8f2fa;border:1px solid #a9c9df;border-radius:10px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#1c4967'><span style='font-size:.7rem'>SLOT {i+1}</span><b style='font-size:1.15rem'>Item {item}</b><span style='font-size:.7rem'>Occupied</span></div>",
                unsafe_allow_html=True,
            )
        else:
            slots[i].markdown(
                f"<div style='height:88px;background:#fafcfd;border:1px dashed #c4d3de;border-radius:10px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#8a9ba8'><span style='font-size:.7rem'>SLOT {i+1}</span><b>Empty</b></div>",
                unsafe_allow_html=True,
            )

    st.progress(min(count / capacity, 1.0), text=f"Buffer occupancy: {count}/{capacity}")
    if over_capacity:
        st.warning("The capacity was reduced below the current number of stored items. Consume items until the buffer is within the selected capacity.")

    producer, consumer = st.columns(2)
    with producer:
        st.subheader("🟦 Producer")
        st.write("Creates a new item and inserts it into the next available slot.")
        produce_disabled = over_capacity or st.session_state.pc_mutex
        if st.button("＋ Produce item", key="pc_produce", use_container_width=True, disabled=produce_disabled):
            if len(st.session_state.pc_buffer) >= capacity:
                st.error("BUFFER FULL — producer cannot add another item.")
                _log("Producer blocked: no empty slots remain.")
            else:
                st.session_state.pc_mutex = True
                item = st.session_state.pc_next_id
                st.session_state.pc_buffer.append(item)
                st.session_state.pc_next_id += 1
                st.session_state.pc_mutex = False
                _log(f"Producer inserted Item {item}. Empty={capacity-len(st.session_state.pc_buffer)}, Full={len(st.session_state.pc_buffer)}.")
                st.success(f"Item {item} produced.")
        if len(st.session_state.pc_buffer) >= capacity:
            st.warning("Buffer is FULL. Producer must wait for an item to be consumed.")

    with consumer:
        st.subheader("🟩 Consumer")
        st.write("Removes the oldest item from the buffer (FIFO order).")
        if st.button("− Consume item", key="pc_consume", use_container_width=True, disabled=st.session_state.pc_mutex):
            if not st.session_state.pc_buffer:
                st.error("BUFFER EMPTY — consumer has no item to remove.")
                _log("Consumer blocked: no full slots are available.")
            else:
                st.session_state.pc_mutex = True
                item = st.session_state.pc_buffer.pop(0)
                st.session_state.pc_mutex = False
                _log(f"Consumer removed Item {item}. Empty={max(0, capacity-len(st.session_state.pc_buffer))}, Full={len(st.session_state.pc_buffer)}.")
                st.success(f"Item {item} consumed.")
        if not st.session_state.pc_buffer:
            st.warning("Buffer is EMPTY. Consumer must wait for an item to be produced.")

    st.markdown("### Synchronization concepts")
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown("**`empty` semaphore**")
        st.metric("Available spaces", empty_slots)
        st.caption("Producer waits if this reaches zero.")
    with s2:
        st.markdown("**`full` semaphore**")
        st.metric("Available items", full_slots)
        st.caption("Consumer waits if this reaches zero.")
    with s3:
        st.markdown("**`mutex`**")
        st.metric("Critical section", "Busy" if st.session_state.pc_mutex else "Free")
        st.caption("Protects buffer modification.")

    with st.expander("How the synchronization works"):
        st.markdown("""
        1. Initially, `empty = buffer capacity`, `full = 0`, and `mutex = 1`.
        2. A producer waits for an empty slot, enters the critical section, inserts an item, and signals that one more item is full.
        3. A consumer waits for a full slot, enters the critical section, removes an item, and signals that one more slot is empty.
        4. The mutex ensures that only one process modifies the shared buffer at a time.

        This application visualizes these rules; it does not launch real concurrent OS processes or kernel semaphores.
        """)

    st.markdown("### Activity log")
    for event in st.session_state.pc_events:
        st.write("• " + event)

    if st.button("Reset Producer–Consumer", key="pc_reset"):
        for key in defaults:
            st.session_state.pop(key, None)
        st.rerun()
