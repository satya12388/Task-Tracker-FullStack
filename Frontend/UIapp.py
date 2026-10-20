import time
import streamlit as st
import requests

st.set_page_config(
    page_title="Task Manager",
    layout="wide"
)

base_url = "http://127.0.0.1:8000"

def check_server(base_url:str):
    try:
        response = requests.get(f"{base_url}/api/v1/home",timeout=3)

        if response.status_code == 200:
            msg = response.json().get("message","OK")
            return True,msg
        return False,f"server returned: {response.status_code}"

    except requests.RequestException as e:
        return False,f"server exception: {e}"


def get_all_tasks(base_url:str):
    try:
        response = requests.get(f"{base_url}/api/v1/Tasks",timeout = 5)
        if response.status_code == 200:
            return response.json()
        st.error(f"failed to fetch tasks: {response.status_code}")
        return None
    except requests.RequestException as e:
        st.error(f"error fetching tasks:{e}")
        return None

def create_task(base_url:str,name:str, description: str, is_completed: bool):
    payload = {
        "name": name.strip(),
        "description": description.strip(),
        "is_completed": is_completed
    }
    try:
        response = requests.post(f"{base_url}/api/v1/Tasks",json=payload,timeout=5)
        if response.status_code in (200, 201):
            return True, response.json().get("name","")
        else:
            return False, f"Failed to create task (HTTP {response.status_code}): {response.text}"
    except requests.RequestException as e:
        return False, f"Connection error: {e}"

def update_task(base_url: str, task_id: int, name: str, description: str, is_completed: bool):
    payload = {
        "name": name.strip(),
        "description": description.strip(),
        "is_completed": is_completed
    }
    try:
        response = requests.put(f"{base_url}/api/v1/Task/{task_id}", json=payload, timeout=5)
        if response.status_code in (200, 201):
            return True, "Task updated successfully!"
        elif response.status_code == 404:
            return False, f"Task with ID {task_id} not found."
        else:
            return False, f"Update failed (HTTP {response.status_code}): {response.text}"
    except requests.RequestException as e:
        return False, f"Connection error: {e}"


def delete_task(base_url: str, task_id: int) -> tuple[bool, str]:
    """Delete a task via DELETE /api/v1/Task/{id}."""
    try:
        response = requests.delete(f"{base_url}/api/v1/Task/{task_id}", timeout=5)
        if response.status_code in (200, 204):
            return True, "Task deleted successfully!"
        elif response.status_code == 404:
            return False, f"Task with ID {task_id} not found."
        else:
            return False, f"Delete failed (HTTP {response.status_code}): {response.text}"
    except requests.RequestException as e:
        return False, f"Connection error: {e}"


editing_id = st.session_state.get("editing_task_id")
st.title("Task Manager with streamlit and Fastapi")

is_healthy,msg = check_server(base_url)

if not is_healthy:
    st.warning(f"Backend server is not running or corrupted with exception {msg}")
    st.stop()

tasks = get_all_tasks(base_url)

total_tasks = len(tasks)
completed_tasks = sum(1 for t in tasks if t.get("is_completed", False))
pending_tasks = total_tasks - completed_tasks
completion_pct = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0

# Metrics Display
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Total Tasks", total_tasks)
col_m2.metric("Completed", completed_tasks)
col_m3.metric("Pending", pending_tasks)
col_m4.metric("Completion Rate", f"{completion_pct}%")

st.progress(completion_pct / 100)
st.write("")


tasks_list,task_create = st.tabs(["View tasks","Create Task"])

with tasks_list:
    if len(tasks) ==0:
        st.error("No Tasks Present, please create a task")

    for task in tasks:
        task_id = task.get("id")
        name = task.get("name", "Untitled")
        description = task.get("description", "")
        is_done = task.get("is_completed", False)

        with st.container(border=True):
            col_title,col_actions = st.columns([5,3])

            with col_title:
                icon = "✅" if is_done else "⏳"
                st.markdown(f"##### {icon} #{task_id}: {name}")

            # with col_status:
            #     if is_done:
            #         st.markdown("✅ Completed")
            #     else:
            #         st.markdown("⏳ Pending")

            with col_actions:
                btn_col1, btn_col2, btn_col3 = st.columns(3)

                with btn_col1:
                    toggle_label = "↩️ Undo" if is_done else "✔️ Done"
                    if st.button(toggle_label,key=f'toggle_{task_id}'):
                        ok,msg = update_task(base_url,task_id,name,description,not is_done)

                        if ok:
                            st.success(f"Status of Task with name:{name} updated successfully!")
                            st.rerun()

                        else:
                            st.error(msg)

                with btn_col2:
                    is_current_editing = (editing_id == task_id)
                    edit_label = "Close" if is_current_editing else "Edit"
                    if st.button(edit_label,key=f"edit_btn_{task_id}"):
                        if is_current_editing:
                            st.session_state["editing_task_id"] = None
                        else:
                            st.session_state["editing_task_id"] = task_id
                        st.rerun()


                
                with btn_col3:
                    toggle_label = "Delete"
                    if st.button(toggle_label,key=f'delete_{task_id}'):
                        ok,msg = delete_task(base_url,task_id)

                        if ok:
                            st.success(f"Task with name:{name} deleted successfully!")
                            st.rerun()

                        else:
                            st.error(msg)
            st.markdown(f"**Description:** {description}")

            if editing_id == task_id:
                st.markdown(f"Eding Task:{task_id}")

                with st.form(key=f"edit_form_{task_id}"):
                    new_name = st.text_input("Task Name", value=name)
                    new_desc = st.text_area("Description", value=description)
                    new_status = st.checkbox("Mark as completed", value=is_done)
                    submit_edit = st.form_submit_button("💾 Save Changes", use_container_width=True)
                    if submit_edit:
                        if not new_name.strip():
                            st.warning("Task name cannot be empty.")
                        else:
                            ok, msg = update_task(base_url, task_id, new_name, new_desc, new_status)
                            if ok:
                                st.success("Task updated successfully!")
                                st.session_state["editing_task_id"] = None
                                st.rerun()
                            else:
                                st.error(msg)

with task_create:

    st.subheader("Create a new Task")

    with st.form(key="create_task_form",clear_on_submit=True):

        task_name = st.text_input("Task Title *", placeholder="e.g. Implement user authentication")

        task_desc = st.text_area("Task Description *", placeholder="Detailed steps or acceptance criteria...")

        task_completed = st.checkbox("Already completed?", value=False)
        
        submitted = st.form_submit_button("Add Task",use_container_width=True)

        if submitted:
            if not task_name.strip():
                st.warning("⚠️ Please provide a task title.")
            elif not task_desc.strip():
                st.warning("⚠️ Please provide a task description.")
            else:
                ok, msg = create_task(base_url, task_name, task_desc, task_completed)
                if ok:
                    container = st.empty()
                    container.success(f"Task with name:{msg} created successfully!")
                    time.sleep(2)
                    container.empty()
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")  
