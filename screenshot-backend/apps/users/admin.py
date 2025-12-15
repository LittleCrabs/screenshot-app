from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from openpyxl import load_workbook
from .models import User

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(label='Excel文件', help_text='请上传包含用户信息的Excel文件（.xlsx）')

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'phone', 'department', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'department']
    search_fields = ['username', 'phone', 'department']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('扩展信息', {'fields': ('phone', 'department')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('扩展信息', {'fields': ('phone', 'department')}),
    )
    
    change_list_template = 'admin/users/user/change_list.html'
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.admin_site.admin_view(self.import_excel), name='users_user_import_excel'),
        ]
        return custom_urls + urls
    
    def import_excel(self, request):
        from django.shortcuts import render, redirect
        from django.contrib import messages
        
        if request.method == 'POST':
            form = ExcelImportForm(request.POST, request.FILES)
            if form.is_valid():
                excel_file = request.FILES['excel_file']
                try:
                    wb = load_workbook(excel_file)
                    ws = wb.active
                    
                    created_count = 0
                    error_rows = []
                    
                    # 跳过表头，从第2行开始
                    for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                        if not row[0]:  # 跳过空行
                            continue
                        
                        username = str(row[0]).strip() if row[0] else ''
                        password = str(row[1]).strip() if len(row) > 1 and row[1] else 'password123'
                        phone = str(row[2]).strip() if len(row) > 2 and row[2] else ''
                        department = str(row[3]).strip() if len(row) > 3 and row[3] else ''
                        
                        if not username:
                            continue
                        
                        if User.objects.filter(username=username).exists():
                            error_rows.append(f'第{row_num}行: 用户名 {username} 已存在')
                            continue
                        
                        try:
                            user = User.objects.create_user(
                                username=username,
                                password=password,
                                phone=phone,
                                department=department,
                            )
                            created_count += 1
                        except Exception as e:
                            error_rows.append(f'第{row_num}行: {str(e)}')
                    
                    if created_count > 0:
                        messages.success(request, f'成功导入 {created_count} 个用户')
                    if error_rows:
                        messages.warning(request, '部分导入失败: ' + '; '.join(error_rows[:5]))
                    
                    return redirect('..')
                except Exception as e:
                    messages.error(request, f'导入失败: {str(e)}')
        else:
            form = ExcelImportForm()
        
        context = {
            'form': form,
            'title': '批量导入用户',
            'opts': self.model._meta,
        }
        return render(request, 'admin/users/user/import_excel.html', context)
