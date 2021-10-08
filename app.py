from flask import Flask, render_template, redirect, url_for, request, make_response,session,abort
from itsdangerous import Signer, BadSignature
from session_interface import MySessionInterface
from inci import Entry_Sil

#set FLASK_ENV=development

app = Flask(__name__)
app.secret_key = b"*_.sdnfks'^+)"
app.session_interface = MySessionInterface()

ES = None
hata = False
silme = []
adet = 10

def get_current_username():
	username = ""
	login_auth = False
	if "username" in session:
		username = session["username"]
		login_auth = True
	return username,login_auth


@app.route("/")
def Index():
	username,login_auth = get_current_username()
	return render_template("index.html",username=username,login_auth=login_auth)


@app.route("/login",methods=["GET","POST"])
def Login():
	global hata
	global ES

	if request.method == "POST":
		if request.form:
			if "username" in request.form and "password" in request.form:
				username = request.form["username"]
				password = request.form["password"]
				ES = Entry_Sil(username,password)
				user_data = ES.user_data
				if not user_data["error"]:
					session["username"] = username
					hata = False
					return redirect(url_for("Contact"))
				else:
					hata = True
					return redirect(url_for("Login"))
		abort(400)

	username,login_auth = get_current_username()
	return render_template("login.html",username=username,login_auth=login_auth,hata=hata)


@app.route("/contact",methods=["GET","POST"])
def Contact():
	global silme
	global adet
	if request.method == "POST":
		if request.form:
			adet = int(request.form.get("priority"))
			if adet == 0:
				adet = ES.entry_sayisi
			silme = request.form.get("message")
			silme = list(map(str,silme.split(" ")))
			return redirect(url_for("BotActivited"))

	username,login_auth = get_current_username()
	return render_template("contact.html",username=username,login_auth=login_auth)


@app.route("/incidel",methods=["GET","POST"])
def InciDel():
	global ES
	data = ""
	if request.method == "POST":
		if request.form:
			data = request.form.get("x","")
			try:
				if data not in silme:
					ES.sil(data)
			except Exception as e:
				print(e)
        username,login_auth = get_current_username()
        return data


@app.route("/botactivited")
def BotActivited():
	eids = ES.link_al(adet)
	username,login_auth = get_current_username()
	return render_template("botactivited.html",eids=eids,username=username,login_auth=login_auth)


@app.route("/contactlist")
def ContactList():
	username,login_auth = get_current_username()
	return render_template("contactlist.html",username=username,login_auth=login_auth)


@app.route("/logout")
def Logout():
	global hata
	if "username" in session:
		del session["username"]
	hata = False
	return redirect(url_for("Index"))


if __name__ == "__main__":
	app.run(debug=True)
