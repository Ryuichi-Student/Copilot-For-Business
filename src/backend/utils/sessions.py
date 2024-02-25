import time
import uuid
from collections import deque
from typing import Any, Dict, List, Optional, Iterable
from src.backend.utils.gpt import get_gpt_response


# TODO: Load from and save to persistent storage
class Session_Storage:
    """
        A class for managing sessions with a focus on maintaining a most-recently-used (MRU) order.

        Attributes:
            session_data (dict): Stores session information indexed by session ID.
            mru (deque): A double-ended queue to track session IDs in MRU order.
            to_delete (set): A set of session IDs marked for deletion.
    """

    def __init__(self, rerun):
        self.session_data = {}
        self.mru: deque = deque()
        self.to_delete = set()
        self.rerun = rerun

    def create_session(self, session_name, rerun=True, autogenerate=True):
        """
        Creates a new session with the given name, stores it, and tracks it as the most recently used session.

        Args:
            rerun:
            session_name (str): The name of the session to create.
        """
        session_id = uuid.uuid4()
        self.session_data[session_id] = {"name": session_name, "data": None}
        self.mru.append(session_id)
        if not autogenerate:
            self.session_data[session_id]["autogenerate"] = False
        if rerun:
            self.rerun()

    def delete_session(self, session_id):
        """
        Marks a session for deletion and triggers a UI rerun. Actual deletion from the MRU tracking is deferred.

        Args:
            session_id (UUID): The unique identifier of the session to delete.
            rerun (function): A callback function to trigger UI rerun.

        Returns:
            bool: False if the session couldn't be deleted (session not found).
        """
        if session_id in self.session_data:
            del self.session_data[session_id]
            self.to_delete.add(session_id)
            self.rerun()
        return False

    def get_sessions(self) -> List[uuid.UUID]:
        """
        Cleans up the MRU list by removing any sessions marked for deletion and returns the current MRU list.

        Returns:
            list: A list of session IDs in most-recently-used order.
        """
        self.update_sessions()
        return list(self.mru)

    def update_sessions(self) -> None:
        """
        Cleans up the MRU list by removing any sessions marked for deletion.
        :return:
        """
        seen = set()
        new: deque = deque()
        while self.mru:
            session_id = self.mru.popleft()
            if session_id in seen:
                continue
            else:
                seen.add(session_id)

            if session_id not in self.to_delete:
                new.append(session_id)
            else:
                self.to_delete.remove(session_id)
        self.mru = new

    def get_session_data(self, session_id: uuid.UUID, update=False) -> Optional[Dict[str, Any]]:
        """
        Retrieves the data for a given session.

        Args:
            session_id (UUID): The unique identifier of the session.

        Returns:
            Optional[dict]: The data associated with the session.
        """
        if session_id not in self.session_data:
            return None

        if update:
            self.update_sessions()

        return self.session_data[session_id]

    def update_session_data(self, session_id: uuid.UUID, data: Any = None) -> None:
        """
        Updates the data for a given session and ensures the session is marked as most recently used.

        Args:
            session_id (UUID): The unique identifier of the session to update.
            data: The new data to store in the session.
        """
        if data is not None:
            self.session_data[session_id]["data"] = data
        if self.mru[0] != session_id:
            self.mru.appendleft(session_id)
            self.update_sessions()

            self.rerun()

    def update_session_name(self, session_id: str, query: str) -> Iterable[str]:
        """
        Uses the query to generate a name for the session and updates the session with the new name.

        Args:
            session_id (str): The unique identifier of the session to update.
            query (str): The query to use for generating the session name.
        """
        name = get_gpt_response(("user", f"""I want to generate a name for a GPT session, based on the user's query. Write down a short name (and nothing else) that describes and summarises the query: "{query}"."""))
        print(f"Named autogenerated session as {name}")
        self.session_data[session_id]["name"] = name
        x = ""
        for letter in name:
            x += letter
            yield f"Generating session name: {x} "
            time.sleep(0.1)
        yield f"Generated session: {x} "
        time.sleep(0.4)

    def update_config(self, session_id: str, config: Dict[str, Any], overwrite=True, rerun=False) -> None:
        if overwrite:
            self.session_data[session_id] |= config
        else:
            for key in config:
                if key not in self.session_data[session_id]:
                    self.session_data[session_id][key] = config[key]
        if rerun:
            self.rerun()

    def get_config(self, session_id: uuid.UUID, config_name) -> Optional[Any]:
        if config_name not in self.session_data[session_id]:
            return None
        return self.session_data[session_id][config_name]

    def use_session(self, session_id: str) -> None:
        self.mru.appendleft(session_id)

    @property
    def requires_autogenerated_session(self) -> bool:
        s = self.get_sessions()
        return not s or all(
                not self.get_config(session, "autogenerate") for session in s
        )
