from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from Protien.models import User
from Order.models import *
from datetime import timedelta
from django.http import HttpResponse
import xhtml2pdf as pisa
import xlwt
from Admin.models import *
# Create your views here.

# =========Admin page============#

def admin(request):
    return render(request,'Admin/adminsignin.html')

# ====== SignIn page===========#

def adminsignin(request): 
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(request,username=username,password=password)
        if user is not None:
            if user.is_superuser:
                auth.login(request,user)
                
                return redirect('adminsignin')
            else:
                messages.info(request,'You are not admin')
                return redirect('admin')
        else:
            messages.info(request,'username OR password is incorrect')
            return redirect('admin')
    else:
        return render(request,'Admin/admin.html')

#=========SignOut page=============#


@login_required(login_url='adminsignin')
def adminsignout(request): 
    auth.logout(request)
    messages.success(request,"You are logged out")
    return redirect('admin')


#==============AdminUser List=============#

@login_required(login_url='adminsignin')
def user_detailes(request):
    if 'key' in request.GET:
        key =request.GET['key']
        userslist=User.objects.filter(Q(username__icontains=key)|Q(email__icontains=key)|Q(phone_no__icontains=key))
    else:
        userslist =User.objects.all().order_by("id")
        print(userslist)
    context ={"adminuser":userslist}
    return render(request,"Admin/adminuser.html",context)

#====User Delete=====#

@login_required(login_url='adminsignin')
def user_delete(request,id):
    user =User.objects.get(id=id)
    user.delete()
    return redirect('adminuser')


#===============Block User==============#

@login_required(login_url='adminsignin')
def user_block(request,id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        if user.is_active == True:
            print(user.is_active)
            user.is_active =False
            user.save()
        
        else:
            print(user.is_active)
            user.is_active =True
            user.save()
        print("//////\\\\\\\\\\")
    return redirect('adminuser')
    


#===============Admin graph Page============#

@login_required(login_url='adminsignin')
def admin_graph(request):
    admin = ''
    # if 'admin' in request.session:
    #     admin = request.session['admin']
    # else:
    #     return redirect('/admin_sign_in')
    # this_admin = Account.objects.get(email=admin)
    sales_graph_data = []
    sales_graph_category = []
    user_graph_data = []
    user_graph_category = []
    if request.method == 'POST':
        duration = request.POST.get('duration')
        print('Getting Graph details of ', duration)
        orders = Order.objects.all()
        users = User.objects.all()
        if duration == 'today':
            sales_graph_data = []
            sales_graph_category = []
            user_graph_data = []
            user_graph_category = []
            count = 0
            # finding the number of sales on today based on orders
            cycle = 0
            for sale in orders:
                cycle = cycle + 1
                # filtering sales based on year
                if str(sale.Order_year) == str(current_date.year):
                    # filtering sales based on month
                    if str(sale.Order_month) == str(current_date.month):
                        # filtering sales based on day
                        if str(sale.Order_day) == str(current_date.day):
                            # filterin sales which has the status as delivered based on orders
                            print(sale.status)
                            if str(sale.status == 'delivered'):
                                count = count + 1
                            sales_graph_data.append(count)
                            sales_graph_category.append(cycle)
            # printing the number of sales on today
            print('Number of sales In Today Is ', count)
            for user in users:
                # filtering sales based on year
                if str(user.signup_year) == str(current_date.year):
                    # filtering sales based on month
                    if str(user.signup_month) == str(current_date.month):
                        # filtering sales based on day
                        if str(user.signup_day) == str(current_date.day):
                            count = count + 1
                            user_graph_data.append(4)
                            user_graph_category.append(1)
        elif duration == 'last_7_days':
            sales_graph_data = []
            sales_graph_category = []
            user_graph_data = []
            user_graph_category = []
            count = 0
            # getting the sales of last  days
            # value of day is from 1 to 7
            for day in range(0, 7):
                count = 0
                for sale in orders:
                    if str(sale.Order_year) == str(current_date.year):
                        # print(sale.Order_day,current_date.day-timedelta(days=day).days)
                        if str(sale.Order_day) == str(current_date.day - (timedelta(days=day).days)):
                            # print('count+',count)
                            count = count + 1
                sales_graph_data.append(count)
                sales_graph_category.append(current_date.day - (timedelta(days=day).days))
            print('Number of sales in the last 7 days is ', sales_graph_data)
            # getting the new users
            for day in range(0, 7):
                count = 0
                for user in users:
                    if str(user.signup_year) == str(current_date.year):
                        if str(user.signup_month) == str(current_date.month):
                            # print(sale.Order_day,current_date.day-timedelta(days=day).days)
                            if str(user.signup_day) == str(current_date.day - (timedelta(days=day).days)):
                                # print('count+',count)
                                count = count + 1
                user_graph_data.append(count)
                user_graph_category.append(current_date.day - (timedelta(days=day).days))
            print('Number of revenue in the last 7 days is ', user_graph_data)
        # this month
        elif duration == 'last_month':
            sales_graph_data = []
            sales_graph_category = []
            user_graph_data = []
            user_graph_category = []
            count = 0
            for day in range(1, 32):
                count = 0
                for sale in orders:
                    if str(sale.Order_year) == str(current_date.year):
                        if str(sale.Order_month) == str(current_date.month):
                            if str(sale.Order_day) == str(day):
                                count = count + 1
                sales_graph_data.append(count)
                sales_graph_category.append(day)
            for day in range(1, 32):
                count = 0
                for user in users:
                    if str(user.signup_year) == str(current_date.year):
                        if str(user.signup_month) == str(current_date.month):
                            if str(user.signup_day) == str(day):
                                count = count + 1
                user_graph_data.append(count)
                user_graph_category.append(day)


        elif duration == 'last_month':
            sales_graph_data = []
            sales_graph_category = []
            user_graph_data = []
            user_graph_category = []
            count = 0
            for day in range(1, 32):
                count = 0
                for sale in orders:
                    if str(sale.Order_year) == str(current_date.year):
                        if str(sale.Order_month) == str(current_date.month):
                            if str(sale.Order_day) == str(day):
                                count = count + 1
                sales_graph_data.append(count)
                sales_graph_category.append(day)
            for day in range(1, 32):
                count = 0
                for user in users:
                    if str(user.signup_year) == str(current_date.year):
                        if str(user.signup_month) == str(current_date.month):
                            if str(user.signup_day) == str(day):
                                count = count + 1
                user_graph_data.append(count)
                user_graph_category.append(day)



        # this year
        else:
            sales_graph_data = []
            sales_graph_category = []
            user_graph_data = []
            user_graph_category = []
            count = 0
            for month in range(1, 13):
                count = 0
                for sale in orders:
                    if str(sale.Order_year) == str(current_date.year):
                        if str(sale.Order_month) == str(month):
                            count = count + 1
                sales_graph_data.append(count)
                sales_graph_category.append(month)
            for month in range(1, 13):
                count = 0
                for user in users:
                    if str(user.signup_year) == str(current_date.year):
                        if str(user.signup_month) == str(month):
                            count = count + 1
                user_graph_data.append(count)
                user_graph_category.append(month)
    user_count = User.objects.all().count()
    sales = Order.objects.filter(status='Delivered')
    cod = Order.objects.filter(payment_mode='Cash on Delivery').count()
    paypal = Order.objects.filter(payment_mode='paypal').count()
    razorpay = Order.objects.filter(payment_mode='Paid by Razorpay').count()
    paypal_payment_method_graph_data = paypal
    razorpay_payment_method_graph_data = razorpay
    cod_payment_method_graph_data = cod
    revenue = 0
    for sale in sales:
        revenue = revenue + sale.order_total
    return render(request, 'Admin/admin_graph.html', {
        # 'duration': duration,
        'customer_count': user_count,
        'sales': sales.count(),
        'revenue': revenue,
        # 'admin': this_admin,
        'sales_graph_data': sales_graph_data,
        'sales_graph_category': sales_graph_category,
        'user_graph_data': user_graph_data,
        'user_graph_category': [user_graph_category],
        'paypal_payment_method_graph_data': paypal_payment_method_graph_data,
        'razorpay_payment_method_graph_data': razorpay_payment_method_graph_data,
        'cod_payment_method_graph_data': cod_payment_method_graph_data,
    })


#==============Render to PDF===============#

@login_required(login_url='adminsignin')
def render_to_pdf(template_src,context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type = 'application/pdf')
    return

              

#==============Converted to Exel===============#

@login_required(login_url='adminsignin')
def export_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response ['content-Disposition'] = 'attachment; filename="sales.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report')  #this will generate a file named as sales Report

    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Product Name','Category','Price','Quantity', ]
    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    total = 0
    rows = SalesReport.objects.values_list(
        'productName','categoryName', 'productPrice', 'quantity')
    for row in rows:
        total +=row[2]
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    row_num += 1
    col_num +=1
    ws.write(row_num,col_num,total,font_style)

    wb.save(response)

    return response

#==============Converted to PDF===============#

@login_required(login_url='adminsignin')
def export_to_pdf(request):
    products = Product.objects.all()
    
    sales = SalesReport.objects.all()
    total_sales = SalesReport.objects.all().aggregate(sum('productPrice'))

    template_path = 'Admin/sales_pdf.html'
    context = {
        'brand_name':products,
        'order_count':sales,
        'total_amount':total_sales['productPrice__sum'],
    } 
     # csv file can also be generated using content_type='application/csv
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


#===================Sales Report=======================#

@login_required(login_url='adminsignin')
def sales_report_date(request):
    data = OrderProduct.objects.all()
    if request.method == 'POST':
        if request.POST.get('month'):
            month = request.POST.get('month')
            print(month)
            data = OrderProduct.objects.filter(created_at__icontains=month)
            
            if data:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'Admin/sales_report.html',context)
                else:
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'Admin/sales_report.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        if request.POST.get('date'):
            date = request.POST.get('date')
            print("0,",date)
            
            date_check = OrderProduct.objects.filter(created_at__icontains=date)
            print(date_check)
            if date_check:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'Admin/sales_report.html',context)
                else:
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'Admin/sales_report.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        if request.POST.get('date1'):
            date1 = request.POST.get('date1')
            date2 = request.POST.get('date2')
            data_range = OrderProduct.objects.filter(created_at__gte=date1,created_at__lte=date2)
            if data_range:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'Admin/sales_report.html',context)
                else:
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'Admin/sales_report.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
    if data:
        if SalesReport.objects.all():
            SalesReport.objects.all().delete()
            for i in data:
                sales = SalesReport()
                sales.productName = i.product.product_name
                sales.categoryName = i.product.category.category_name
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'Admin/sales_report.html',context)

        else:
            for i in data:
                sales = SalesReport()
                sales.productName = i.product.product_name
                sales.categoryName = i.product.category.category_name
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'Admin/sales_report.html',context)
        
    else:
        messages.warning(request,"Nothing Found!!")
    
    return render(request,'Admin/sales_report.html')


