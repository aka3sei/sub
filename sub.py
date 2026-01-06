import streamlit as st

# ページ設定
st.set_page_config(page_title="営業評価シミュレーター", layout="wide")

st.title("📊 営業評価・ボーナス算定シミュレーター")
st.caption("営業評価_個人：数値評価と行動評価に基づき、最終支給額をシミュレーションします。")

# --- サイドバー：【A】基本情報 ---
st.sidebar.header("【A】基本情報")
name = st.sidebar.text_input("氏名", value="営業 太郎")
monthly_salary = st.sidebar.number_input("月給 (円)", value=300000, step=10000)
base_bonus_months = st.sidebar.number_input("基本ボーナス月数 (例: 2)", value=2.0, step=0.1)

# --- メインエリア：3カラム構成 ---
col1, col2, col3 = st.columns(3)

with col1:
    st.header("【B】数値評価 (60%)")
    st.write("実績を入力してください")
    
    # 売上高
    s_target = st.number_input("売上目標 (万円)", value=1000, key="st")
    s_actual = st.number_input("売上実績 (万円)", value=900, key="sa")
    s_rate = (s_actual / s_target) if s_target > 0 else 0
    
    # 粗利
    p_target = st.number_input("粗利目標 (万円)", value=300, key="pt")
    p_actual = st.number_input("粗利実績 (万円)", value=310, key="pa")
    p_rate = (p_actual / p_target) if p_target > 0 else 0
    
    # 新規契約
    n_target = st.number_input("新規目標 (件)", value=10, key="nt")
    n_actual = st.number_input("新規実績 (件)", value=8, key="na")
    n_rate = (n_actual / n_target) if n_target > 0 else 0
    
    avg_achieve = (s_rate + p_rate + n_rate) / 3
    b_score = avg_achieve * 0.6
    st.info(f"数値評価スコア: {b_score:.2%}")

with col2:
    st.header("【C】行動評価 (25%)")
    eval_map = {"S: 1.2": 1.2, "A: 1.0": 1.0, "B: 0.8": 0.8, "C: 0.5": 0.5}
    
    c1 = st.selectbox("商談・提案活動", eval_map.keys(), index=1)
    c2 = st.selectbox("CRM・報告", eval_map.keys(), index=1)
    c3 = st.selectbox("案件管理", eval_map.keys(), index=1)
    c4 = st.selectbox("顧客対応", eval_map.keys(), index=1)
    
    c_avg = (eval_map[c1] + eval_map[c2] + eval_map[c3] + eval_map[c4]) / 4
    c_score = c_avg * 0.25
    st.info(f"行動評価スコア: {c_score:.2%}")

with col3:
    st.header("【D】姿勢・貢献度 (15%)")
    pose_map = {"A: 1.0": 1.0, "B: 0.8": 0.8, "C: 0.5": 0.5}
    
    d1 = st.selectbox("チーム貢献", pose_map.keys(), index=0)
    d2 = st.selectbox("勤怠・規律", pose_map.keys(), index=0)
    d3 = st.selectbox("業務改善", pose_map.keys(), index=0)
    d4 = st.selectbox("会社方針理解", pose_map.keys(), index=0)
    
    d_avg = (pose_map[d1] + pose_map[d2] + pose_map[d3] + pose_map[d4]) / 4
    d_score = d_avg * 0.15
    st.info(f"姿勢評価スコア: {d_score:.2%}")

st.divider()

# --- 【E/F/G】最終計算エリア ---
res_col1, res_col2 = st.columns([1, 2])

with res_col1:
    st.header("【G】調整・最終判断")
    # ご要望のスライダー
    adjust_factor = st.slider("チーム調整係数", min_value=0.50, max_value=1.50, value=1.00, step=0.01)
    st.write(f"現在の係数: **{adjust_factor}**")

with res_col2:
    st.header("💰 計算結果")
    
    # 最終支給率
    final_rate = b_score + c_score + d_score
    # 基本ボーナス額
    base_bonus_amount = monthly_salary * base_bonus_months
    # 調整前支給額
    pre_adjust_amount = base_bonus_amount * final_rate
    # 最終支給額（調整係数適用）
    final_amount = pre_adjust_amount * adjust_factor
    
    # 表示
    c_final1, c_final2 = st.columns(2)
    c_final1.metric("最終支給率 (調整前)", f"{final_rate:.1%}")
    c_final2.metric("最終支給額 (円)", f"¥{int(final_amount):,}")

    # 視覚的なフィードバック
    st.progress(min(final_rate * adjust_factor, 1.0))
    st.caption(f"基本ボーナス額 ¥{int(base_bonus_amount):,} × 支給率 {final_rate:.2%} × 係数 {adjust_factor}")

# --- 保存ボタンなど（将来用） ---
if st.button("評価結果を確定・保存"):
    st.success(f"{name} さんの評価データを保存しました（※シミュレーション）")