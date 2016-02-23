from django.shortcuts import render
from django.http import HttpResponse
from .models import resultItem, gcUser
from django.utils.encoding import smart_str
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail


import json

def index(request):
	if request.user.is_authenticated():
		return render(request, 'welcome.html')
	return render(request, 'index.html')

def validateEmail( email ):
    
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def isValidUsername(field_data):
    try:
        User.objects.get(username=field_data)
    except User.DoesNotExist:
        return True
    return False

def isValidEmail(field_data):
    try:
        User.objects.get(email=field_data)
    except User.DoesNotExist:
        return True
    return False
        

def register(request):
	if request.user.is_authenticated():
		print request.user.get_username()
		return HttpResponseRedirect(reverse('welcome'))
	if request.method == 'POST':
		print 'yolooooo22222'
		username = request.POST['inputUsername']
		emailID = request.POST['inputEmail']
		passw = request.POST['inputPassword']
		if validateEmail(emailID) == True and len(username) != 0 and len(passw) != 0 and isValidEmail(emailID) == True and isValidUsername(username) == True:
			print 'success'
			user = User.objects.create_user(username, emailID, passw)
			this_user = gcUser.objects.create(user=user,choice_schools_branch_degree='')
			return HttpResponseRedirect(reverse('index'))
		else:
			print 'fail'
			return HttpResponseRedirect(reverse('register'))

	else:
		print 'yolooooo'
		return render(request, 'register.html')

def logoutUser(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))


def welcomeUser(request):
	print request
	if request.user.is_authenticated():
		return render(request, 'welcome.html')
	if request.method == 'POST':
		print request.POST
		username = request.POST['username']
		passw = request.POST['passwd']
		user = authenticate(username=username,password=passw)
		if user is not None:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect(reverse('welcome'))
	return render(request, 'index.html')

# data_list = list of dicts, item = django query item
def found_match(item, data_list):
	idx = 0
	for it in data_list:
		#flag = False

		#if it.get('school') != None:
		#	if it['school'].find('Oswego') != -1:
		#		if item.school == it['school']:
		#			flag = True
						
		if item.school != it.get('school','null'):
			idx += 1
			continue
		

		if item.branch != it.get('branch','null'):
			idx += 1
			continue
		
		if item.degree != it.get('degree','null'):
			idx += 1
			continue
	
		if item.stats != it.get('stats','null'):
			idx += 1
			continue
		
		if item.via != it.get('via','null'):
			idx += 1
			continue

		if item.decision != it.get('decision','null'):
			idx += 1
			continue
		
		return idx
	return -1

def save_college(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			college = request.POST['college']
			branch = request.POST['branch']
			print request.POST
			if request.POST['degree'] == 'ms':
				degree = ' Masters (F16)'
			else:
				degree = ' PhD (F16)'
			choice_sbg = college + '$' + branch + '$' + degree + '&'
			try:
				this_user = gcUser.objects.get(user = request.user)
				this_user.choice_schools_branch_degree = this_user.choice_schools_branch_degree + choice_sbg
				this_user.save()
			except ObjectDoesNotExist:
				this_user = gcUser.objects.create(user = request.user)
				this_user.choice_schools_branch_degree = choice_sbg
				this_user.save()
			return HttpResponseRedirect(reverse('listOfColleges'))
		else:
			return render(request,'index.html')
	else:
		return render(request,'index.html')

def deleteColleges(request):
	if request.user.is_authenticated():
		this_user = gcUser.objects.get(user=request.user)
		this_user.choice_schools_branch_degree = ''
		this_user.save()
		
		return render(request,'welcome.html')
	else:
		return render(request,'index.html')

def listOfColleges(request):
	if request.user.is_authenticated():
		this_user = gcUser.objects.get(user = request.user)
		choice_sbg = this_user.choice_schools_branch_degree
		context = {
			'data' : []
		}
		school = []
		branch = []
		degree = []
		user_school_branch_degree = this_user.choice_schools_branch_degree.split('&')
		#print user_school_branch_degree
		for sch in user_school_branch_degree:
			if sch:
				print sch
				u_sbg = sch.split('$')
				print u_sbg
				if len(u_sbg) == 0:
					break
				school.append(u_sbg[0])
				branch.append(u_sbg[1])
				degree.append(u_sbg[2])
		context['data'] = zip(school,branch,degree)
		#print context
		return render(request, 'listOfColleges.html', context)

	else:
		return render(request,'index.html')

def swapSubscription(request):
	if request.user.is_authenticated():
		this_user = gcUser.objects.get(user=request.user)
		if this_user.enable_email == True:
			this_user.enable_email = False
			this_user.save()
			return HttpResponse("Subscription disabled. To enable, go to homepage.")
		else:
			this_user.enable_email = True
			this_user.save()
			return HttpResponse("Subscription enabled. To disable, go to homepage.")
	else:
		return HttpResponse("Please login")

def updateDB(request):
	data = []
	with open('/Users/nishaddawkhar/django_apps/gradCafeResults/result.json') as f:
		for line in f:
			#print line
			if line[-1] == '\n':
				line = line[:-1]
			if line[0] != '{':
				line = line[1:]
			#print line
			if line[-1] != '}':
				line = line[:-1]
			#print line
			data.append(json.loads(line))
	#print data

	all_result_items = resultItem.objects.order_by('-time_added').all()
	#print all_result_items

	found = 0
	idx = 0
	match_idx = -1

	for it in all_result_items:
		idx_found = found_match(it, data)
		if idx_found != -1:
			if found == 0:
				match_idx = idx_found
			found += 1
			if found == 7:
				break
		else:
			found = 0
			match_idx = -1
		idx += 1

	if len(all_result_items) == 0:
		match_idx = len(data)
		#print 'emptyyyyy'

	print match_idx
	for i in range(match_idx-1,-1,-1):
		if 'branch' in data[i]:
			new_item = resultItem(school=data[i]['school'], branch=data[i]['branch'], degree=data[i].get('degree','null'), stats=data[i].get('stats','null'), via=data[i]['via'], decision=data[i].get('decision','null'))
			new_item.save()
			#print 'Found new item: '
			#print data[i]
			all_users = gcUser.objects.all()
			for user in all_users:
				user_school_branch_degree = user.choice_schools_branch_degree.split('&')
				#print user_school_branch_degree
				for sch in user_school_branch_degree:
					u_sbg = sch.split('$')
					#print u_sbg
					if data[i]['school'] == u_sbg[0]:
						if data[i]['branch'] == u_sbg[1]:
							if data[i].get('degree','null') == u_sbg[2]:
								print 'Gotta email user :D'
								#print data[i]
								if user.enable_email == True:
									send_mail('Grad Cafe Result Monitor[New Decision]', 'School: '+data[i]['school']+'\nBranch: '+data[i]['branch']+'\nDegree: '+data[i].get('degree','null'), 'gradcaferesultmonitor@gmail.com',['nishad.dawkhar94@gmail.com'], fail_silently=False)
									print 'mail_sent'
	
	return HttpResponse("hi")