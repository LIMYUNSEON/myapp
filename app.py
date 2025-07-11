import streamlit as st
import json
import os

# 파일 이름 정의
todo_file = "todos.json"

# 할 일 목록 불러오기
def load_todos():
    if os.path.exists(todo_file):
        with open(todo_file, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

# 할 일 목록 저장하기
def save_todos(todos):
    with open(todo_file, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

# 스트림릿 앱 시작
st.set_page_config(page_title="오늘의 할 일", page_icon="✅")
st.title("✅ 오늘의 할 일")

# 세션 상태 초기화
if "todos" not in st.session_state:
    st.session_state.todos = load_todos()

# 새 할 일 추가
new_task = st.text_input("할 일을 입력하세요:", key="new_task")
if st.button("추가"):
    if new_task:
        st.session_state.todos.append({"task": new_task, "done": False})
        save_todos(st.session_state.todos)
        st.experimental_rerun()

# 할 일 목록 표시
st.subheader("할 일 목록")
if st.session_state.todos:
    for i, item in enumerate(st.session_state.todos):
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            st.markdown(f"{'✅ ' if item['done'] else ''}{item['task']}")
        with col2:
            if not item['done']:
                if st.button("완료", key=f"done_{i}"):
                    st.session_state.todos[i]["done"] = True
                    save_todos(st.session_state.todos)
                    st.experimental_rerun()
            else:
                if st.button("삭제", key=f"delete_{i}"):
                    st.session_state.todos.pop(i)
                    save_todos(st.session_state.todos)
                    st.experimental_rerun()
else:
    st.info("할 일이 없습니다. 새로운 할 일을 추가해보세요!")
