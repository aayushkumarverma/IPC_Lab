import streamlit as st

def _log(message):
    st.session_state.shm_events.insert(0, message)
    st.session_state.shm_events = st.session_state.shm_events[:14]

def shared_memory_page():
    st.title("🧠 Shared Memory")
    st.write(
        "Shared memory allows processes to communicate by accessing the same memory region. "
        "It can be efficient because data is not repeatedly transferred through a message channel, "
        "but access must be synchronized."
    )
    st.caption("Simulation model: one shared data region protected by a mutex.")

    defaults = {
        "shm_data": "Welcome to IPC Lab",
        "shm_lock_owner": None,
        "shm_events": ["Shared memory initialized. Mutex is unlocked."],
        "shm_last_writer": "System",
        "shm_last_reader": "No read yet",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    lock_owner = st.session_state.shm_lock_owner
    status = "UNLOCKED" if lock_owner is None else f"LOCKED by {lock_owner}"
    st.markdown("### Shared memory status")
    a, b, c = st.columns(3)
    a.metric("Current stored value", "Available" if st.session_state.shm_data else "Empty")
    b.metric("Mutex status", "Unlocked" if lock_owner is None else "Locked")
    c.metric("Last writer", st.session_state.shm_last_writer)

    st.markdown("### Process interaction")
    writer, memory, reader = st.columns([1, 1.15, 1])

    with writer:
        st.subheader("🟦 Process A")
        st.markdown("**Writer**")
        st.write("Process A must acquire the mutex before changing shared data.")
        write_value = st.text_input("Data to write", key="shm_input", placeholder="Enter text...")
        if st.button("Acquire mutex", key="shm_a_acquire", use_container_width=True):
            if lock_owner is None:
                st.session_state.shm_lock_owner = "Process A"
                _log("Process A acquired the mutex.")
                st.success("Mutex acquired by Process A.")
            else:
                _log(f"Process A requested mutex but it is held by {lock_owner}.")
                st.warning(f"Mutex is held by {lock_owner}. Process A must wait.")
        if st.button("Write to shared region", key="shm_write", use_container_width=True):
            if st.session_state.shm_lock_owner != "Process A":
                st.error("Process A cannot write. Acquire the mutex first.")
                _log("Process A write denied: it does not own the mutex.")
            elif not write_value.strip():
                st.warning("Enter a value to write.")
            else:
                st.session_state.shm_data = write_value.strip()
                st.session_state.shm_last_writer = "Process A"
                _log(f"Process A wrote: {write_value.strip()}")
                st.success("Shared memory updated.")
        if st.button("Release mutex", key="shm_a_release", use_container_width=True):
            if st.session_state.shm_lock_owner == "Process A":
                st.session_state.shm_lock_owner = None
                _log("Process A released the mutex.")
                st.success("Mutex released.")
            else:
                st.warning("Process A does not currently own the mutex.")

    with memory:
        st.subheader("Shared memory region")
        lock_owner = st.session_state.shm_lock_owner
        st.markdown(
            f"""
            <div style="background:#f0f7fc;border:2px solid #a8c8df;border-radius:13px;padding:22px;text-align:center">
              <div style="font-size:.76rem;letter-spacing:1.1px;color:#52728a;font-weight:700">COMMON DATA REGION</div>
              <div style="font-size:2.1rem;margin:12px">▤</div>
              <div style="font-size:1.05rem;font-weight:700;color:#173f5c;overflow-wrap:anywhere">{st.session_state.shm_data}</div>
              <div style="font-size:.82rem;color:#60798c;margin-top:12px">Last writer: {st.session_state.shm_last_writer}</div>
              <div style="display:inline-block;margin-top:12px;padding:6px 12px;border-radius:20px;background:{'#fde8e7' if lock_owner else '#e2f3e8'};color:{'#9b2923' if lock_owner else '#24613a'};font-size:.77rem;font-weight:700">MUTEX: {status}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("")
        st.info("The mutex protects the critical section: the part of the program that accesses shared data.")
        st.caption("In a real OS, processes map the shared region into their address spaces. This page models the behavior.")

    with reader:
        st.subheader("🟩 Process B")
        st.markdown("**Reader**")
        st.write("Process B acquires the same mutex before reading in this simplified protected-access example.")
        if st.button("Acquire mutex", key="shm_b_acquire", use_container_width=True):
            if st.session_state.shm_lock_owner is None:
                st.session_state.shm_lock_owner = "Process B"
                _log("Process B acquired the mutex.")
                st.success("Mutex acquired by Process B.")
            else:
                _log(f"Process B requested mutex but it is held by {st.session_state.shm_lock_owner}.")
                st.warning(f"Mutex is held by {st.session_state.shm_lock_owner}. Process B must wait.")
        if st.button("Read shared region", key="shm_read", use_container_width=True):
            if st.session_state.shm_lock_owner != "Process B":
                st.error("Process B cannot read in this protected-access demo. Acquire the mutex first.")
                _log("Process B read denied: it does not own the mutex.")
            else:
                st.session_state.shm_last_reader = st.session_state.shm_data
                _log(f"Process B read: {st.session_state.shm_data}")
                st.success(f"Read value: {st.session_state.shm_data}")
        if st.button("Release mutex", key="shm_b_release", use_container_width=True):
            if st.session_state.shm_lock_owner == "Process B":
                st.session_state.shm_lock_owner = None
                _log("Process B released the mutex.")
                st.success("Mutex released.")
            else:
                st.warning("Process B does not currently own the mutex.")

    st.markdown("### Last value read by Process B")
    st.code(st.session_state.shm_last_reader, language="text")

    st.markdown("### Activity log")
    for event in st.session_state.shm_events:
        st.write("• " + event)

    if st.button("Reset Shared Memory", key="shm_reset"):
        for key in defaults:
            st.session_state.pop(key, None)
        st.rerun()
