import uuid
from collections import deque
from typing import Any, Dict, List


class Session_Storage:
    """
        A class for managing sessions with a focus on maintaining a most-recently-used (MRU) order.

        Attributes:
            session_data (dict): Stores session information indexed by session ID.
            mru (deque): A double-ended queue to track session IDs in MRU order.
            to_delete (set): A set of session IDs marked for deletion.
        """
    def __init__(self):
        self.session_data = {}
        self.mru = deque()
        self.to_delete = set()

    def create_session(self, session_name):
        """
        Creates a new session with the given name, stores it, and tracks it as the most recently used session.

        Args:
            session_name (str): The name of the session to create.

        Returns:
            UUID: The unique identifier for the new session.
        """
        session_id = uuid.uuid4()
        self.session_data[session_id] = {"name": session_name, "data": ""}
        self.mru.appendleft(session_id)
        return session_id

    def delete_session(self, session_id, rerun):
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
            rerun()
        return False

    def get_sessions(self) -> List[uuid.UUID]:
        """
        Cleans up the MRU list by removing any sessions marked for deletion and returns the current MRU list.

        Returns:
            list: A list of session IDs in most-recently-used order.
        """
        seen = set()
        if self.to_delete:
            while self.mru:
                session_id = self.mru.popleft()
                if session_id in seen:
                    continue
                else:
                    seen.add(session_id)

                if session_id not in self.to_delete:
                    self.mru.append(session_id)
                else:
                    self.to_delete.remove(session_id)
        return list(self.mru)

    def get_session_data(self, session_id: uuid.UUID) -> Dict[str, Any]:
        """
        Retrieves the data for a given session.

        Args:
            session_id (UUID): The unique identifier of the session.

        Returns:
            Optional[dict]: The data associated with the session.
        """
        if session_id not in self.session_data:
            return None
        return self.session_data[session_id]

    def update_session_data(self, session_id: uuid.UUID, data: Any) -> None:
        """
        Updates the data for a given session and ensures the session is marked as most recently used.

        Args:
            session_id (UUID): The unique identifier of the session to update.
            data: The new data to store in the session.
        """
        self.session_data[session_id]["data"] = data
        if self.mru[0] != session_id:
            self.mru.appendleft(session_id)
