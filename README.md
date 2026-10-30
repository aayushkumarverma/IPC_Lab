# IPC Lab — Inter-Process Communication Simulator

A light-themed, interactive Operating Systems project built with Python and Streamlit.

## Modules
1. **Shared Memory** — common memory region, writer/reader processes, mutex ownership, protected read/write, activity log.
2. **Message Passing** — sender and receiver, FIFO queue, channel capacity, full/empty channel handling, receive history.
3. **Producer–Consumer** — adjustable bounded buffer, producer/consumer actions, full/empty states, mutex and semaphore concepts.

## Run
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Files
- `app.py` — overview, navigation, comparison table and integration.
- `ipc_shared_memory.py` — Shared Memory module.
- `ipc_message_passing.py` — Message Passing module.
- `ipc_producer_consumer.py` — Producer–Consumer module.

## Demo sequence
- Shared Memory: Process A acquires mutex → writes → releases; Process B acquires → reads → releases. Try writing without the lock.
- Message Passing: set a small capacity → send messages until full → attempt one extra send → receive in FIFO order → try receiving when empty.
- Producer–Consumer: fill buffer → attempt production when full → consume → produce again → empty buffer → attempt consumption.

## Academic scope
This is a conceptual interactive simulator. It models IPC behavior in one Streamlit session; it does not create real OS processes, kernel shared-memory segments, OS pipes, or actual OS-level semaphores. Mutex and semaphore behavior is represented for teaching and demonstration.
