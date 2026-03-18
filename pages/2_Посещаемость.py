with tab_mark:
    st.subheader("Ежедневная отметка")
    selected_date = st.date_input("Выберите дату", value=date.today(), key="mark_date")
    
    # 1. Вызываем БЕЗ db в скобках
    raw_children = get_all_children()
    all_children = to_dict_list(raw_children)
    
    # 2. Фильтруем активных
    active_children = [c for c in all_children if c.get('status') == 'активный']
    
    if active_children:
        # 3. Вызываем БЕЗ db в скобках
        existing_raw = get_attendance_by_date(selected_date)
        existing_att = to_dict_list(existing_raw)
        att_dict = {row['child_id']: row['status'] for row in existing_att}
        
        with st.form("attendance_form"):
            status_selections = {}
            for child in active_children:
                col1, col2 = st.columns([2, 3])
                col1.write(f"{child.get('last_name', '')} {child.get('first_name', '')}")
                
                default_status = att_dict.get(child['id'], "присутствовал")
                status_selections[child['id']] = col2.radio(
                    "Статус", ["присутствовал", "отсутствовал", "болел"],
                    index=["присутствовал", "отсутствовал", "болел"].index(default_status),
                    key=f"child_{child['id']}", horizontal=True, label_visibility="collapsed"
                )
            
            if st.form_submit_button("💾 Сохранить журнал"):
                for child_id, status in status_selections.items():
                    # 4. Вызываем БЕЗ db в скобках
                    add_attendance(child_id, selected_date, status)
                st.success("✅ Сохранено!")
                st.rerun()
