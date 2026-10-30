import streamlit as st
from ipc_shared_memory import shared_memory_page
from ipc_message_passing import message_passing_page
from ipc_producer_consumer import producer_consumer_page

st.set_page_config(
    page_title="IPC Lab | Operating Systems",
    page_icon="🔁",
    layout="wide",
    initial_sidebar_state="expanded",
)

# A restrained, light academic theme. The app remains readable in Streamlit's
# normal light appearance rather than forcing a dark dashboard aesthetic.
st.markdown("""
<style>
    .block-container {max-width: 1380px; padding-top: 1.6rem; padding-bottom: 2.5rem;}
    h1, h2, h3 {letter-spacing: -0.35px;}
    .main-title {font-size:2.35rem; font-weight:750; color:#183b56; line-height:1.15;}
    .subtitle {font-size:1.02rem; color:#526779; margin-top:.35rem;}
    .eyebrow {font-size:.76rem; font-weight:700; color:#39769b; letter-spacing:1.6px;}
    .module-card {
        background:#f5f9fc; border:1px solid #d9e5ee; border-radius:12px;
        padding:17px 18px; min-height:176px;
    }
    .module-card h3 {font-size:1.08rem; color:#183b56; margin:.35rem 0 .45rem 0;}
    .module-card p {font-size:.91rem; color:#526779; margin:0;}
    .module-icon {font-size:1.65rem;}
    .info-strip {
        background:#eef6fb; border-left:4px solid #5b9ac0; border-radius:7px;
        padding:12px 15px; color:#284b63;
    }
    div[data-testid="stMetric"] {
        background:#f7fafc; border:1px solid #e0e9ef; border-radius:10px;
        padding:11px 13px;
    }
    div.stButton > button {border-radius:8px; font-weight:600;}
    [data-testid="stSidebar"] {background:#f7f9fb;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🔁 IPC Lab")
    st.caption("OPERATING SYSTEMS · INTERACTIVE SIMULATOR")
    st.divider()
    page = st.radio(
        "Navigate",
        ["Overview", "Shared Memory", "Message Passing", "Producer–Consumer"],
        label_visibility="visible",
    )
    st.divider()
    st.markdown("**Project modules**")
    st.markdown("🧠 Shared Memory")
    st.markdown("✉️ Message Passing")
    st.markdown("📦 Producer–Consumer")
    st.divider()
    st.caption("Python · Streamlit")
    st.caption("Educational simulation")

if page == "Overview":
    st.markdown('<div class="eyebrow">OPERATING SYSTEMS PROJECT</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Inter-Process Communication</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">An interactive lab for understanding how processes exchange information and coordinate shared resources.</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    st.subheader("What is IPC?")
    st.write(
        "Inter-Process Communication (IPC) refers to the mechanisms an operating system "
        "provides so that independent processes can exchange data and coordinate their work. "
        "Different mechanisms solve this problem in different ways."
    )

    st.markdown("### Explore the three mechanisms")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="module-card">
          <div class="module-icon">🧠</div>
          <h3>1. Shared Memory</h3>
          <p>Processes access a common memory region. Fast data exchange requires synchronization to avoid conflicting access.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Open Shared Memory →", key="go_shm", use_container_width=True):
            st.session_state["nav_target"] = "Shared Memory"
            st.rerun()
    with c2:
        st.markdown("""
        <div class="module-card">
          <div class="module-icon">✉️</div>
          <h3>2. Message Passing</h3>
          <p>Processes communicate by sending and receiving messages through a channel such as a queue, mailbox, or pipe.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Open Message Passing →", key="go_mp", use_container_width=True):
            st.session_state["nav_target"] = "Message Passing"
            st.rerun()
    with c3:
        st.markdown("""
        <div class="module-card">
          <div class="module-icon">📦</div>
          <h3>3. Producer–Consumer</h3>
          <p>A producer adds items to a bounded buffer while a consumer removes them. Synchronization prevents invalid access.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Open Producer–Consumer →", key="go_pc", use_container_width=True):
            st.session_state["nav_target"] = "Producer–Consumer"
            st.rerun()

    # If a module shortcut was clicked, update the sidebar selection on rerun.
    if "nav_target" in st.session_state:
        target = st.session_state.pop("nav_target")
        st.session_state["navigation_radio"] = target
        st.rerun()

    st.write("")
    st.subheader("How IPC works — simplified view")
    flow1, flow2, flow3, flow4, flow5 = st.columns([1, .35, 1, .35, 1])
    with flow1:
        st.info("**Process A**\n\nNeeds to share data")
    with flow2:
        st.markdown("<div style='text-align:center;font-size:1.7rem;padding-top:18px;color:#64839a'>→</div>", unsafe_allow_html=True)
    with flow3:
        st.info("**IPC mechanism**\n\nMemory, messages, or buffer")
    with flow4:
        st.markdown("<div style='text-align:center;font-size:1.7rem;padding-top:18px;color:#64839a'>→</div>", unsafe_allow_html=True)
    with flow5:
        st.info("**Process B**\n\nReceives or uses data")

    st.subheader("Compare the mechanisms")
    st.dataframe(
        [
            {"Mechanism": "Shared Memory", "Data exchange": "Common memory region", "Main concern": "Race conditions and mutual exclusion", "Key concept": "Mutex / synchronization"},
            {"Mechanism": "Message Passing", "Data exchange": "Send and receive messages", "Main concern": "Message delivery and channel state", "Key concept": "Queue / pipe / mailbox"},
            {"Mechanism": "Producer–Consumer", "Data exchange": "Items placed in a shared buffer", "Main concern": "Buffer full or empty", "Key concept": "Bounded buffer / semaphores"},
        ],
        use_container_width=True,
        hide_index=True,
    )

    with st.expander("Important terms to know before the demonstration"):
        st.markdown("""
        - **Process:** a program in execution.
        - **IPC:** mechanisms that allow processes to exchange information.
        - **Shared memory:** a memory region accessible by multiple processes.
        - **Race condition:** a result that depends on the timing/order of concurrent operations.
        - **Mutex:** a mutual-exclusion lock that allows one process/thread into a critical section at a time.
        - **Message passing:** communication through send and receive operations.
        - **Semaphore:** a synchronization variable used to control access to resources or count available items/slots.
        - **Bounded buffer:** a buffer with a fixed maximum capacity.
        """)

   

elif page == "Shared Memory":
    shared_memory_page()
elif page == "Message Passing":
    message_passing_page()
else:
    producer_consumer_page()
