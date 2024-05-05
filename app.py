from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

# app = Flask(__name__, static_folder='uploads')
app = Flask(__name__)
os.makedirs('uploads', exist_ok=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_csv():

    file = request.files.get('file')
    if file and file.filename.endswith('.csv'):
        print('CSVファイルが正常にアップロードされました。')

        file_path = os.path.join('uploads', file.filename)
        # ファイル保存
        # file.save(file_path)

        df = pd.read_csv(file_path)

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

        #
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

        # 　二つ目
        # 上位n人の発明者を表示する
        n = 20
        inventor_application_counts_sorted = inventor_application_counts.sort_values(
            ascending=False)

        top_inventors = inventor_application_counts_sorted.index[:n]
        top_counts = inventor_application_counts_sorted.values[:n]

        # データフレームを作成
        df = pd.DataFrame({
            "発明者": top_inventors[::-1],
            "出願件数": top_counts[::-1]
        })

        # 棒グラフを作成
        fig2 = px.bar(df, x="出願件数", y="発明者", orientation="h",
                      labels={"発明者": "発明者/権利者", "出願件数": "出願件数"})
        # # y軸のメモリを100ごとに表示
        # fig.update_layout(yaxis=dict(showticklabels=True))
        # # 数字のフォントサイズを大きくする
        # fig.update_traces(textfont_size=46)
        fig2.update_layout(width=900, height=700)

        # fig3
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
        fig3 = px.imshow(top_inventor_counts, x=top_inventor_names,
                         y=top_inventor_counts.index,  # y軸の値を指定
                         labels={"x": "年", "y": "発明者/権利者", "color": "出願件数"},
                         title="発明者/権利者ごとの一年ごとの出願数のパテントマップ")
        # x軸の目盛を1年ごとに設定
        # dtickで目盛間隔を1年、tickformatで年のみ表示
        fig3.update_xaxes(dtick=1, tickformat="%Y")

        # fig.update_yaxes(tickwidth=1)
        # fig.update_xaxes(tickwidth=1)
        fig3.update_layout(width=1500, height=600)

        return render_template('index.html', plot=fig.to_html(include_plotlyjs='cdn'),
                               plot2=fig2.to_html(include_plotlyjs='cdn'),
                               plot3=fig3.to_html(include_plotlyjs='cdn'))

    else:
        return '有効なCSVファイルをアップロードしてください。'


if __name__ == '__main__':
    app.run(debug=True)
