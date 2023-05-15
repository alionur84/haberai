from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from scrapper import get_news
import random
import requests
import json
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("APPKEY")


class NewsForm(FlaskForm):
	news_text = TextAreaField("Haber Metni", validators=[DataRequired(), Length(min=800, max=5000)])
	submit = SubmitField("Tahmin Et")

class CategoryForm(FlaskForm): 
	random_dunya = ['ortadogu', 'avrupa_birligi', 'rusya_ukrayna']
	category = SelectField(
		'Haber Kategorisi',
		choices=[
		('saglik', 'Sağlık'),
		('ekonomi', 'Ekonomi'),
		('teknoloji', 'Teknoloji'),
		('spor', 'Spor'),
		('siyaset', 'Siyaset'),
		('kultur', 'Kültür'),
		(random.choice(random_dunya), 'Dünya')
		])
	submit = SubmitField('Haber Bul')


@app.route("/", methods = ['GET', 'POST'])
@app.route("/home", methods = ['GET', 'POST'])
def home():
	app.news_text = ""
	app.cat = ""
	form = NewsForm()
	if form.validate_on_submit():
		news_text = form.news_text.data
		form.news_text.data = ""
		app.news_text = news_text
		return redirect(url_for("display_result"))

	return render_template("index.html",
		title="Home",
		form=form)

@app.route("/display_result", methods = ['GET', 'POST'])
def display_result():
	url = os.environ.get("NEWSDETECTAPIURL")
	req_body = {"news_text": app.news_text}
	api_req = requests.post(url, json = req_body)
	response = json.loads(api_req.text)
	result = response['prediction']
	cat = ""
	return render_template("result.html", news_text=app.news_text, cat=cat, result=result, title="Sonuç")

from flask import request

@app.route("/display_result_scrapped", methods=['POST'])
def display_result_scrapped():
    news_text = request.form['news_text']
    cat = request.form['cat']
    url = os.environ.get("NEWSDETECTAPIURL")
    req_body = {"news_text": news_text}
    api_req = requests.post(url, json=req_body)
    response = json.loads(api_req.text)
    result = response['prediction']
    return render_template("result.html", news_text=news_text, cat=cat, result=result, title="Sonuç")


@app.route("/get_random_news", methods = ['GET', 'POST'])
def get_random_news():
	form = CategoryForm()
	if form.validate_on_submit():
		cat = form.category.data
		app.cat = cat
		return redirect(url_for('scrapped_news'))
	return render_template("get_random_news.html", form=form, title="Haber Bul")


@app.route("/scrapped_news", methods = ['GET', 'POST'])
def scrapped_news():
	news = get_news(app.cat)
	news = random.choice(news)
	return render_template("scrapped_display.html", news=news, cat=app.cat, title="Haber Bul")


@app.route("/project_info")
def project_info():
	return render_template("project_info.html", title="Proje Bilgileri")

@app.route("/qr_code")
def qr_code():
	return render_template("qr_code.html", title="QR Code")

@app.route("/vertex_ai_video")
def vertex_ai_video():
	return render_template("vertex_ai_video.html", title="Vertex AI - Video")

@app.route("/vertex_ai_slides")
def vertex_ai_slides():
	return render_template("vertex_ai_slides.html", title="Vertex AI - Slides")

@app.route("/lambda_slides")
def lambda_slides():
	return render_template("lambda_slides.html", title="Lambda - Slides")


# 404 error
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# internal server error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500


if __name__ == '__main__':
	app.run(debug=False)


