import streamlit as st
import pandas as pd
from datetime import date
import sys
from pathlib import Path

# Добавляем путь для импортов
sys.path.append(str(Path(__file__).resolve().parent.parent))
from crud import get_all_children, add_attendance, get_attendance_by_date, get_all_attendance

st.set_page_config(page_title="Посещаемость", page_icon="📅", layout="wide")
st.title("Учет посещаемости 📅")

# Наша проверенная функция-конвертер
def to_dict_list(query_results):
    data = []
    if query_results:
        for item in query_results:
            try:
                row = {col.name: getattr(item, col.name) for col in item.__table__.columns}
                data.append(row)
            except:
                continue
    return data

tab_mark, tab_log = st.tabs(["📍 Отметить присутствие", "📖 Журнал посещаемости"])

with tab_mark:
    st.subheader("Ежедневная отметка")
    selected_date = st.date_input("Выберите дату", value=date.today(), key="mark_date")
    
    # Получаем список детей и переводим в понятный формат
    raw_children = get_all_children()
    all_children = to_dict_list(raw_children)
    
    # Фильтруем только активных
    active_children = [c for c in all_children if c.get('status') == 'активный']
    
    if active_children:
        # Проверяем, есть ли уже отметки на эту дату
        existing_raw = get_attendance_by_date(selected_date)
        existing_att = to_dict_list(existing_raw)
        att_dict = {row['child_id']: row['status'] for row in existing_att}
        
        with st.form("attendance_form"):
            st.write(f"Отметка на **{selected_date.strftime('%d.%m.%Y')}**")
            
            status_selections = {}
            
            for child in active_children:
                col1, col2 = st.columns([2, 3])
                full_name = f"{child.get('last_name', '')} {child.get('first_name', '')}"
                col1.write(full_name)
                
                # Если отметка уже была, ставим её, иначе "присутствовал"
                current_val = att_dict.get(child['id'], "присутствовал")
                options = ["присутствовал", "отсутствовал", "болел"]
                
                status_selections[child['id']] = col2.radio(
                    f"Статус для {child['id']}", 
                    options,
                    index=options.index(current_val),
                    key=f"child_{child['id']}",
                    horizontal=True,
                    label_visibility="collapsed"
                )
            
            if st.form_submit_button("💾 Сохранить журнал", type="primary"):
                for child_id, status in status_selections.items():
                    add_attendance(child_id, selected_date, status)
                st.success("✅ Журнал посещаемости обновлен!")
                st.rerun()
    else:
        st.info("Нет активных детей. Добавьте их в разделе 'Дети'.")

with tab_log:
    st.subheader("История посещаемости")
    # В crud.py мы сделали функцию get_all_attendance, которая сразу возвращает словари с именами
    history = get_all_attendance()
    
    if history:
        df = pd.DataFrame(history)
        # Переименуем для красоты
        df.columns = ['Дата', 'Имя', 'Фамилия', 'Статус']
        st.dataframe(df.sort_values(by='Дата', ascending=False), use_container_width=True, hide_index=True)
    else:
        st.info("Записей пока нет.")
