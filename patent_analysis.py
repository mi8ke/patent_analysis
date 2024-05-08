# %% [markdown]
# j-platpatにて発明･考案の名称/タイトルを無人搬送車とし、日付指定を20000101～20240502とした。
# 国内文献が731件ヒットし、csv出力した結果が特実_国内文献.csvである。

# %%
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
import japanize_matplotlib

# CSVファイル読み込み
df = pd.read_csv("特実_国内文献.csv")

# 出願年を抽出
df["出願年"] = pd.to_datetime(df["出願日"]).dt.year

# 年ごとの出願件数集計
df_grouped = df.groupby("出願年")["文献番号"].count().reset_index()
df_grouped.columns = ["出願年", "出願件数"]

# 発明者/権利者ごとの一年ごとの出願件数を集計　ピボットテーブルにする
inventor_counts = df.groupby(
    ["出願人/権利者", "出願年"])["文献番号"].count().unstack().fillna(0)  # NaN値を0で置き換える
inventor_counts = inventor_counts.astype(int)

# 出願者ごとの出願数
inventor_application_counts = inventor_counts.sum(axis=1)
# 出願年ごとの出願数
annual_applications = inventor_counts.sum(axis=0)

# %%
# グラフ作成
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(annual_applications.index,
              annual_applications.values, color='skyblue')
# 軸ラベルとタイトル設定
plt.xlabel("出願年", fontsize=12)
plt.ylabel("出願件数", fontsize=12)

# グリッド線と目盛設定
# ax.grid(True)
major_locator = MultipleLocator(1)
ax.xaxis.set_major_locator(major_locator)

# 日本語表示設定
plt.rcParams['font.family'] = 'MS Gothic'
plt.tick_params(labelsize=10)

# 横軸ラベルの範囲設定
ax.set_xlim(df_grouped["出願年"].min()-0.5, df_grouped["出願年"].max()+0.5)
plt.xticks(rotation=45)

# グラフ表示
plt.tight_layout()
plt.show()

# %%

# Assuming 'annual_applications' is a pandas Series

# Create a Plotly figure
fig = go.Figure()

# Add bar chart data
fig.add_trace(go.Bar(
    x=annual_applications.index,
    y=annual_applications.values,
    name="出願件数",
    marker_color='skyblue',
))

# Set axis labels and title
fig.update_xaxes(title="出願年", titlefont={"size": 16})
fig.update_yaxes(title="出願件数", titlefont={"size": 16})

# Configure grid and ticks
# fig.update_xaxes(showgrid=True, ticks="outside", ticktextsize=12)
fig.update_xaxes(showgrid=True, ticks="outside",
                 ticktext=df_grouped["出願年"].astype(str))
fig.update_yaxes(showgrid=True, ticks="outside",
                 ticktext=df_grouped["出願件数"].astype(str))


# Set Japanese font
fig.update_layout(font={"family": "YuGothic"})

# Set x-axis range with a slight buffer
fig.update_xaxes(range=[df_grouped["出願年"].min() -
                 0.5, df_grouped["出願年"].max() + 0.5])

# Adjust layout
fig.update_layout(
    width=800,
    height=500,
    margin=dict(l=20, r=20, t=40, b=40),
)

# Display the chart
fig.show()

htmlStr = fig.to_html(full_html=True, include_plotlyjs='cdn')

# ファイルに書き込み
with open("annual_applications.html", "w") as f:
    f.write(htmlStr)

# 或いは、write_html で直接ファイル書き出し
fig.write_html("annual_applications2.html",
               full_html=True, include_plotlyjs=True)

# %%
# 上位n人の発明者を表示する
n = 20

inventor_application_counts_sorted = inventor_application_counts.sort_values(
    ascending=False)

top_inventors = inventor_application_counts_sorted.index[:n]
top_counts = inventor_application_counts_sorted.values[:n]

# グラフ作成
plt.figure(figsize=(10, 8))
bars = plt.barh(top_inventors, top_counts,
                color='skyblue'
                )
# Add labels for each bar
for i, (bar, count) in enumerate(zip(bars, top_counts)):
    label_text = f"{count:,}"  # Format count with commas for readability
    x_offset = 0.5  # Adjust this offset to position the label correctly
    center_x, center_y = bar.get_center()

    plt.text(bar.get_width() + x_offset, center_y, label_text,
             ha='left', va='center', fontsize=10, color='black')

# 凡例を表示
# plt.legend(loc="lower right")  # 凡例の位置を右上に変更
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # 凡例の位置を右上に変更

plt.xlabel("出願件数")
plt.title("発明者/権利者別分布")
# plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

# %%

# データフレームを作成
df = pd.DataFrame({
    "発明者": top_inventors,
    "出願件数": top_counts
})

# 棒グラフを作成
fig = px.bar(df, x="出願件数", y="発明者", orientation="h",
             labels={"発明者": "発明者/権利者", "出願件数": "出願件数"})
# # y軸のメモリを100ごとに表示
# fig.update_layout(yaxis=dict(showticklabels=True))
# # 数字のフォントサイズを大きくする
# fig.update_traces(textfont_size=46)
fig.update_layout(width=800, height=500)

# グラフを表示
fig.show()

htmlStr = fig.to_html(full_html=True, include_plotlyjs='cdn')

# ファイルに書き込み
with open("inventors.html", "w") as f:
    f.write(htmlStr)

# 或いは、write_html で直接ファイル書き出し
fig.write_html("inventors2.html",
               full_html=True, include_plotlyjs=True)

# %%

# 不明なキーを削除
top_inventor_counts = inventor_counts.drop(index=inventor_counts.index[~inventor_counts.index.isin(
    top_inventors)], inplace=False)

top_inventors_list = top_inventors.tolist()
reversed_top_inventors_list = top_inventors_list[::-1]
top_inventor_counts = top_inventor_counts.loc[reversed_top_inventors_list]

# # データを正規化する
# top_inventor_counts_standardization = (top_inventor_counts - top_inventor_counts.mean()
#                    ) / top_inventor_counts.std()

# 発明者/権利者名のリストを作成
top_inventor_names = top_inventor_counts.columns.tolist()
# 発明者/権利者番号を作成
top_inventor_numbers = range(len(top_inventor_names))

# サブプロットを作成
fig, ax = plt.subplots(figsize=(10, 6))

# パテントマップの作成
cmap = plt.cm.Blues  # 他のカラーマップに変更することもできます
vmin = top_inventor_counts.min().min()
vmax = top_inventor_counts.max().max()
ax.pcolor(top_inventor_counts,
          cmap=cmap, vmin=vmin, vmax=vmax)  # 修正

ax.set_xticks([i + 0.5 for i in range(len(top_inventor_numbers))])
ax.set_yticks([i + 0.5 for i in range(len(top_inventor_counts.index))])

# 軸の目印のラベルを設定
ax.set_xticklabels(top_inventor_names, rotation=45, ha="right")
ax.set_yticklabels(top_inventor_counts.index)

# グラフのタイトルを設定
plt.title("発明者/権利者ごとの一年ごとの出願数のパテントマップ")

# グラフを表示
plt.tight_layout()
plt.show()

# %%

# 不明なキーを削除
top_inventor_counts = inventor_counts.drop(index=inventor_counts.index[~inventor_counts.index.isin(
    top_inventors)], inplace=False)

top_inventors_list = top_inventors.tolist()
reversed_top_inventors_list = top_inventors_list[::-1]
# top_inventor_counts = top_inventor_counts.loc[reversed_top_inventors_list]
top_inventor_counts = top_inventor_counts.loc[top_inventors_list]

# 発明者/権利者名のリストを作成
top_inventor_names = top_inventor_counts.columns.tolist()

# パテントマップを作成
fig = px.imshow(top_inventor_counts, x=top_inventor_names,
                y=top_inventor_counts.index,  # y軸の値を指定
                labels={"x": "年", "y": "発明者/権利者", "color": "出願件数"},
                title="発明者/権利者ごとの一年ごとの出願数のパテントマップ")
# x軸の目盛を1年ごとに設定
fig.update_xaxes(dtick=1, tickformat="%Y")  # dtickで目盛間隔を1年、tickformatで年のみ表示

# fig.update_yaxes(tickwidth=1)
# fig.update_xaxes(tickwidth=1)
fig.update_layout(width=1000, height=800)

# グラフを表示
fig.show()

htmlStr = fig.to_html(full_html=True, include_plotlyjs='cdn')

# ファイルに書き込み
with open("patent_map.html", "w") as f:
    f.write(htmlStr)

# 或いは、write_html で直接ファイル書き出し
fig.write_html("patent_map2.html",
               full_html=True, include_plotlyjs=True)
