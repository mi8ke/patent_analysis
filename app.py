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

        return render_template('index.html', plot=fig.to_html(include_plotlyjs='cdn'))

    else:
        return '有効なCSVファイルをアップロードしてください。'


if __name__ == '__main__':
    app.run(debug=True)
