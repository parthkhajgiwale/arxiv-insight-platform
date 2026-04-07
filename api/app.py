from flask import Flask, jsonify, request, render_template
from db.db import get_connection
import pandas as pd
import plotly.express as px

app = Flask(__name__)


# 🏠 Home Page
@app.route("/")
def home():
    return render_template("index.html")


# 🔍 Search Page
@app.route("/search")
def search():
    query = request.args.get("q", "")

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM papers", conn)
    conn.close()

    # 🔍 Filter data
    filtered_df = df[
        df["title"].str.contains(query, case=False, na=False) |
        df["authors"].str.contains(query, case=False, na=False)
    ].copy()

    if filtered_df.empty:
        return render_template("results.html", papers=[], query=query)

    # =========================
    # 📈 GRAPH 1 — Trend (Line Chart)
    # =========================
    filtered_df["published"] = pd.to_datetime(filtered_df["published"])

    trend_df = (
        filtered_df
        .groupby(filtered_df["published"].dt.date)
        .size()
        .reset_index(name="count")
    )

    fig1 = px.line(
        trend_df,
        x="published",
        y="count",
        markers=True,
        title=f"Research Trend for '{query}'"
    )

    fig1.update_layout(
        template="plotly_white",
        height=400,
        margin=dict(l=40, r=40, t=50, b=40)
    )

    graph1 = fig1.to_html(full_html=False)

    # =========================
    # 👨‍🔬 GRAPH 2 — Top Authors
    # =========================
    authors_series = filtered_df["authors"].str.split(", ").explode()
    top_authors = authors_series.value_counts().head(8).sort_values()

    fig2 = px.bar(
        x=top_authors.values,
        y=top_authors.index,
        orientation='h',
        color=top_authors.values,
        color_continuous_scale='plasma',
        title="Top Authors"
    )

    fig2.update_traces(text=top_authors.values, textposition='outside')

    fig2.update_layout(
        template="plotly_white",
        height=400,
        bargap=0.3,
        xaxis_title="Number of Papers",
        yaxis_title="Authors"
    )

    graph2 = fig2.to_html(full_html=False)

    # =========================
    # 🧠 GRAPH 3 — Topic Distribution
    # =========================
    if "topic" in filtered_df.columns:
        topic_counts = (
            filtered_df["topic"]
            .value_counts()
            .head(8)
            .sort_values()
        )

        fig3 = px.bar(
            x=topic_counts.values,
            y=topic_counts.index,
            orientation='h',
            color=topic_counts.values,
            color_continuous_scale='viridis',
            title="Topic Distribution"
        )

        fig3.update_traces(text=topic_counts.values, textposition='outside')

        fig3.update_layout(
            template="plotly_white",
            height=400,
            bargap=0.3,
            xaxis_title="Number of Papers",
            yaxis_title="Topics"
        )

        graph3 = fig3.to_html(full_html=False)
    else:
        graph3 = None

    # =========================
    # 📦 Convert papers
    # =========================
    papers = filtered_df.to_dict(orient="records")

    return render_template(
        "results.html",
        papers=papers,
        query=query,
        graph1=graph1,
        graph2=graph2,
        graph3=graph3
    )


if __name__ == "__main__":
    app.run(debug=True)