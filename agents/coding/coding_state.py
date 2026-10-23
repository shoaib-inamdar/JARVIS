from typing import TypedDict


class CodingState(TypedDict):
    user_request: str
    current_mode: str

    project_root: str
    relevant_files: list[str]
    open_file: str
    error_context: str

    plan_steps: list
    current_step: int
    plan_approved: bool

    proposed_path: str
    patch_approved: bool
    action_history: list

    test_results: str
    list_results: str
    verified: bool

    pending_permission: str
    safety_flags: list
    blocked: bool

    final_reply: str
    avatar_mood: str
