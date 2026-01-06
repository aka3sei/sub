import streamlit as st
import pandas as pd
# import gspread  # 実際の実装時にインストール・有効化
# from google.oauth2.service_account import Credentials

# --- スプレッドシート記録用の関数（概念） ---
def save_to_spreadsheet(data):
    """
    ここにGoogle Sheets APIとの連携コードを記述します。
    現在はシミュレーションとして、保存された内容を画面に表示します。
    """
    # 実際の手順:
    # 1. 認証情報の読み込み
    # 2. シートを開く
    # 3. 最終行に data を追加
    st.toast("Googleスプレッドシートにデータを書き込みました！", icon="✅")

# ページ設定
st.set_page_config(page_title="営業評価シミュレーター", layout="wide")

st.title("📊 営業評価・ボーナス算定シミュレーター")

# --- 【A】基本情報 ---
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

# --- メイン評価エリア（B/C/Dは前回のスライダーを維持） ---
col1, col2, col3 = st.columns(3)

with col1:
    st.header("【B】数値評価 (60%)")
    s_target = st.number_input("売上目標", value=1000)
    s_actual = st.number_input("売上実績", value=900)
    s_rate = (s_actual / s_target) if s_target > 0 else 0
    # ...他項目省略(前回と同様)...
    b_score = s_rate * 0.6 # 簡易計算
    st.metric("数値評価スコア", f"{b_score:.2%}")

def eval_slider(label, key, default=1.0, is_posture=False):
    max_val = 1.0 if is_posture else 1.2
    return st.slider(label, 0.5, max_val, default, 0.1, key=key)

with col2:
    st.header("【C】行動評価 (25%)")
    c1 = eval_slider("商談・提案活動", "c1")
    c_avg = c1 # 簡易計算
    c_score = c_avg * 0.25
    st.metric("行動評価スコア", f"{c_score:.2%}")

with col3:
    st.header("【D】姿勢・貢献度 (15%)")
    d1 = eval_slider("チーム貢献", "d1", is_posture=True)
    d_avg = d1 # 簡易計算
    d_score = d_avg * 0.15
    st.metric("姿勢評価スコア", f"{d_score:.2%}")

st.divider()

# --- 【G】最終調整 & 【F】算定結果 ---
res_col1, res_col2 = st.columns([1, 2])
with res_col1:
    st.header("【G】最終調整")
    adjust_factor = st.slider("チーム調整係数", 0.80, 1.20, 1.00, 0.01)

with res_col2:
    st.header("💰 算定結果")
    final_rate = b_score + c_score + d_score
    base_bonus = monthly_salary * base_bonus_months
    total_rate = final_rate * adjust_factor
    final_amount = int(base_bonus * total_rate)
    st.metric("最終支給額", f"¥{final_amount:,}", delta=f"支給率 {total_rate:.2%}")

st.header("📝 【H】評価コメント")
feedback = st.text_area("フィードバック内容を入力してください")

st.divider()

# --- 【確定・記録ボタン】 ---
if st.button("評価内容をスプレッドシートに記録する", type="primary"):
    # 保存するデータの作成
    record_data = {
        "氏名": name,
        "評価期間": eval_period,
        "月給": monthly_salary,
        "支給率": f"{total_rate:.2%}",
        "支給額": final_amount,
        "調整係数": adjust_factor,
        "フィードバック": feedback
    }
    
    # スプレッドシート保存関数の呼び出し
    save_to_spreadsheet(record_data)
    
    # 完了プレビュー表示
    st.success("スプレッドシートへの記録が完了しました。")
    st.json(record_data) # 記録内容を画面にも表示
