# 代码生成时间: 2025-10-06 21:34:41
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from typing import List, Dict, Tuple
import numpy as np

# 假设我们有一个电影数据集和用户评分数据集
MOVIE_DATA = pd.read_csv('movies.csv')  # 电影信息
RATING_DATA = pd.read_csv('ratings.csv')  # 用户评分

# 基于用户的协同过滤算法
class UserBasedCollaborativeFiltering:
    def __init__(self):
        self.user_item_matrix = self._create_user_item_matrix(MOVIE_DATA, RATING_DATA)
        self.user_similarity_matrix = self._create_user_similarity_matrix(self.user_item_matrix)

    def _create_user_item_matrix(self, movie_data: pd.DataFrame, rating_data: pd.DataFrame) -> pd.DataFrame:
        # 创建用户-项目矩阵
        user_item_matrix = rating_data.pivot_table(index='userId', columns='movieId', values='rating', fill_value=0)
        return user_item_matrix

    def _create_user_similarity_matrix(self, user_item_matrix: pd.DataFrame) -> pd.DataFrame:
        # 计算用户相似度矩阵
        vectorizer = CountVectorizer()
        user_profiles = vectorizer.fit_transform(user_item_matrix.apply(lambda x: ' '.join(map(str, x)), axis=1))
        user_similarity_matrix = pd.DataFrame(cosine_similarity(user_profiles, user_profiles), index=user_item_matrix.index, columns=user_item_matrix.index)
        return user_similarity_matrix

    def get_recommendations(self, user_id: int, num_recommendations: int = 5) -> List[Tuple[str, float]]:
        # 获取推荐电影列表
        if user_id not in self.user_similarity_matrix.index:
            raise ValueError(f'User with id {user_id} not found in the dataset.')

        # 找到与当前用户最相似的用户列表
        similar_users = self.user_similarity_matrix[user_id].sort_values(ascending=False).head(num_recommendations).index[1:]  # 排除用户自己

        # 找到这些相似用户评分较高的电影
        recommended_movies = []
        for similar_user in similar_users:
            rated_movies = self.user_item_matrix.loc[similar_user].dropna().index.tolist()
            for movie_id in rated_movies:
                if movie_id not in [x[0] for x in recommended_movies] and self.user_item_matrix.loc[user_id, movie_id] == 0:  # 用户未评分
                    movie_title = MOVIE_DATA.loc[MOVIE_DATA['movieId'] == movie_id, 'title'].values[0]
                    recommended_movies.append((movie_title, MOVIE_DATA.loc[MOVIE_DATA['movieId'] == movie_id, 'genres'].values[0]))

        return recommended_movies

# Dash 应用
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('电影推荐系统'),
    dcc.Dropdown(
        id='user-dropdown',
        options=[{'label': f'User {i}', 'value': i} for i in MOVIE_DATA['userId'].unique()],
        value=1  # 默认选择第一个用户
    ),
    html.Div(id='recommendations-container'),
    dcc.Graph(id='similarity-graph')
])

# 回调函数：更新推荐列表
@app.callback(
    Output('recommendations-container', 'children'),
    [Input('user-dropdown', 'value')]
)
def update_recommendations(user_id: int):
    try:
        recommender = UserBasedCollaborativeFiltering()
        recommendations = recommender.get_recommendations(user_id)
        return [html.Div([f'{title} ({genres})', dcc.Markdown(r'$oxed{title} ({genres})')]) for title, genres in recommendations]
    except Exception as e:
        return html.Div([html.P(str(e))])

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)