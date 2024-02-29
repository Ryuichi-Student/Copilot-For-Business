# TODO: Reduce the number of tokens used (the database merger!)
# TODO: Add a stop and a fast forward button during text stream button
# TODO: Add a progress bar for the database merger
# TODO: Remove the folder in the database merger
# TODO: Optimise single database queries
# TODO: Add session rename feature
# TODO: Handle errors more gracefully
# TODO: Save images correctly - the image colours are wrong...
# TODO: Make sure answers are consistent! Using one metric -> using a lot of metrics should still talk about the same thing.

import atexit
import threading
import time
from functools import wraps

import streamlit as st
import sys
import os

from streamlit.runtime.scriptrunner import add_script_run_ctx

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.backend.copilot import Copilot
from src.backend.utils.sessions import Session_Storage
from src.backend.utils.dbmaker import join_dbs, get_database_list
from src.backend.utils.gpt import stream
from concurrent.futures import ThreadPoolExecutor
import plotly.io as pio


# Wrapper to load streamlit widgets asynchronously
def load_async():
    def decorator(func):
        def wrapper(*args, **kwargs):
            def task():
                time.sleep(0.1)
                func(*args, **kwargs)

            executor = st.session_state.executor
            executor.submit(task)
            for t in executor._threads:
                add_script_run_ctx(t)
            # print(getattr(threading.current_thread(), "streamlit_script_run_ctx", "No script run context").session_id)

        return wrapper
    return decorator


if "session_storage" not in st.session_state:
    st.session_state.session_storage = Session_Storage(st.rerun)
if "plot_changed" not in st.session_state:
    st.session_state.plot_changed = False

session_manager = st.session_state.session_storage


# ----------------------------------   Creating a session   ----------------------------------

def display_session_ui(p):
    print("Displaying session UI")
    # If there are no sessions or all are named, create a new one and flags it to be named.
    if session_manager.requires_autogenerated_session:
        session_manager.create_session(f"New Session", rerun=False)
        sessions = session_manager.get_sessions()
        session_manager.update_config(sessions[-1], {"autogenerate": True}, overwrite=False)

    sessions = session_manager.get_sessions()

    current_session_id = p.selectbox(
        label="Select a session:",
        options=sessions,
        format_func=lambda x: session_manager.get_session_data(x)['name'],
        index=0,  # Automatically switch to the most recent session ID
        key="session_id",
        on_change=lambda: session_manager.use_session(st.session_state.session_id),
    )  # type: ignore

    print(f"New session: {current_session_id}")
    return current_session_id


def create_copilot(current_session):
    print("Creating copilot")
    copilot = current_session['data']
    if copilot is None:
        print("Creating new copilot")
        options = st.session_state.selected_db
        print(options)
        args = join_dbs(options)
        if isinstance(args, dict):
            copilot = Copilot(db=args["name"], dbtype='sqlite', potential_embedded=args["embedded"],
                              non_embedded=args["not-embedded"])
        else:
            copilot = Copilot(db=f"{args}", dbtype='sqlite')

        session_manager.update_session_data(current_session_id, data=copilot)
    return copilot


col1, col2 = st.columns([7, 3])

with st.sidebar:
    # Session data
    # TODO: Load from persistent storage
    _p = st.empty()
    current_session_id = display_session_ui(_p)

# ----------------------------------   Choosing databases   ----------------------------------


# Choose a database
l = get_database_list()
session_manager.update_config(current_session_id, {
    "selected_db": [] if not l else [max(l, key=os.path.getctime)],
    "query": None,
    "finished": False
}, overwrite=False)


def select_databases(placeholder, session_id):
    def _on_change():
        session_manager.update_config(
            session_id, {"selected_db": st.session_state.databases}
        )
        print(f"Loading databases: {st.session_state.databases}")

    options = placeholder.multiselect(
        label="Select databases to load",
        options=get_database_list(),
        default=session_manager.get_config(session_id, "selected_db"),
        on_change=_on_change,
        key="databases",
        disabled=session_manager.get_config(session_id, "query") is not None
    )

    return options


with st.sidebar:
    db_placeholder = st.empty()
    databases = select_databases(db_placeholder, current_session_id)

# ----------------------------------   Ask for query   ----------------------------------
col1, col2 = st.columns([7, 3])

with col1:
    # title
    st.header("Copilot for Business")
    st.subheader(session_manager.get_session_data(current_session_id)["name"])

if not session_manager.get_config(current_session_id, "query"):
    userQuery = st.chat_input("Enter your question")
    if userQuery:
        options = db_placeholder.multiselect(
            label="Select databases to load",
            options=get_database_list(),
            default=session_manager.get_config(current_session_id, "selected_db"),
            disabled=True
        )
        session_manager.update_config(current_session_id, {"query": userQuery})
        if session_manager.get_config(current_session_id, "autogenerate"):
            session_manager.update_config(current_session_id, {"autogenerate": False})
            placeholder = st.empty()
            for x in session_manager.update_session_name(current_session_id, userQuery):
                placeholder.text(x)
            placeholder.empty()

        st.rerun()
else:
    userQuery = session_manager.get_config(current_session_id, "query")


# ----------------------------------   Create a Copilot   ----------------------------------
def create_copilot():
    copilot = session_manager.get_session_data(current_session_id)["data"]
    if copilot is None:
        options = session_manager.get_config(current_session_id, "selected_db")
        print(options)
        args = join_dbs(options)
        if isinstance(args, dict):
            copilot = Copilot(db=args["name"], dbtype='sqlite', potential_embedded=args["embedded"],
                              non_embedded=args["not-embedded"])
        else:
            print(f"Creating new copilot with {args}")
            copilot = Copilot(db=f"{args}", dbtype='sqlite')
        session_manager.update_session_data(current_session_id, data=copilot)
    return copilot


def handle_toggles_and_plot(userQuery):
    if "executor" in st.session_state:
        st.session_state.executor.shutdown(wait=False)
    st.session_state.executor = ThreadPoolExecutor(max_workers=4)

    @load_async()
    def show_plot():
        def run():
            if st.session_state.plot_changed:
                st.session_state.plot_changed = False
            else:
                # if "plot.jpeg" in os.listdir("."):
                #     _plot_placeholder.image("plot.jpeg")
                pass
            print("showing plot")
            fig = plot.generate()
            config = {'displayModeBar': False}
            _plot_placeholder.plotly_chart(fig, config=config)
            print("Finished showing plot")
        
        if _spinner_placeholder is not None:
            print("spinning")
            with _spinner_placeholder, st.spinner("Plotting graph..."):
                run()
        else:
            run()

    @load_async()
    def show_sql():
        print("showing sql")
        with st.expander("See SQL"):
            if plot:
                plot.formatSQL()
            else:
                st.write(copilot.get_sql(userQuery))
        print("Finished showing sql")

        # else:
        #     print("Not showing sql")

    if plot:
        # Update for showing top 10 values toggle
        if plot.dfLength > 10:
            current_topN_state = False if "topN" not in st.session_state else st.session_state.topN

            def change_plot():
                st.session_state.plot_changed = True
                print("Plot changed")
            _plot_toggle_placeholder.toggle(label="Show top 10 values only", key="topN",
                                                   value=current_topN_state, on_change=change_plot)

            plot.topn(10, current_topN_state)
        show_plot()

    # current_sqlView_state = False if "sqlView" not in st.session_state else st.session_state.sqlView
    # sqlView = _sql_toggle_placeholder.toggle("Show SQL", key="sqlView", value=current_sqlView_state)

    show_sql()

    st.session_state.executor.shutdown(wait=True)

if userQuery:
    copilot = create_copilot()

    # ----------------------------------   Query the Copilot   ----------------------------------

    # display the user's entered prompt
    st.text(f"USER:\n{userQuery}\n\nCOPILOT:")

    status_placeholder = st.empty()
    if not session_manager.get_config(current_session_id, "finished"):
        status = status_placeholder.status("Thinking...", expanded=True)
        copilot.set_status_placeholder(status)
    copilot.query(userQuery)

    # button to allow the user to accept or remove

    t = copilot.get_early_answer(userQuery)
    if t:
        status_placeholder.empty()
        k = st.empty()
        if session_manager.get_config(current_session_id, "finished"):
            k.write(t)
        else:
            session_manager.update_config(current_session_id, {"finished": True})
            @load_async(component=None)
            def _stream():
                for x in stream(t):
                    k.write(x)
            _stream()
    else:
        plot = copilot.get_plot(userQuery)

        status_placeholder.empty()
        _spinner_placeholder = st.empty()
        _plot_placeholder = st.empty()
        _plot_toggle_placeholder = st.empty()
        _plot_toggle_placeholder.toggle(label="Show top 10 values only")
        # _sql_placeholder = st.empty()
        # _sql_toggle_placeholder = st.empty()
        # _sql_toggle_placeholder.toggle("Show SQL")

        # none type has no attribute formatSQL
        handle_toggles_and_plot(userQuery)


        # drop down expander that shows the generalised answer created for the graph
        with st.expander("See explanation"):
            generalised_answer = copilot.get_generalised_answer(userQuery)
            if generalised_answer:
                st.write(generalised_answer)
            else:
                st.write("Copilot for Business was not able to generate a text explanation. Please try to refine your question to help")


        # _t = st.empty()
        # t = copilot.get_generalised_answer(userQuery)
        # if t:
        #     if session_manager.get_config(current_session_id, "finished"):
        #         _t.write(t)
        #     else:
        #         session_manager.update_config(current_session_id, {"finished": True})
        #         for x in stream(t):
        #             _t.write(x)
        # else:
        #     st.markdown(
        #         "Copilot for Business was not able to generate an answer. Please try to refine your question to help")



@atexit.register
def shutdown():
    print("Cleaning up threadpool")
    if "executor" in st.session_state:
        st.session_state.executor.shutdown(wait=False)
        print("Shutting down UI threadpool")