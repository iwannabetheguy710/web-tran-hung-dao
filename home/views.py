from django.shortcuts import *
from django.http import *
from django.contrib.auth.models import *
from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError
from .models import *
from django.db.models import *

import hashlib # for hash with salt

def index_page(req):
	latest_post = NewFeed.objects.all()[:20]
	loi_hs = ['' for i in range(len(latest_post))]
	for k, v in enumerate(loi_hs):
		loi_hs[k] = latest_post[k].loi_hs.split('\r\n')
	for k, v in enumerate(loi_hs[0]):
		loi_hs[0][k] = v.split(',')
	for k, v in enumerate(latest_post):
		latest_post[k].loi_hs = loi_hs[k]
	return render(req, 'pages/index.html', {'latest_post': latest_post})

def login_page(req):
	if req.user.is_authenticated:
		return redirect('/')
	salt = "-`>"
	if req.method =="POST":
		username = req.POST['usr-name']
		passwd = hashlib.sha256(bytes(salt.join(list(req.POST["usr-pwd"])), encoding='utf-8')).hexdigest()
		usr = authenticate(username=username, password=passwd)
		if usr is not None:
			login(req, usr)
			return redirect('/')
		else:
			return render(req, 'pages/login.html', {'msg_err': 'Tên tài khoản hoặc mật khẩu không chính xác, vui lòng thử lại.'})
	return render(req, 'pages/login.html')

def logout_page(req):
	if req.user.is_authenticated:
		logout(req)
	return redirect('/')

def register_page(req):
	if req.user.is_authenticated:
		return redirect('/')
	salt = "-`>"
	if req.method == "POST":
		username = req.POST["usr-name"]
		email = req.POST["usr-email"]
		passwd = hashlib.sha256(bytes(salt.join(list(req.POST["usr-pwd"])), encoding='utf-8')).hexdigest()
		repasswd = hashlib.sha256(bytes(salt.join(list(req.POST["re-usr-pwd"])), encoding='utf-8')).hexdigest()
		if len(req.POST["usr-pwd"]) < 8 and len(req.POST["usr-pwd"]) > 25:
			return render(req, 'pages/register.html', {'msg_err': 'Mật khẩu của bạn phải có độ dài từ 8 đến 25 ký tự.'})
		elif passwd == repasswd:
			try:
				for i in username:
					if (len(username) < 3 or len(username) > 30) or i not in '0123456789qwertyuiopasdfghjklzxcvbnm':
						return render(req, 'pages/register.html', {'msg_err': 'Tên tài khoản của bạn phải từ 4 tới 30 ký tự. Không bao gồm dấu cách và các ký tự đặc biệt.'})
				user = User.objects.create_user(username, email, passwd)
				user.save()
			except IntegrityError:
				return render(req, 'pages/register.html', {'msg_err': 'Tên tài khoản đã tồn tại.'})
			return render(req, 'pages/registered.html')
		else:
			return render(req, 'pages/register.html', {'msg_err': 'Mật khẩu của bạn khi nhập lại không khớp.'})
	elif req.method == "GET":
		return render(req, 'pages/register.html')

def tkb_page(req):
	class_tag = [f'B{x}' for x in range(1, 11)]
	return render(req, 'pages/tkb.html', {'class_tag': class_tag})

def tkb_detail_page(req, class_name):
	tkb = TKB.objects.filter(class_name=class_name)[0]
	csv = tkb.TKB_content.split('\n')
	for k,v in enumerate(csv):
		csv[k] = v.split(',')
	timet = [['7h - 7h45'], ['7h55 - 8h40'], ['8h55 - 9h40'], ['9h50 - 10h35'], ['10h40 - 11h25']]
	for k, v in enumerate(csv):
		csv[k] = timet[k] + csv[k]
	return render(req, 'pages/tkbdetail.html', {
		'class_name': class_name,
		'table': csv,
	})

def tkb_edit_page(req, class_name):
	if (req.user.is_authenticated and (req.user.is_staff  or req.user.is_superuser)) == False:
		raise Http404
	tkb = TKB.objects.filter(class_name=class_name)[0]
	csv = tkb.TKB_content.split('\n')
	prev = tkb.TKB_content.split('\n')
	for k,v in enumerate(csv):
		csv[k] = v.split(',')
		prev[k] = v.split(',')
	timet = [['7h - 7h45'], ['7h55 - 8h40'], ['8h55 - 9h40'], ['9h50 - 10h35'], ['10h40 - 11h25']]
	for k, v in enumerate(prev):
		prev[k] = timet[k] + prev[k]
	if req.method == "POST":
		for i in range(5):
			for j in range(6):
				val = req.POST[f'rc-{i}{j}']
				csv[i][j] = val if val != '' else csv[i][j]
		for k, v in enumerate(csv):
			csv[k] = ','.join(csv[k])
		csv = '\n'.join(csv)
		tkb.TKB_content = csv
		tkb.save()
		return redirect(f'/tkb/{class_name}/edit/')
	if req.method == "GET":
		return render(req, 'pages/tkbedit.html', {
			'class_name': class_name,
			'table': prev,
		})