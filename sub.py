import streamlit as st

# ページ設定（ワイドモードで広く使う）
st.set_page_config(page_title="営業評価シミュレーター", layout="wide")

st.title("📊 営業評価・ボーナス算定シミュレーター")

# --- 【A】基本情報（メイン画面最上部に配置） ---
st.subheader("【A】基本情報")
a_col1, a_col2, a_col3, a_col4 = st.columns(4)
with a_col1:
    name = st.text_input("氏名", value="営業 太郎")
with a_col2:
    eval_period = st.text_input("評価期間", value="2025年度 上期")
with a_col3:
    monthly_salary = st.number_input("月給 (円)", value=300000, step=10000)
with a_col4:
    base_bonus_months = st.number_input("基本ボーナス月数", value=2.0, step=0.1)

st.divider()

# --- メイン評価エリア（3カラム構成） ---
col1, col2, col3 = st.columns(3)

with col1:
    st.header("【B】数値評価 (60%)")
    st.caption("目標と実績を入力")
    s_target = st.number_input("売上目標 (万円)", value=1000, key="st")
    s_actual = st.number_input("売上実績 (万円)", value=900, key="sa")
    s_rate = (s_actual / s_target) if s_target > 0 else 0
    
    p_target = st.number_input("粗利目標 (万円)", value=300, key="pt")
    p_actual = st.number_input("粗利実績 (万円)", value=310, key="pa")
    p_rate = (p_actual / p_target) if p_target > 0 else 0
    
    n_target = st.number_input("新規目標 (件)", value=10, key="nt")
    n_actual = st.number_input("新規実績 (件)", value=8, key="na")
    n_rate = (n_actual / n_target) if n_target > 0 else 0
    
    avg_achieve = (s_rate + p_rate + n_rate) / 3
    b_score = avg_achieve * 0.6
    st.metric("数値評価スコア", f"{b_score:.2%}")

# スライダー生成関数
def eval_slider(label, key, default=1.0, is_posture=False):
    max_val = 1.0 if is_posture else 1.2
    return st.slider(label, 0.5, max_val, default, 0.1, key=key)

with col2:
    st.header("【C】行動評価 (25%)")
    st.caption("S=1.2 / A=1.0 / B=0.8 / C=0.5")
    c1 = eval_slider("商談・提案活動", "c1")
    c2 = eval_slider("CRM・報告", "c2")
    c3 = eval_slider("案件管理", "c3")
    c4 = eval_slider("顧客対応", "c4")
    
    c_avg = (c1 + c2 + c3 + c4) / 4
    c_score = c_avg * 0.25
    st.metric("行動評価スコア", f"{c_score:.2%}")

with col3:
    st.header("【D】姿勢・貢献度 (15%)")
    st.caption("A=1.0 / B=0.8 / C=0.5")
    d1 = eval_slider("チーム貢献", "d1", is_posture=True)
    d2 = eval_slider("勤怠・規律", "d2", is_posture=True)
    d3 = eval_slider("業務改善", "d3", is_posture=True)
    d4 = eval_slider("会社方針理解", "d4", is_posture=True)
    
    d_avg = (d1 + d2 + d3 + d4) / 4
    d_score = d_avg * 0.15
    st.metric("姿勢評価スコア", f"{d_score:.2%}")

st.divider()

# --- 【E/F/G】計算結果・最終調整エリア ---
res_col1, res_col2 = st.columns([1, 2])

with res_col1:
    st.header("【G】最終調整")
    adjust_factor = st.slider("チーム調整係数", 0.80, 1.20, 1.00, 0.01)
    st.info(f"係数: {adjust_factor:.2f}")

with res_col2:
    st.header("💰 算定結果")
    final_rate = b_score + c_score + d_score
    base_bonus = monthly_salary * base_bonus_months
    total_rate = final_rate * adjust_factor
    final_amount = int(base_bonus * total_rate)
    
    # 支給額と最終支給率を大きく表示
    r1, r2 = st.columns(2)
    r1.metric("最終支給額", f"¥{final_amount:,}")
    r2.metric("合計支給率", f"{total_rate:.2%}", delta=f"調整前 {final_rate:.1%}")

    # 詳細な根拠
    with st.expander("🔍 この計算の根拠（内訳）を表示"):
        st.write(f"**基本ボーナス額:** ¥{int(base_bonus):,}")
        st.write(f"1. 数値評価（60%）寄与: {b_score:.2%}")
        st.write(f"2. 行動評価（25%）寄与: {c_score:.2%}")
        st.write(f"3. 姿勢評価（15%）寄与: {d_score:.2%}")
        st.write(f"--- 調整前支給率: {final_rate:.2%}")
        st.write(f"--- チーム調整（x{adjust_factor}）後の支給率: {total_rate:.2%}")
